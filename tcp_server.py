import rpyc
import os
from rpyc.utils.server import ThreadedServer
import sys
import json

class Service(rpyc.Service):
    def on_connect(self, conn):
        print("Someone joined!",flush=True)
    
    def on_disconnect(self, conn):
        print("Someone left!", flush=True)
  
    def exposed_fileWriter(self, contents, filename, tag, value):
        name = value + '|' + filename
        f = os.listdir("secure")
        # Verifying if files with the same name exist and giving it a new name
        if any(name in filenames for filenames in f):   
            pass
        else:
            k = open("secure/"+ name, "wb")
            if k.mode == "wb":
                k.write(contents)
                print("\nThe file '"+filename+"' from "+tag+" has been transmitted to the SERVER successfully!\n",flush=True)
            k.close()
        #load json
        try:
            with open("secure/state.json", "r") as f:
                data_dict = json.load(f)
            try:
                if not tag in data_dict[name]:
                    data_dict[name].append(tag)
            except:
                data_dict[name] = [tag]
            #update json
            with open("secure/state.json", "w") as f:
                json.dump(data_dict, f)
        except:
            data_dict = {}
            data_dict[name] = [tag]
            with open("secure/state.json", "w") as f:
                json.dump(data_dict, f)
        
        
    def exposed_download(self, fname, value):
      file_path = os.path.join("secure", value + '|'+ fname)
      try:
          with open(file_path, "rb") as f:
              contents = f.read()
              return contents
      except IOError:
          return b"NF"

    def exposed_disp_list(self):
        return os.listdir("secure")
    
    def exposed_delete(self, fname, value):
        try:
            os.remove("secure/"+ value + '|' + fname)
        except:
            pass
    
    def exposed_delete_tag(self, tags, fname, value):
        try:
            with open("secure/state.json", "r") as f:
                data_dict = json.load(f)
            if value + '|' + fname in data_dict.keys():
                data_dict[value + '|' + fname] = [tag for tag in data_dict[value + '|' + fname] if tag not in tags]
            with open("secure/state.json", "w") as f:
                json.dump(data_dict, f)
        except:
            pass

if __name__ == "__main__":
    # Create a Secure folder which can only be accessed by the Server
    if not os.path.isdir("secure/"):
        os.mkdir("secure", 0o700)
        print("\nSecure Folder Created!\n")
    if not os.path.isdir("download/"):
        os.mkdir("download", 0o700)
        print("\nDownload Folder Created!\n")
    t = ThreadedServer(Service, hostname= sys.argv[1], port=sys.argv[2])
    t.start()