import socket, os
import time, json
from datetime import datetime
import Server_folder.func_command_S as func


class Remote_Server():
	
	#Создание сервера 
	def __init__(self):		
	
		ip ='192.168.0.99'
		# ip = '127.0.0.1'
		port = 2027
		server_Remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print('Сервер ожидает подключения...')
		server_Remote.bind((ip, port))
		server_Remote.listen(1)
		self.connect_client_for_server(start_server=server_Remote)

	#Принятие запроса на подключение клиента к серверу
	def connect_client_for_server(self, start_server):
		while True:
			client_connect, client_addr = start_server.accept()
			self.control_entrance(server=start_server, connect=client_connect, address=client_addr)
			
	#Получаем имя пользователя и время входа клиента
	def control_entrance(self, server, connect, address):
		print(address)
		self.current_user = connect.recv(1024)
		self.current_user = self.current_user.decode()
		self.current_user = str(self.current_user)
		
		#Запись в файл json
		self.client_entrance = f'Вход клиента: {self.current_user}'
		client_json = {'1. Client entrance': self.client_entrance}
		self.rec_data_json(client_json)
		self.authorization(server = server, connect = connect)

		#Авторизация клиента
	def authorization(self, server, connect):
		
		time_connecting = datetime.now()
		full_time = time_connecting.strftime('%d.%m.%Y %H:%M:%S')
		full_time = str(full_time)
		print(full_time)

		login = (connect.recv(1024))
		login = login.decode()
		
		print(f'Логин клиента: {login}')
		password = connect.recv(1024)
		password = password.decode()
		print(f'Пароль клиента: {password}')
		right_password = '2637'

		if password == right_password:
			check_password = 'True'
			connect.send(check_password.encode())
			message_entrance = f'{full_time} Вход выполнен!'
			print(message_entrance)
			connect.send(message_entrance.encode())
			time.sleep(2)
			self.rec_data_json(message_entrance)
			self.control(server = server, connect = connect)
		else:
			check_password = 'False'
			connect.send(check_password.encode())
			error_entrance = f'{full_time} Вход не выполнен!!!'
			connect.send(error_entrance.encode())
			print(error_entrance)			
			time.sleep(2)
			self.rec_data_json(error_entrance)
			self.connect_client_for_server(start_server=server)
	
	#Принимаем команды управления
	def	control(self, server, connect):
		while True:
			command = connect.recv(1024)
			command = command.decode()

    	    #Информация о системе
			if command == 'system_info':
				sys_info = func.system_info(conn = connect)
				#Запись в файл json 
				client_json = {'conclusion_command': sys_info}
				self.rec_data_json(client_json)
				
			#Информация о HDD
			if command == 'hdd_info':
				message_HDD = func.info_HDD(conn = connect)
				client_json = {'conclusion_command': message_HDD}
				self.rec_data_json(client_json)

			#Информация о температуре железа
			if command == 'hardware_monitor':		
				message_monitor = func.hardware_mon(conn = connect)
				#Запись в файл json
				client_json = {'conclusion_command': message_monitor}
				self.rec_data_json(client_json)

			if command == 'file_size':
				size_file = func.get_file_size(conn = connect)
				#Запись в файл json
				client_json = {'conclusion_command': size_file}
				self.rec_data_json(client_json)

			#Открытие папки
			if command == 'ls':				
				way_info = func.open_directory(conn = connect)
				#Запись в файл json 
				client_json = {'conclusion_command': way_info}
				self.rec_data_json(client_json)
				self.connect_client_for_server(start_server = server)

			#Получение директории сервера
			if command == "current_dir":
				info_file = func.current_directory(conn = connect)
				#Запись в файл json 
				client_json = {'conclusion_command': info_file}
				self.rec_data_json(client_json)

			#Запуск файла на сервере
			if command == 'start_file':				
				info_file = func.launch_file(conn = connect)
				#Запись в файл json 
				client_json = {'conclusion_command': info_file}
				self.rec_data_json(client_json)

			#Создание папки
			if command == 'create_folder':
				message_info = func.create_folder(conn = connect)
				#Запись в файл json 
				client_json = {'conclusion_command': message_info}
				self.rec_data_json(client_json)

			#Создание папки
			if command == 'create_folder':
				message_info = func.create_folder(conn = connect)
				#Запись в файл json 
				client_json = {'conclusion_command': message_info}
				self.rec_data_json(client_json)

			#Скачивание файла клиентом				
			if command == "download":
				file_info = func.download_file(conn = connect)				
				#Запись в файл json 
				client_json = {'conclusion_command': file_info}
				self.rec_data_json(client_json)
				self.connect_client_for_server(start_server = server)

			#Загрузка файла на сервер
			if command == 'load':
				file_info = func.load_file(conn = connect)
				#Запись в файл json 
				client_json = {'conclusion_command': file_info}
				self.rec_data_json(client_json)
				self.connect_client_for_server(start_server = server)

			#Отключение клиента
			if command == 'exit':
				time_connecting = datetime.now()
				full_time = time_connecting.strftime('%d.%m.%Y %H:%M:%S')
				full_time = str(full_time)
				self.info_exit = f'{full_time} Клиент {self.current_user} отключился от сервера!'
				print(self.info_exit)
				#Запись в файл json 
				client_json = {'conclusion_command': self.info_exit}
				self.rec_data_json(client_json)
				connect.close()
				self.serverClear()
				time.sleep(1)
				self.connect_client_for_server(start_server=server)

	#Запись в файл json 		
	def rec_data_json(self, text_data):
		self.save_data_json()
		with open('data_server.json','a', encoding = 'utf-8') as data:
			data.write(json.dumps(text_data,indent = 4,ensure_ascii = False ))
				
	#Запись данных в json файл
	def save_data_json(self):
		dict_data_client = { 
		}
		with open('data_server.json','a', encoding='utf-8') as data:
			data.write(json.dumps(dict_data_client, indent=4,ensure_ascii = False))

	#Очистка консоли сервера
	def serverClear(self):return os.system('clear')

	
#Сервер должен дать доступ к своему хранилищу(к дискам)
if __name__=='__main__':
	Remote_Server()