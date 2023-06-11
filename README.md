# Distributed Tag-Base System

## Descripción

El Sistema de Ficheros con Etiquetas Distribuido es un sistema distribuido que permite a los usuarios almacenar y recuperar archivos utilizando etiquetas. Está diseñado para ser escalable y tolerante a fallos. El sistema está construido utilizando una arquitectura peer-to-peer, donde cada nodo en la red actúa como cliente y servidor. Esto permite un sistema descentralizado que puede manejar grandes cantidades de datos y tráfico. El sistema está escrito en `Python` y es de código abierto, lo que permite contribuciones de la comunidad.

#### Arquitectura

El sistema consta de los siguientes componentes:

- Nodos: Cada nodo en la red es responsable de almacenar y brindar archivos. Los nodos se comunican entre sí para compartir información sobre los archivos que tienen y las etiquetas asociadas con ellos.
- Cliente: El cliente es responsable de interactuar con el usuario y enviar solicitudes a los nodos en la red. El cliente puede cargar, descargar, eliminar y buscar archivos según etiquetas.
- Parser de comandos: Es responsable de analizar la entrada del usuario y generar un comando que puede ser ejecutado por el cliente.

#### Protocolo Kademlia

El sistema utiliza el protocolo `Kademlia` para comunicación peer-to-peer y almacenamiento de tabla hash distribuida (`DHT`).

El protocolo `Kademlia` es un protocolo de tabla hash distribuida que permite a los nodos en una red localizar y recuperar datos de manera eficiente. Utiliza una estructura de árbol binario para organizar los nodos en la red, donde cada nodo es responsable de un subconjunto del espacio de ficheros. Los nodos se comunican entre sí para compartir información sobre las llaves de las que son responsables, lo que permite el enrutamiento y búsqueda eficientes de datos.

En el Sistema de Etiquetas Distribuido, cada nodo en la red utiliza el protocolo Kademlia para almacenar y recuperar archivos y sus etiquetas asociadas. Cuando se carga un archivo en la red, se genera una clave hash, que luego se utiliza para determinar qué nodo en la red es responsable de almacenar el archivo. El nodo almacena el archivo y sus etiquetas asociadas en su almacenamiento local.

Cuando un usuario busca archivos según etiquetas, el cliente envía una solicitud a uno de los nodos en la red para buscar archivos con la etiqueta especificada. El nodo luego utiliza el protocolo `Kademlia` para localizar los nodos que son responsables de las claves asociadas con la etiqueta. El nodo luego envía solicitudes a estos nodos para recuperar los archivos y sus etiquetas asociadas. Una vez que se han recuperado los archivos y las etiquetas, el nodo los envía al cliente.

##### Tolerancia a fallos

El protocolo `Kademlia` asegura la tolerancia a fallos al permitir que los nodos se unan y abandonen la red de manera dinámica sin afectar el sistema en general.

Cuando un nodo se une a la red, contacta a otros nodos en la red para determinar su posición en la estructura de árbol binario. Luego, el nodo almacena información sobre los otros nodos que ha contactado en su almacenamiento local. Esta información incluye los IDs de nodo, las direcciones IP y los números de puerto de los otros nodos.

Cuando un nodo abandona la red, se comunica con los otros nodos que ha almacenado en su almacenamiento local para informarles de su partida. Los otros nodos luego actualizan sus tablas de enrutamiento para eliminar el nodo que se va.

Si un nodo falla o se vuelve inaccesible, los otros nodos en la red aún pueden localizar y recuperar datos utilizando el protocolo `Kademlia` para enrutar alrededor del nodo fallido. Cuando un nodo necesita localizar una clave que no está en su almacenamiento local, envía una solicitud al nodo que está más cerca de la clave. Si ese nodo no es accesible, el nodo solicitante envía la solicitud al siguiente nodo más cercano, y así sucesivamente, hasta que se encuentra la clave.

La tolerancia a fallos se logra mediante la replicación de archivos y sus etiquetas asociadas en varios nodos en la red. Esto asegura que si un nodo falla o se vuelve inaccesible, los archivos y etiquetas aún pueden ser recuperados de otros nodos en la red.

#### Flujo de datos:

- Los archivos se cargan en los nodos de la red y se almacenan de manera distribuida.
- Las etiquetas se asocian con los archivos y se almacenan de manera distribuida.
- Cuando un usuario busca archivos según etiquetas, el cliente envía una solicitud a uno de los nodos en la red para buscar archivos con la etiqueta especificada. El nodo luego devuelve una lista de archivos que coinciden con la etiqueta.
- Cuando un usuario descarga un archivo, el cliente envía una solicitud al nodo que tiene el archivo. El nodo luego envía el archivo al cliente.

#### Lenguaje de Comandos

La clase `CommandParser` en `client.py` es responsable de analizar la entrada del usuario y generar un comando que puede ser ejecutado por el cliente.

El método `parse` recibe una cadena como entrada y devuelve un objeto `Command`. El objeto `Command` tiene dos atributos: `name` y `args`. `name` es una cadena que representa el nombre del comando (por ejemplo, "add", "delete", "list", etc.), y `args` es un diccionario que contiene los argumentos del comando.

El método `parse` primero divide la cadena de entrada en tokens usando el espacio en blanco como delimitador. Luego verifica si el primer token es un nombre de comando válido. Si lo es, establece el atributo `name` del objeto `Command` en el nombre del comando. Si no lo es, genera una excepción.

El método `parse` luego itera sobre los tokens restantes y los agrega al diccionario `args`. Se espera que los argumentos estén en la forma "-arg value", donde "-arg" es el nombre del argumento y "value" es el valor del argumento.

Una vez que se han agregado todos los argumentos al diccionario `args`, el método `parse` devuelve la instrucción.

## Instalación

### Paquetes de `Python` utilizados

- `pickle`
- `umgspack`
- `rpyc`
- `asyncio`