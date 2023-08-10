# CRANE: despliegue inteligente de contenedores

Crane es una API de proposito general que permite desplegar imagenes de docker y simular una estructura cloud localmente, con el fin de probar aplicaciones en un entorno controlado.
En esta api utilizamos la libreria de docker-py y python-on-whales para interactuar con el demonio de docker y desplegar contenedores.

conda activate crane-restapi
uvicorn app:app --reload

Metricas de Prometheus:
traefik_entrypoint_requests_total
