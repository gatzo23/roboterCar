import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = "192.168.178.91"
while 1:
    data = input("Enter Data :")
# IPADRESS = RPi IP address
# 6666 = Number Port
    client_socket.sendto(data.encode(), (UDP_IP,6666))
    print ("Sending request")
    if data == "q":
        break

client_socket.close()