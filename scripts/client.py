import socket
from distutils.util import strtobool


N = 256

def communication(ip,data):
    ###接続処理
	port = 8000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))
	###送信
	senddata = str(data[0]) + "," + str(data[1]) + "," +str(int(data[2])) + "," + str(data[3])
	try:
		s.send(senddata.encode("utf-8"))
	except:
		pass
	###受信
	data = s.recv(N)
	###受信データ変換
	temp = data.decode("utf-8")
	temp = temp.split(",")
	print(data)
	try:
		read=[int(temp[0]),int(temp[1]),strtobool(temp[2]),int(temp[3])]
	except:
		read=[0,200,False]
	return read




