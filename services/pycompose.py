import os
import json
import yaml
from pathlib import Path
from fastapi.responses import JSONResponse
from schemas.app import App


async def docker_compose_generator(app: App):
    config = open('config/proxy.json')
    proxy = json.load(config)

    if not proxy:
        return JSONResponse(status_code=400, content={"message": "Wrong proxy config detected", "proxy": proxy})

    # first: add the proxy config to yaml
    yaml_obj = [
        {
            "version": '3',
            'services': {
                proxy['name']:
                {
                    'image': proxy['image'],
                    'command': proxy['command'],
                    'ports': proxy['ports'],
                    'volumes': proxy['volumes']
                }
            }
        }
    ]

    # second: add the app config to yaml
    for service in app.services:
        name = service['name']

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
    file2 = open(f"composes/{app.name}/docker-compose.yml", "w")
    yaml.dump_all(yaml_obj, file2)
    file2.close()

    return yaml_obj
