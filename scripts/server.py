import socket
import threading
import time

global first
first=True
global save_id
save_id=0
def identification(id):
	global first
	global save_id
	if first:
		save_id=id
		first=False
		return True
	if id==save_id:
		return True
	return False


PORT = 8000
N = 256
clientno = 0
global resive1
global resive2
resive1 = "0,200,False".encode("utf-8")
resive2 = "0,200,False".encode("utf-8")

def send_data(client, clientno):
	global resive1
	global resive2
	resive = client.recv(N)
	temp = resive.decode("utf-8")
	temp = temp.split(",")
	print(resive)
	temp = int(temp[0])
	print(temp)
	if identification(temp):
		resive1 = resive
		client.send(resive2)#データ送信
	else:
		resive2 = resive
		client.send(resive1)
	print(resive1,resive2)
	client.close()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("",PORT))
server.listen(0)

while True:
	client, addr = server.accept()
	p = threading.Thread(target = send_data, args = (client, clientno))
	p.start()
