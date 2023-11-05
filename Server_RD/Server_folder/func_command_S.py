import subprocess, os, cpuinfo
import psutil, platform, json
import time



#Открытие папки 
def open_directory(conn):
	way_search = (conn.recv(1024)).decode()

	#Проверка на наличие директрории
	if os.path.isdir(way_search) == True:
		error_dir = 'True'
		conn.send(error_dir.encode())
		file_list = os.listdir(way_search)
		direct_info = f'Клиент просматривает директорию {way_search}'
		print(direct_info)
		file_list = str(file_list)
		print(file_list)
		conn.send(file_list.encode())
		time.sleep(1)
		conn.close()
		return direct_info
	else:
		error_dir = 'False'
		conn.send(error_dir.encode())
		error_way = f'Путь директории {way_search} не найден!'
		print(error_way)
		conn.send(error_way.encode())
		time.sleep(1)
		conn.close()
		print("Переподключение") 
		return error_way

#Информация о CPU и его температуре
def hardware_temp():
	pass

def current_directory(conn): 
	current = os.getcwd()
	conn.send(current.encode())
	info_message = 'Клиент запросил расположение сервера'
	print(info_message)
	return info_message

#Запуск файла на сервере
def launch_file(conn):
	start_file = (conn.recv(1024)).decode()	
	print(start_file)
	if os.path.isfile(start_file) == True:
		error_start_file = "True"
		conn.send(error_start_file.encode())
		os.startfile(start_file)
		print('Запуск: ',start_file)
		message_file = f'Файл: {start_file} запущен'
		conn.send(message_file.encode())
		return message_file
	else:
		error_start_file = "False"
		conn.send(error_start_file.encode())
		error_start = f'Файл {start_file} не найден'
		print(error_start)
		conn.send(error_start.encode())
		return error_start
	
#Создание папки
def create_folder(conn):
	way_dict_fold = (conn.recv(1024)).decode()
	if os.path.isdir(way_dict_fold):
		check_dict = 'True'
		conn.send(check_dict.encode())
		create_folder = (conn.recv(1024)).decode()
		check_folder = f'{way_dict_fold}\{create_folder}'
		os.mkdir(check_folder)					
		folder_dict = f'Папка создана! Путь: {check_folder}'
		conn.send(folder_dict.encode())
		message_folder = f'Клиент создал папку! Путь {check_folder}'
		print(message_folder)
		return message_folder
	else:
		check_dict = 'False'
		conn.send(check_dict.encode())
		message_error = f'Директория не найдена! {way_dict_fold}'
		conn.send(message_error.encode())
		print(message_error)
		return message_error
	
#Информация о системе
def system_info(conn):
	system = system_Info()
	system = str(system)
	message_system_info = 'Клиент запросил информацию о системе!'
	print(message_system_info)
	conn.send(system.encode())
	console_command = {'Вывод информации на консоль сервера': message_system_info}
	return console_command

#Информация о HDD
def info_HDD(conn):
	hdd = HDD_info()
	hdd = str(hdd)
	conn.send(hdd.encode())
	message_HDD = 'Клиент запросил информацию о HDD!'
	print(message_HDD)	
	return message_HDD			

def hardware_mon(conn):
	cpu_mon = cpu_temp()
	print(cpu_mon)
	cpu_mon =  str(cpu_mon)
	conn.send(cpu_mon.encode())
	#Запись в файл json 
	message_cpu = 'Клиент запросил информацию о процессоре и температуре!'
	print(message_cpu)
	return message_cpu			

#Температура процессора(Линукс)
def cpu_temp():
	temp = psutil.sensors_temperatures()
	return temp

#Температура о HDD
def hdd_temp():
	process = subprocess.Popen(["sensors"],shell=False)
	data = process.communicate()
	temp = int(data[0].split()[5][1:3])
	return temp

#Информация о системе
def system_Info():
	cpu = cpuinfo.get_cpu_info()['brand_raw']
	return (cpu, platform.machine(), platform.node(), platform.processor(), platform.system(), platform.version())

#Информация о HDD
def HDD_info():
	partitions = psutil.disk_partitions()
	list_disk_info =[]
	for partition in partitions:
		try:
			partition_usage = psutil.disk_usage(partition.mountpoint)
		except PermissionError:
			continue
		hdd = (f"=== Device: {partition.device} ===, Mountpoint: {partition.mountpoint}, File system type: {partition.fstype}, Total size: {get_size(partition_usage.total)}, Used: {get_size(partition_usage.used)}, Free: {get_size(partition_usage.free)}")
		list_disk_info.append(hdd)
	hdd_info = json.dumps(list_disk_info)
	return hdd_info

def get_file_size(conn):
	file_size = (conn.recv(1024)).decode()
	if os.path.isfile(file_size):#True
		size = os.path.getsize(file_size)/1024
		conn.send(f'{(size:=str(size))} КБ'.encode())
		info_size = f'Клиент запросил размер файла {file_size}'
		return info_size
	else:
		error = 'Указанный файл не найден!'
		conn.send(error.encode())
		return error


