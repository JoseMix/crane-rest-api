import os
import yaml
import shutil
import copy
from pathlib import Path
from fastapi.responses import JSONResponse
from api.config.proxy import getConfig
from api.schemas.app import App
from api.config.constants import *


def write_yaml(obj, path):
    with open(path, "w") as file:
        yaml.dump_all(obj, file)


def docker_compose_generator(app: App):
    app = copy.deepcopy(app)

    proxy = getConfig(app.name)

    if not proxy:
        return JSONResponse(status_code=400, content={"message": "Wrong proxy config detected", "proxy": proxy})

    # first: add the proxy config to yaml
    yaml_obj = [
        {
            "version": '3',
            "networks": {
                "prometheus-net": {
                    "external": True
                },
                "crane-net": {}
            },
            'services': {
                proxy['name']:
                {
                    'image': proxy['image'],
                    'command': proxy['command'],
                    'ports': proxy['ports'],
                    'volumes': proxy['volumes'],
                    'networks': proxy['networks']
                }
            }
        }
    ]
    app_hosts = []
    services = app.services

    for service in services:
        name = service.pop('name', None)
        labels = service.get('labels', [])
        labels.extend(
            [f"a.label.name={app.name}", f"traefik.http.routers.{app.name}.rule=Host(`{app.name}-{name}.docker.localhost`)"])
        app_hosts.append(f"{app.name}-{name}.docker.localhost")
        service['labels'] = labels
        yaml_obj[0]['services'][name] = service

    path = Path.cwd() / TEMP_FILES_PATH / app.name / "docker-compose.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(yaml_obj, path)

    return {
        "hosts": app_hosts,
        "path": path,
        "yaml": yaml_obj
    }


def docker_compose_remove(app_name: str):
    if REMOVE_TEMP_FILES:
        path = Path.cwd() / TEMP_FILES_PATH / app_name
        shutil.rmtree(path)
        return "App removed"
    else:
        return "App not removed because REMOVE_TEMP_FILES is False"


def prometheus_yaml_generator():
    yaml_obj = [
        {

            "global": {
                "scrape_interval": GLOBAL_SCRAPE_INTERVAL,
                "evaluation_interval": GLOBAL_EVALUATION_INTERVAL,
                "external_labels": {
                    "monitor": EXTERNAL_LABELS_MONITOR
                }
            },
            "rule_files": [
                RULES_FILE
            ],
            "alerting": {
                "alertmanagers": [
                    {
                        "scheme": ALERT_MANAGER_SCHEME,
                    },
                    {
                        "static_configs": [
                            {
                                "targets": [
                                    f"alertmanager:{ALERT_MANAGER_PORT}"
                                ]
                            }
                        ]
                    }
                ]
            },
            "scrape_configs": [
                {
                    "job_name": PROMETHEUS_SCRAPE_JOB_NAME,
                    "static_configs": [
                        {
                            "targets": [
                                f"localhost:{PROMETHEUS_PORT}"
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    # third: write the yaml file
    os.makedirs(
        f'{os.getcwd()}/{MONITORING_FILES_PATH}/prometheus',
        exist_ok=True
    )

    path = Path.cwd() / MONITORING_FILES_PATH / "prometheus" / PROMETHEUS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(yaml_obj, path)

    return yaml_obj


def prometheus_scrape_generator(app: App):
    with open(f"{MONITORING_FILES_PATH}/prometheus/{PROMETHEUS_FILE}", "r") as file:
        file_data = yaml.safe_load(file)
        search = [scrape for scrape in file_data['scrape_configs']
                  if scrape['job_name'] == app.name]
        if not search:
            file_data['scrape_configs'].append({
                "job_name": app.name,
                "scrape_interval": PROMETHEUS_SCRAPE_INTERVAL,
                "static_configs": [
                    {
                        "targets": [
                            f"{app.ip}:{TARGET_PORT}"
                        ]
                    }
                ]
            })
            file.close()
        else:
            return JSONResponse(status_code=400, content={"message": "App already exists"})
    with open(f"{MONITORING_FILES_PATH}/prometheus/{PROMETHEUS_FILE}", "w") as file2:
        yaml.dump(file_data, file2)
        file2.close()

    return file_data


def prometheus_scrape_remove(app_name: str):
    with open(f"{MONITORING_FILES_PATH}/prometheus/{PROMETHEUS_FILE}", "r") as file:
        file_data = yaml.safe_load(file)
        file_data['scrape_configs'] = [
            scrape for scrape in file_data['scrape_configs'] if scrape['job_name'] != app_name]
        file.close()
    with open(f"{MONITORING_FILES_PATH}/prometheus/{PROMETHEUS_FILE}", "w") as file2:
        yaml.dump(file_data, file2)
        file2.close()

    return file_data
