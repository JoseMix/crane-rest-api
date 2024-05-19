''' This file contains the schema for the alert notification. '''
from typing import List, Optional
from pydantic import BaseModel


class GroupLabels(BaseModel):
    alertname: Optional[str] = None


class CommonLabels(BaseModel):
    alertname: Optional[str] = None
    code: Optional[str] = None
    entrypoint: Optional[str] = None
    instance: Optional[str] = None
    job: Optional[str] = None
    method: Optional[str] = None
    monitor: Optional[str] = None
    protocol: Optional[str] = None
    severity: Optional[str] = None


class Annotations(BaseModel):
    description: Optional[str] = None
    summary: Optional[str] = None


class Alert(BaseModel):
    status: str
    labels: CommonLabels
    annotations: Annotations
    startsAt: str
    endsAt: str
    generatorURL: str
    fingerprint: str


class AlertNotification(BaseModel):
    receiver: str
    status: str
    alerts: List[Alert]
    groupLabels: GroupLabels
    commonLabels: CommonLabels
    commonAnnotations: Annotations
    externalURL: str
    version: str
    groupKey: str
    truncatedAlerts: int
