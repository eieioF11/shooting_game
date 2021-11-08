import socket


N = 256
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(ip):
	port = 8000
	s.connect((ip, port))

def communication(data):
	senddata = str(data[0]) + "," + str(data[1]) + "," +str(data[2])
	s.send(senddata.encode("utf-8"))
	data = s.recv(N)
	temp = data.decode("utf-8")
	temp = temp.split(",")
	print(data)
	read=[int(temp[0]),int(temp[1]),bool(temp[2])]
	return read




