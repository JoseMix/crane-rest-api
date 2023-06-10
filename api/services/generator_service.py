import os
import yaml

from pathlib import Path
from fastapi.responses import JSONResponse
from api.config.proxy import getConfig
from api.schemas.app import App


def write_yaml(obj, path):
    with open(path, "w") as file:
        yaml.dump_all(obj, file)


async def docker_compose_generator(app: App):
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

    for service in app.services:
        name = service.pop('name', None)
        labels = service.get('labels', [])
        labels.extend(
            [f"a.label.name={app.name}", f"traefik.http.routers.{app.name}.rule=Host(`{app.name}-{name}.docker.localhost`)"])
        service['labels'] = labels
        yaml_obj[0]['services'][name] = service

    path = Path.cwd() / "api" / "files" / app.name / "docker-compose.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(yaml_obj, path)

    return yaml_obj


async def prometheus_yaml_generator():
    yaml_obj = [
        {

            "global": {
                "scrape_interval": "15s",
                "evaluation_interval": "15s",
                "external_labels": {
                    "monitor": "crane-monitor"
                }
            },
            "rule_files": [
                "rules.yml"
            ],
            "alerting": {
                "alertmanagers": [
                    {
                        "scheme": "http",
                    },
                    {
                        "static_configs": [
                            {
                                "targets": [
                                    "alertmanager:9093"
                                ]
                            }
                        ]
                    }
                ]
            },
            "scrape_configs": [
                {
                    "job_name": "prometheus",
                    "static_configs": [
                        {
                            "targets": [
                                "localhost:9090"
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    # third: write the yaml file
    os.makedirs(
        f'{os.getcwd()}/api/files/monitoring/prometheus',
        exist_ok=True
    )

    path = Path.cwd() / "api" / "files" / "monitoring" / \
        "prometheus" / "prometheus.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(yaml_obj, path)

    return yaml_obj


async def prometheus_scrape_generator(app: App):
    with open(f"api/files/monitoring/prometheus/prometheus.yml", "r") as file:
        file_data = yaml.safe_load(file)
        search = [scrape for scrape in file_data['scrape_configs']
                  if scrape['job_name'] == app.name]
        if not search:
            file_data['scrape_configs'].append({
                "job_name": app.name,
                "scrape_interval": "5s",
                "static_configs": [
                    {
                        "targets": [
                            f"{app.ip}:8080"
                        ]
                    }
                ]
            })
            file.close()
        else:
            return JSONResponse(status_code=400, content={"message": "App already exists"})
    with open(f"api/files/monitoring/prometheus/prometheus.yml", "w") as file2:
        yaml.dump(file_data, file2)
        file2.close()

    return file_data
