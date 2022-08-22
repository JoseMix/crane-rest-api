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


  bec2527dd8373c3a17e11e482201fc411641f3e0101a910cc5e5a52247518924  
  22b008bac0e45a7e918d211d275b69eec7914de779847af48b69fce01eebc224

  pg: 9a0e750f2bfddb15ef109c0543a7cf7fc9aa7fd41f705b01d15cadc988c53184
