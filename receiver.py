import socket,cv2, pickle,struct, time
import threading
# create socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#  server ip address here
def connect_server():
	time.sleep(15)
	host_ip = '192.168.99.1' 
	port = 9999
	s.connect((host_ip,port)) 
	data = b""
	metadata_size = struct.calcsize("Q")
	while True:
		while len(data) < metadata_size:
			packet = s.recv(4*1024) 
			if not packet: break
			data+=packet
		packed_msg_size = data[:metadata_size]
		data = data[metadata_size:]
		msg_size = struct.unpack("Q",packed_msg_size)[0]
	
		while len(data) < msg_size:
			data += s.recv(4*1024)
		frame_data = data[:msg_size]
		data  = data[msg_size:]
		frame = pickle.loads(frame_data)
		cv2.imshow("RECEIVING VIDEO",frame)
		key = cv2.waitKey(10) 
		if key  == 13:
			break
	s.close()

def sender():
	host_name  = socket.gethostname()
	host_ip = socket.gethostbyname(host_name)
	print('HOST IP:',host_ip)
	port = 1234
	socket_address = (host_ip,port)
	# Socket Bind
	s.bind(socket_address)
	# Socket Listen
	s.listen(5)
	print("LISTENING AT:",socket_address)
	while True:
		client_socket,addr = s.accept()
		print('GOT CONNECTION FROM:',addr)
		if client_socket:
			vid = cv2.VideoCapture(1)
		
			while(vid.isOpened()):
				ret,image = vid.read()
				img_serialize = pickle.dumps(image)
				message = struct.pack("Q",len(img_serialize))+img_serialize
				client_socket.sendall(message)
			
				cv2.imshow('VIDEO FROM SERVER',image)
				key = cv2.waitKey(10) 
				if key ==13:
					client_socket.close()


x1 = threading.Thread(target=connect_server)
x2 = threading.Thread(target=sender)


x1.start()
x2.start()