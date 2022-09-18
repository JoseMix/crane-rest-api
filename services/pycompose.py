import json
import os
import yaml
from pathlib import Path
from config.proxy import getConfig
from fastapi.responses import JSONResponse
from schemas.app import App


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

    # second: add the app config to yaml
    for service in app.services:
        name = service['name']
        labels = service['labels'] if 'labels' in service else []
        labels.append(f"a.label.name={app.name}")
        labels.append(
            f"traefik.http.routers.{app.name}.rule=Host(`{app.name}-{name}.docker.localhost`)")
        service['labels'] = labels
        yaml_obj[0]['services'] = {
            **yaml_obj[0]['services'], **{name: {}}
        }

        del service['name']

        for attr, value in service.items():
            yaml_obj[0]['services'][name] = {
                **yaml_obj[0]['services'][name], **{attr: value}
            }

    # third: write the yaml file
    os.makedirs(f'{os.getcwd()}/composes/{app.name}', exist_ok=True)
    file = open(f"composes/{app.name}/docker-compose.yml", "w")
    yaml.dump_all(yaml_obj, file)
    file.close()

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
            "scrape_configs": []
        }
    ]

    # third: write the yaml file
    os.makedirs(
        f'{os.getcwd()}/composes/monitoring/prometheus',
        exist_ok=True
    )

    file = open(
        f"composes/monitoring/prometheus/prometheus.yml", "w")
    yaml.dump_all(yaml_obj, file)

    file.close()

    return yaml_obj


async def prometheus_scrape_generator(app: App):
    with open(f"composes/monitoring/prometheus/prometheus.yml", "r") as file:
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
    with open(f"composes/monitoring/prometheus/prometheus.yml", "w") as file2:
        yaml.dump(file_data, file2)
        file2.close()

    return file_data
