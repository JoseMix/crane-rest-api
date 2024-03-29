from api.schemas.alert import AlertNotification

from typing import Any, Dict


async def processAlert(data: Dict[Any, Any]):
    alertNotification = AlertNotification.parse_obj(data)
    status = alertNotification.status
    alerts = alertNotification.alerts
    for alert in alerts:
        labels = alert.labels
        annotations = alert.annotations
    return " ***************-----------  alert ----------------****************"
