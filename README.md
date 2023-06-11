# Distributed Tag-Base System

## Description

Distributed Tag-Base System is a distributed system that allows users to store and retrieve files using tags. It is designed to be scalable, fault-tolerant, and highly available. The system is built using a peer-to-peer architecture, where each node in the network acts as both a client and a server. This allows for a decentralized system that can handle large amounts of data and traffic. The system is written in `Python` and is open-source, allowing for contributions from the community.

#### Architecture

The system consists of the following components:

- Nodes: Each node in the network is responsible for storing and serving files. Nodes communicate with each other to share information about the files they have and the tags associated with them.
- Client: The client is responsible for interacting with the user and sending requests to the nodes in the network. The client can upload, download, delete files, and search for files based on tags.
- Command Parser: The Command Parser is responsible for parsing the user's input and generating a command object that can be executed by the client.

#### Kademlia Protocol

The system uses the `Kademlia` protocol for peer-to-peer communication and distributed hash table (`DHT`) storage.

The `Kademlia` protocol is a distributed hash table protocol that allows nodes in a network to efficiently locate and retrieve data. It uses a binary tree structure to organize nodes in the network, with each node being responsible for a subset of the keyspace. Nodes communicate with each other to share information about the keys they are responsible for, allowing for efficient routing and lookup of data.

In the Distributed Tag-Base System, each node in the network uses the Kademlia protocol to store and retrieve files and their associated tags. When a file is uploaded to the network, it is hashed to generate a key, which is then used to determine which node in the network is responsible for storing the file. The node then stores the file and its associated tags in its local storage.

When a user searches for files based on tags, the client sends a request to one of the nodes in the network to search for files with the specified tag. The node then uses the `Kademlia` protocol to locate the nodes that are responsible for the keys associated with the tag. The node then sends requests to these nodes to retrieve the files and their associated tags. Once the files and tags have been retrieved, the node returns them to the client.


##### Fault Tolerance

The `Kademlia` protocol ensures fault tolerance in the Distributed Tag-Base System by allowing nodes to join and leave the network dynamically without affecting the overall system.

When a node joins the network, it contacts other nodes in the network to determine its position in the binary tree structure. The node then stores information about the other nodes it has contacted in its local storage. This information includes the node IDs, IP addresses, and port numbers of the other nodes.

When a node leaves the network, it contacts the other nodes it has stored in its local storage to inform them of its departure. The other nodes then update their routing tables to remove the departing node.

If a node fails or becomes unreachable, the other nodes in the network can still locate and retrieve data by using the `Kademlia` protocol to route around the failed node. When a node needs to locate a key that is not in its local storage, it sends a request to the node that is closest to the key. If that node is unreachable, the requesting node sends the request to the next closest node, and so on, until the key is found.

Fault tolerance is achieved by replicating files and their associated tags across multiple nodes in the network. This ensures that if a node fails or becomes unreachable, the files and tags can still be retrieved from other nodes in the network.

#### Data Flow:

- Files are uploaded to the nodes in the network and are stored in a distributed manner.
- Tags are associated with the files and are stored in a distributed manner.
- When a user searches for files based on tags, the client sends a request to one of the nodes in the network to search for files with the specified tag. The node then returns a list of files that match the tag.
- When a user downloads a file, the client sends a request to the node that has the file. The node then sends the file to the client.

#### Command Parser

The `CommandParser` class in `client.py` is responsible for parsing the user's input and generating a command object that can be executed by the client.

The `parse` method takes a string as input and returns a `Command` object. The `Command` object has two attributes: `name` and `args`. name is a string that represents the name of the command (e.g. "add", "delete", "list", etc.), and `args` is a dictionary that contains the arguments for the command.

The `parse` method first splits the input string into tokens using whitespace as the delimiter. It then checks if the first token is a valid command name. If it is, it sets the name attribute of the `Command` object to the command name. If it is not, it raises a `CommandError` exception.

The `parse` method then iterates over the remaining tokens and adds them to the `args` dictionary. The arguments are expected to be in the form "-arg value", where "-arg" is the name of the argument and "value" is the value of the argument. If an argument is not in this format, the `parse` method raises a `CommandError` exception.

Once all the arguments have been added to the args dictionary, the parse method returns the `Command` object.

## Used `Python` packages

- `pickle`
- `umgspack`
- `rpyc`
- `asyncio`

## Modos de uso

python3 client.py client-ip client-port bootstrap-routing-node-ip bootstrap-routing-port

`add -f file-list -t tag-list`

Copia uno o más ficheros hacia el sistema y estos son inscritos con las etiquetas contenidas en tag-list.

`delete -q tag-query`

Elimina todos los ficheros que cumplan con la consulta tag-query.

`list -q tag-query`

Lista el nombre y las etiquetas de todos los ficheros que cumplan con la consulta tag-query.

`add-tags -q tag-query -t tag-list`

Añade las etiquetas contenidas en tag-list a todos los ficheros que cumpan con la consulta tag-query.

`delete-tags -q tag-query -t tag-list`

Elimina las etiquetas contenidas en tag-list de todos los ficheros que cumplan con la consulta tag-query.

#### Funciones adicionales

`get -q tag-query`

Descarga todos los ficheros que cumplan con la consulta tag-query. Los ficheros seran almacenados en la carpeta 'secure' del Proyecto.
