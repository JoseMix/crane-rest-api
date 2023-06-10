# CRANE: despliegue inteligente de contenedores

Crane es una API de proposito general que permite desplegar imagenes de docker y simular una estructura cloud localmente, con el fin de probar aplicaciones en un entorno controlado.
En esta api utilizamos la libreria de docker-py y python-on-whales para interactuar con el demonio de docker y desplegar contenedores.

conda activate crane-restapi
uvicorn app:app --reload

docker run --name crane-db -e MYSQL_ROOT_PASSWORD=9ZmS353Kxf2rDd7KnHvHLmCsg -d mysql:latest

Metricas de Prometheus:
traefik_entrypoint_requests_total

Funciones de Crane:
1 - Recibe una imagen de docker y la despliega en un contenedor.

- El contenedor debera tener una imagen de docker, que debera estar disponible en el repositorio de docker.
- Para esta imagen crane debera crear un enrutador en la misma red, que permita el auto-escalamiento y el acceso al contenedor.
- Por defecto se utilizara una politica de autoescalado para el contenedor.
- Crane devolvera los datos de acceso al servicio que hayamos desplegado

2 - Crane monitorea en segundo plano los contenedores que administra.

- Si el contenedor tiene demasiada carga se debera evaluar la politica de auto escalamiento.
- Si un contenedor tiene una carga de transacciones muy baja se debera evaluar la politica de auto escalamiento.
- Si el contenedor tiene demasiado tiempo sin ser accedido se debera evaluar la politica de reciclaje.
- SI el contenedor tiene una falla se debera evaluar la politica de reintento.
