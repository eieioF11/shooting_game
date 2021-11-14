import socket
import threading
import sys

global first
first=True
global save_id
save_id=0
###ID判定関数
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
resive1 = "0,200,0".encode("utf-8")
resive2 = "0,200,0".encode("utf-8")
###クライアント接続時の処理
def send_data(client, clientno):
	global resive1
	global resive2
	###データの受信
	resive = client.recv(N)
	temp = resive.decode("utf-8")
	temp = temp.split(",")
	print(resive)
	temp = int(temp[0])
	print(temp)
	###IDの判定
	if identification(temp):
		resive1 = resive
		client.send(resive2)#データ送信
	else:
		resive2 = resive
		client.send(resive1)#データ送信
	print(resive1,resive2)
	client.close()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("",PORT))
server.listen(0)

while True:
	host = socket.gethostname()
	myip = socket.gethostbyname(host)
	print(myip)
	client, addr = server.accept()
	p = threading.Thread(target = send_data, args = (client, clientno))
	try:
		p.start()
	except KeyboardInterrupt:
		p.exit()
		server.close()
		sys.exit(1)
