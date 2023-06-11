import rpyc

def divide_file(file_path, chunk_size):
    """
    Divide un archivo en partes más pequeñas de tamaño fijo.

    Args:
        file_path (str): La ruta del archivo a dividir.
        chunk_size (int): El tamaño de cada parte en bytes.

    Returns:
        Una lista de rutas de archivo de las partes divididas.
    """
    parts = []
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_path = file_path + '?{}'.format(len(parts))
            with open(part_path, 'wb') as part:
                part.write(chunk)
            parts.append(part_path)
    return parts

def send_file_in_parts(ip, port, name):
    client_tcp = rpyc.connect(ip, port)
    parts = divide_file(name, 1024 * 1024)
    for part in parts:
        with open(part, "rb") as f:
            contents = f.read()
            client_tcp.root.fileWriter(contents, part, 'l')
    client_tcp.close()

async def send_file(ip, port, name):
    client_tcp = rpyc.connect(ip, port)

    with open(name, "rb") as f:
        contents = f.read()
        client_tcp.root.fileWriter(contents, name, 'l')
    client_tcp.close()

async def download(ip, port, name):
    client_tcp = rpyc.connect(ip, port)
    content = client_tcp.root.download(name)
    if content == 'NF':
        return False
    with open('probando_get/'+name, "wb") as f:
        f.write(content)  
    client_tcp.close()
    return True