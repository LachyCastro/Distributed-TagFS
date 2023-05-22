# Informe

## RPCProtocol

La clase llamada `RPCProtocol` implementa un protocolo de red para la comunicación entre procesos usando datagramas UDP. Este protocolo utiliza el formato de serialización `msgpack` para codificar los mensajes y utiliza `asyncio` para manejar el envío y la recepción de forma asincrónica.

El protocolo define dos tipos de mensajes: solicitudes y respuestas. Las solicitudes se identifican con el primer byte `b'\x00'` y las respuestas se identifican con el primer byte `b'\x01'`. Cada mensaje contiene un ID de mensaje de 20 bytes generado aleatoriamente y un cuerpo de mensaje codificado en `msgpack`.

La clase `RPCProtocol` define tres métodos principales para manejar los mensajes: `datagram_received()`, `_accept_request()` y `_accept_response()`. El método `datagram_received()` se llama cuando se recibe un datagrama UDP y se encarga de llamar a `_solve_datagram()` de forma asincrónica para procesar el datagrama.

El método `_solve_datagram()` es el que se encarga de interpretar el mensaje recibido y determinar si es una solicitud o una respuesta. Si es una solicitud, se llama al método correspondiente en la instancia de RPCProtocol para procesar la solicitud. Si es una respuesta, se recupera el ID de mensaje correspondiente y se busca en un diccionario de mensajes pendientes para encontrar la solicitud original y completar su resultado.

El método `_accept_request()` se encarga de procesar una solicitud. Verifica si la solicitud es válida, llama al método correspondiente en la instancia de `RPCProtocol` para procesar la solicitud y envía la respuesta al remitente.

El método `_accept_response()` se encarga de procesar una respuesta. Verifica si la respuesta es válida y completa la solicitud pendiente correspondiente.

## Crawling

`SpiderCrawl` es la clase base y define el comportamiento general de un rastreador que se utiliza para buscar nodos en la red. La clase implementa un algoritmo para buscar nodos cercanos a un nodo dado, que se basa en el algoritmo de búsqueda de proximidad de Kademlia.

`ValueSpiderCrawl` es una clase que hereda de `SpiderCrawl`. Se utiliza para buscar un valor asociado con una clave en la red. El algoritmo es similar al algoritmo de búsqueda de proximidad de Kademlia, pero en lugar de buscar nodos cercanos a una clave, busca valores asociados a esta.

`NodeSpiderCrawl` hereda de `SpiderCrawl`  también, y se utiliza para buscar nodos en la red. Análogamente con `ValueSpiderCrawl`, es un algoritmo similar al algoritmo de búsqueda de proximidad de Kademlia, pero en lugar de buscar valores asociados a una clave, busca nodos cercanos a esta clave.

La clase `RPCFindResponse` se utiliza para representar la respuesta de una búsqueda en la red. Es la que permite a las clases que heredan de `SpiderCrawl` determinar si la búsqueda tuvo éxito y recuperar los valores o nodos encontrados, según cada caso.
