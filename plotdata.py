

##plot data##



if __name__ == "__main__":
    thread = threading.Thread(target=init_plot)
    thread.daemon = True
    thread.start()

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Listening on UDP port "+str(port))
server.serve_forever()