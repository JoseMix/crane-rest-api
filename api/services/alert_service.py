''' This module contains the services for managing alerts '''
from typing import Any, Dict
import json
from sqlalchemy.orm import Session
from api.schemas.alert import AlertNotification
from api.clients.OPAClient import get_opa_raw_data
import api.db.crud.app_crud as AppCrud
from api.config.constants import OPA_ALERT_RULES_CONFIG_NAME
from api.services.crane_service import start, scale


async def manage_alert(db: Session, data: Dict[Any, Any]):
    ''' Manage received alerts '''

    alert_notification = AlertNotification.parse_obj(data)
    status = alert_notification.status
    alert_name = alert_notification.groupLabels.alertname
    alerts = alert_notification.alerts

    function_name = get_opa_raw_data(OPA_ALERT_RULES_CONFIG_NAME)[
        'result'][alert_name][status]

    for alert in alerts:
        alert_app_name = alert.labels.job
        app_id = alert_app_name.split("-")[-1]
        app = AppCrud.get_by_id(db, app_id, None)
        if not app:
            continue
        function_to_execute = globals()[function_name]
        await function_to_execute(db, app)

    return {"message": "Alerts managed"}


async def start_app(db, app):
    '''Start app if not force stopped'''
    if not app.force_stop:
        await start(db, app.id)


async def send_email():
    '''Send email to user'''


async def scale_app(db, app):
    '''Scale app to current scale + 1 if current scale < max scale'''
    if app.current_scale < app.max_scale:
        app.services = json.loads(app.services)
        app.hosts = json.loads(app.hosts)
        app.current_scale += 1
        AppCrud.update(db, app)
        await scale(db, app.id, app.current_scale)


async def deescalate_app(db, app):
    '''Deescalate app to min scale'''
    if app.current_scale > app.min_scale:
        app.services = json.loads(app.services)
        app.hosts = json.loads(app.hosts)
        app.current_scale = app.min_scale
        AppCrud.update(db, app)
        await scale(db, app.id, app.current_scale)
