# Script 2: Receives data from port 5000 using the python script osc_server.
from pythonosc import dispatcher
from pythonosc import osc_server
import threading

ip = "127.0.0.1"
port = 5000

def receive_data(portnum):
  """Receives data from port 5000.

  Args:
    port: The port to receive the data from.
    
  """
  

  

def handle_test(address, args, types):
  print(args[0])

if __name__ == "__main__":

  thread = threading.Thread(target=receive_data, args=(port,))
  thread.daemon = True
  thread.start()
  dispatcher = dispatcher.Dispatcher()

  server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
  dispatcher.map("/test", handle_test)

  while True:
    server.handle_request()

receive_data(port)
