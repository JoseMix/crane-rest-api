def getConfig(appName):
    config = {
        "name": "traefik-proxy",
        "image": "traefik:latest",
        "command": [
            "--api.insecure=true",
            "--providers.docker=true",
            "--accesslog=true",
            "--accesslog.format=json",
            "--metrics.prometheus=true",
            "--metrics.prometheus.buckets=0.1,0.3,1.2,5.0",
            "--entrypoints.web.address=:80",
            "--providers.docker.constraints=" +
            "Label(`a.label.name`, `" + appName + "`)",
            "--providers.docker.watch=true",
        ],
        "ports": ["0:80", "0:8080"],
        "expose": ["8080"],
        "volumes": ["/var/run/docker.sock:/var/run/docker.sock"],
        "networks": ["crane-net", "prometheus-net"],
        "labels": {
            "traefik.enable": "true",
            "traefik.http.routers.traefik.rule": "Host(`traefik." + appName + ".local`)",
            "traefik.http.routers.traefik.entrypoints": "web",
            "traefik.http.routers.traefik.middlewares": "traefik-auth",
        }
    }

    return config
