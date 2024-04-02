# CRANE: despliegue inteligente de contenedores

Crane es una API de proposito general que permite desplegar imagenes de docker y simular una estructura cloud localmente, con el fin de probar aplicaciones en un entorno controlado.
En esta api utilizamos la libreria de docker-py y python-on-whales para interactuar con el demonio de docker y desplegar contenedores.

conda activate crane-restapi
uvicorn app:app --reload

Metricas de Prometheus:
traefik_entrypoint_requests_total
traefik_entrypoint_requests_duration_seconds

Endpoint de Prometheus:
http://localhost:9090/

Endpoint de AlertManager:
http://localhost:9093/


Test de carga con artillery:
artillery quick -k --count 10 -n 20 http://appnueva-b9811f52-whoami.docker.localhost:32769



revisar lint