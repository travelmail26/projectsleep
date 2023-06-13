import socket

def send_data(data, address, port):
  """Sends data to the other script.

  Args:
    data: The data to send.
    address: The address of the other script.
    port: The port of the other script.

  """

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((address, port))
    s.sendall(data)

def check_address_and_port(address, port):
  """Checks whether the address and port are listening.

  Args:
    address: The address to check.
    port: The port to check.

  Returns:
    True if the address and port are listening, False otherwise.

  """

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
      s.connect((address, port))
      return True
    except socket.error:
      return False

if __name__ == "__main__":
  data = "Hello, world!"
  address = "127.0.0.1"
  port = 5000

  if check_address_and_port(address, port):
    send_data(data, address, port)
  else:
    print("The address and port are not listening.")
