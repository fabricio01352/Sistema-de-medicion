# Sistema-de-medicion
Este sistema tiene como proposito medir masas grandes (carros) mediante sensores infrarrojos de barrera para determinar entradas y salidas de carros de un negocio de detallado automotriz. El empresario podra ver la cantidad real de clientes que tiene. El sistema sera escalable y modular para cambiar los sensores por un lazo conductivo en un futuro, sin afectar el sistema. 

El sistema se encuentra aun en progreso y el ultimo commit es el programa terminado pero con restricciones: El sensor es ultrasonico, solo se envian reportes en PDF al whatsapp del usuario (no existe dashboard), no se crean reportes ni estadisticas, el prototipo del circuito PCB y de la carcasa IP44 probablemente no se terminaran pronto, y hacen falta mejoras en el codigo, sin embargo por temas de tiempo, el sistema se usara como esta, ya que es bastante funcional y cumple con las expectativas.


**Arquitectura sencilla de cliente servidor. Se utiliza protocolo de comunicacion estandar TCP/IP con mensajeria por broker por MQTT, con la opcion de escalarlo y agregar mas modulos e intercomunicarlos mediante UART
**
ESP 32 CLIENTE -> LECTURA DE DATOS -> BACKEND -> BASE DE DATOS 


La administracion se hara mediante un tablero sencillo Kanban en Jira



<img width="796" height="597" alt="Diagrama en blanco (5)" src="https://github.com/user-attachments/assets/d2616ef0-82f3-4123-97d1-bb4d511c7b3d" />
<img width="2060" height="520" alt="Diagrama en blanco (4)" src="https://github.com/user-attachments/assets/c66fe4ca-07d3-4276-a5e3-ff3f21fc173c" />
