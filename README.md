# CRANE: despliegue inteligente de contenedores

CRANE es una herramienta diseñada para el despliegue local de aplicaciones en contenedores, enfocada en simplificar las pruebas de entornos distribuidos de forma local. CRANE ofrece una solución liviana y de propósito general con capacidades de ruteo, escalado y monitoreo automático. Orientada a estudiantes, docentes y
desarrolladores que necesiten crear y desplegar servicios en contenedores simulando las características básicas que ofrece un entorno cloud de plataforma como servicio (PaaS).

## Requisitos
```
pip install -r requirements.txt
uvicorn app:app --reload
```
### Importante: El docker daemon debe estar iniciado, de lo contrario recibiremos una advertencia y el servidor no se iniciará.

## Endpoints de la API REST
```http://localhost:8000/docs```

## Endpoint de Prometheus:
```http://localhost:9090/```

## Endpoint de AlertManager:
```http://localhost:9093/```

