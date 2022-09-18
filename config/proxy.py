def getConfig(appName):
    config = {
        "name": "traefik-proxy",
        "image": "traefik:latest",
        "command": [
            "--api.insecure=true",
            "--providers.docker",
            "--metrics.prometheus=true",
            "--metrics.prometheus.buckets=0.1,0.3,1.2,5.0",
            "--entrypoints.web.address=:80",
            "--providers.docker.constraints=" +
            "Label(`a.label.name`, `" + appName + "`)",
        ],
        "ports": ["0:80", "0:8080"],
        "expose": ["8080"],
        "volumes": ["/var/run/docker.sock:/var/run/docker.sock"],
        "networks": ["crane-net", "prometheus-net"],
    }

    return config
