import rpyc
import os 

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


async def send_file(ip, port, name, tag, value):
    finished = False
    client_tcp = rpyc.connect(ip, port)
    with open(name, "rb") as f:
        contents = f.read()
        client_tcp.root.fileWriter(contents, name, tag, value)
        finished = True
    client_tcp.close()
    return finished


async def download(ip, port, name, value):
    client_tcp = rpyc.connect(ip, port)
    content = client_tcp.root.download(name, value)
    if content == 'NF':
        return False
    ################################################
    f = os.listdir("download")
    if any(name in filenames for filenames in f):  
        i = 1
        while True:
            new_name = name.split('.')[0] + str(i) + '.' + name.split('.')[1]
            if not any(new_name in filenames for filenames in f): 
                name = new_name
                break
            i += 1


    ################################################
    with open('download/'+name, "wb") as f:
        f.write(content)  
    client_tcp.close()
    return True

async def delete_file(ip, port, name, value):
    client_tcp = rpyc.connect(ip, port)
    client_tcp.root.delete(name, value)
    client_tcp.close()