def get_size(bytes, suffix="B"):
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < (factor:=1024):
			return f"{bytes:.2f}{unit}{suffix}"
		bytes /= factor

#Создание папки
def create_folder(conn):
	way_dict_fold = (conn.recv(1024)).decode()
	if os.path.isdir(way_dict_fold):
		check_dict = 'True'
		conn.send(check_dict.encode())
		create_folder = (conn.recv(1024)).decode()
		check_folder = f'{way_dict_fold}\{create_folder}'
		os.mkdir(check_folder)					
		folder_dict = f'Папка создана! Путь: {check_folder}'
		conn.send(check_folder.encode())
		message_folder = f'Клиент создал папку! Путь {check_folder}'
		print(message_folder)
		return message_folder
	else:
		check_dict = 'False'
		conn.send(check_dict.encode())
		message_error = f'Директория не найдена! {way_dict_fold}'
		conn.send(message_error.encode())
		print(message_error)
		return message_error
	
#Загрузка файла на сервер
def load_file(conn):
	full_dir_client = (conn.recv(1024)).decode()
	way_direct = (conn.recv(1024)).decode()
	print(f'Путь директории {way_direct} найден')

	#Проверка на наличие директории и загрузка файла
	if os.path.isdir(way_direct):
		error_dispatch_log = 'True'
		conn.send(error_dispatch_log.encode())
		files = (conn.recv(1024)).decode()
		way_files = f'{way_direct}/{files}'
		save_way_files = f'Клиент загрузил файл! Путь сохранения файла: {way_files}'
		print(save_way_files)

		#Проверка на наличие файла
		if os.path.isfile(way_files):#True
			mesage_Server = 'Файл в данной директории уже есть! Заменить его?'
			conn.send(mesage_Server.encode())
			recent_file = (conn.recv(1024)).decode()
			if recent_file == 'Да':
				recent_yes = f'Клиент заменил файл {way_files}! Путь сохранения файла: {way_files}'
				print(recent_yes)
				time.sleep(2)
				downloads_files = open(way_files, 'wb')
				print('Сохранение файла с клиента...')
				while True:
					data = conn.recv(1024)
					downloads_files.write(data)
					if not data:break
				time.sleep(2)
				downloads_files.close()
				print('Сохранение файла завершено!')

				#Запись в файл json 
				conn.close()
				time.sleep(3)
				print("Переподключение")
				return recent_yes

			elif recent_file == 'Нет':
				recent_no = f'Клиент не заменил файл {way_files}'
				time.sleep(2)
				conn.close()
				print("Переподключение") 
				return recent_no
		else:
			mess_serv ='Файла в данной директории нет!'
			conn.send(mess_serv.encode())
			time.sleep(2)
			downloads_files = open(way_files, 'wb')
			print('Сохранение файла с клиента...')
			while True:
				data = conn.recv(1024)
				downloads_files.write(data)
				if not data: break
			time.sleep(2)
			downloads_files.close()
			print('Сохранение файла завершено!')

			#Запись в файл json 
			conn.close()
			time.sleep(1)
			print("Переподключение")    
			return save_way_files
	else:
		error_dispatch_log = 'False'
		conn.send(error_dispatch_log.encode())
		error_dispatch = f'Путь директории {way_direct} не найден'
		print(error_dispatch)

		#Запись в файл json 
		conn.send(error_dispatch.encode())
		time.sleep(2)
		conn.close()
		print("Переподключение") 
		return error_dispatch

#Скачивание файла клиентом	
def download_file(conn):
	send_files_log = (conn.recv(1024)).decode()
	print(send_files_log)

	if send_files_log == 'True':
		name_file = (conn.recv(1024)).decode()

		#Проверка на наличие файла
		if os.path.isfile(name_file) == True:
			send_prov_file = 'True'
			conn.send(send_prov_file.encode())
			send_way_files ='Путь файла: ',name_file
			print(send_way_files)
			send_files = open(name_file, 'rb')
			print('Передача файла клиенту...')
			time.sleep(4)
			line = send_files.read(1024)			
			while line:
				conn.send(line)
				line = send_files.read(1024)
			
			send_files.close()
			time.sleep(2)
			print('Передача файла завершена!')
			#Запись в файл json 
			conn.close()
			print("Переподключение") 
			return send_way_files 
		else:
			send_prov_file = 'False'
			conn.send(send_prov_file.encode())

			error_file = f'Путь файла {name_file} не найден!'
			print(error_file)
			conn.send(error_file.encode())
			#Запись в файл json
			time.sleep(2)
			conn.close()
			print("Переподключение") 
			return error_file
	elif send_files_log == 'False':
		print('Указанная директория на клиенте не найдена!')
		time.sleep(2)
		conn.close()
		print("Переподключение") 
