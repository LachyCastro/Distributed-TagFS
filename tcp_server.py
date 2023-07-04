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
  
    # def exposed_fileWriter(self, contents, filename, username):
    #     #print(contents,flush=True)
    #     f = os.listdir("secure")
    #     # Verifying if files with the same name exist and giving it a new name
    #     if any(filename in filenames for filenames in f):   
    #         # k = open("secure/new"+filename, "wb")
    #         # if k.mode == "wb":
    #         #     k.write(contents)
    #         #     print("\nThe file '"+filename+"' from "+username+" has been transmitted to the SERVER successfully!\n",flush=True)
    #         # k.close()
    #         pass
    #     else:
    #         k = open("secure/"+filename, "wb")
    #         if k.mode == "wb":
    #             k.write(contents)
    #             print("\nThe file '"+filename+"' from "+username+" has been transmitted to the SERVER successfully!\n",flush=True)
    #         k.close()
    
    # def exposed_download(self, fname):
    #   file_path = os.path.join("secure", fname)
    #   try:
    #       with open(file_path, "rb") as f:
    #           contents = f.read()
    #           return contents
    #   except IOError:
    #       return b"NF"

    # def exposed_disp_list(self):
    #     return os.listdir("secure")
    
    # def exposed_delete(self, fname):
    #     try:
    #         os.remove("secure/"+fname)
    #     except:
    #         pass
    def exposed_fileWriter(self, contents, filename, username, value):
        #print(contents,flush=True)
        f = os.listdir("secure")
        # Verifying if files with the same name exist and giving it a new name
        if any(value + '|' +filename in filenames for filenames in f):   
            # k = open("secure/new"+filename, "wb")
            # if k.mode == "wb":
            #     k.write(contents)
            #     print("\nThe file '"+filename+"' from "+username+" has been transmitted to the SERVER successfully!\n",flush=True)
            # k.close()
            pass
        else:
            k = open("secure/"+ value + '|' + filename, "wb")
            if k.mode == "wb":
                k.write(contents)
                print("\nThe file '"+filename+"' from "+username+" has been transmitted to the SERVER successfully!\n",flush=True)
            k.close()
        #load json
        try:
            with open("secure/state.json", "r") as f:
                data_dict = json.load(f)
            try:
                if not username in data_dict[filename]:
                    data_dict[filename].append(username)
            except:
                data_dict[filename] = [username]
            #update json
            with open("secure/state.json", "w") as f:
                json.dump(data_dict, f)
        except:
            data_dict = {}
            data_dict[filename] = [username]
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
            os.remove("secure/"+value + '|' + fname)
        except:
            pass
  

if __name__ == "__main__":
    # Create a Secure folder which can only be accessed by the Server
    if not os.path.isdir("secure/"):
        os.mkdir("secure", 0o700)
        print("\nSecure Folder Created!\n")
    t = ThreadedServer(Service, hostname= sys.argv[1], port=sys.argv[2])
    t.start()