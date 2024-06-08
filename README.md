## CRANE: despliegue de aplicaciones contenerizadas en entornos locales

CRANE es una herramienta diseñada para el despliegue local de aplicaciones en contenedores, enfocada en simplificar las pruebas de entornos distribuidos de forma local. CRANE ofrece una solución liviana y de propósito general con capacidades de ruteo, escalado y monitoreo automático. Orientada a estudiantes, docentes y
desarrolladores que necesiten crear y desplegar servicios en contenedores simulando las características básicas que ofrece un entorno cloud de plataforma como servicio (PaaS).

### Características
- Desplegar imágenes a través de API REST diseñada con Python Fast API.
- Monitoreo y Alertado automático utilizando Prometheus y AlertManager.
- Evaluación de políticas de seguridad y escalado utilizando Open Policy Agent.
- Modelo RBAC para la autenticación y autorización.
- Documentación con Swagger OPEN API.


## 🔗 Videos demostrativos
[DEMO 1: INICIO DE CRANE](https://drive.google.com/file/d/12CNwgmc6HoB1oHBe1uoRmNLRs5ddVTOT/view?usp=sharing)

[DEMO 2: CREAR SERVICIO](https://drive.google.com/file/d/1nvo89CqVDqeXvcTlSXZMz-S5fEIWKCk4/view?usp=sharing)

[DEMO 3: AUTO START DE SERVICIO CAIDO](https://drive.google.com/file/d/1VmrdGA-yz6MwEoNjJf-bVAl4F5pG8qeE/view?usp=sharing)

[DEMO 4: ESCALAMIENTO AUTOMATICO](https://drive.google.com/file/d/1jVokt9Al6N15-3VulOaImbHSVAw03kRh/view?usp=sharing)

[DEMO 5: DESESCALAMIENTO AUTOMATICO](https://drive.google.com/file/d/1CuHOBBpaTs90n10xcEKRHGu6lekBxtEc/view?usp=sharing)
### Se encuentra a su disposición la colección de Postman en el repositorio


### Requisitos
```
pip install -r requirements.txt
uvicorn app:app --reload
```
#### Importante: El docker daemon debe estar iniciado, de lo contrario recibiremos una advertencia y el servidor no se iniciará.


### Documentación de la API
```http://localhost:8000/docs```


### Endpoint de Prometheus:
```http://localhost:9090```


### Endpoint de AlertManager:
```http://localhost:9093```


### Registro
```
curl --location 'http://localhost:8000/api/v1/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "full_name": "Franco Bellino",
    "email": "franco@gmail.com",
    "password": "123456"
}'
```


### Login
```
curl --location 'http://localhost:8000/api/v1/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "franco@gmail.com",
    "password": "123456"
}'
```


### Desplegar mi primer servicio


```
curl --location 'http://localhost:8000/api/v1/apps' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6ImZyYW5jb0BnbWFpbC5jb20iLCJyb2xlcyI6WyJBRE1JTiJdfQ.QkZ8W1uxFQ9CWIgo1YFCJaOC-2-2C7J4zrPSsZhVfBM' \
--data '{
    "name": "prueba_demo_crane",
    "services": [
        {
            "name": "whoami",
            "image": "traefik/whoami",
            "networks": [
                "crane-net"
            ]
        }
    ]
}'
```
