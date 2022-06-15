# CRANE: despliegue inteligente de contenedores

Funciones de Crane:
1 - Recibe una imagen de docker y la despliega en un contenedor.
  - El contenedor debera tener una imagen de docker, que debera estar disponible en el repositorio de docker.
  - Para esta imagen crane debera crear un enrutador en la misma red, que permita el auto-escalamiento y el acceso al contenedor.
  - Por defecto se utilizara una politica de autoescalado para el contenedor.
  - Crane devolvera los datos de acceso al servicio que hayamos desplegado

2 - Crane monitorea en segundo plano los contenedores que administra.
  - Si el contenedor tiene demasiada carga la politica de auto escalamiento.
  - Si un contenedor tiene una carga de transacciones muy baja se debera evaluar la politica de auto escalamiento.
  - Si el contenedor tiene demasiado tiempo sin ser accedido se debera evaluar la politica de reciclaje.
  - SI el contenedor tiene una falla se debera evaluar la politica de reintento.  
  
