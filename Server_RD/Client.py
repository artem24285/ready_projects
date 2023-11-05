import socket, getpass
import re, time, os


class Connect_Client:

    #Подключение к серверу
    def __init__(self):   
        ip = '192.168.0.99'
        # self.ip = '127.0.0.1'
        port = 2027
        connect_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_server.connect((ip, port)) # Подключаемся к нашему серверу.  
        self.user_pass(connected_server=connect_server) 

    # Отправляем имя пользователя на сервер    
    def user_pass(self, connected_server):
        current_user = getpass.getuser()
        current_user = str(current_user)
        connected_server.send(current_user.encode())
        self.authorization(connect = connected_server)

    # Переподключение клиента к серверу
    # def reconnect_for_server(self):
    #     reconnect_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     reconnect_server.connect((self.ip, self.port)) # Подключаемся к нашему серверу. 
    #     self.control_Remote_Desktop(connect = reconnect_server)
        
    #Отключение клиента
    def exit(self,connect):
        connect.close()

    #Отправляем команды управления
    def control_Remote_Desktop(self, connect):         
         while True:
            command = input(str('> '))

            #Информация о железе
            if command == 'system_info':
                connect.send(command.encode())
                system = (connect.recv(1024)).decode()
                print('-'*20)
                for i in system.split(','):
                    i = re.sub(r"[, () ',]", " ",i)
                    print(i)
                print('-'*20)
            
            #Информация о температуре HDD и cpu
            if command == 'hardware_monitor':
                command = command.lower()
                connect.send(command.encode())
                cpu = (connect.recv(1024)).decode()
                print(cpu)

            #Информация о HDD
            if command == 'hdd_info':
                connect.send(command.encode())
                hdd = (connect.recv(1024)).decode()
               
                hdd_form_info = str(hdd)[1:-1]
                print(hdd_form_info)
                print('-'*40)
                for i in hdd_form_info.split(','): 
                    i = re.sub(r"[,  ']" , " ", i)    
                    print(i)
                print('-'*40)

             #Скачивание файл с сервера 
            if command == "download":
                connect.send(command.encode())
                save_file = input('Директория для сохранения файла: ')
                lens = 0

                if os.path.isdir(save_file):
                    send_files_log = 'True'
                    connect.send(send_files_log.encode())
                    files_names = input('Имя файла для сохранения: ')
                    save_files_client = f'{save_file}/{files_names}'
                    name_file = input(str('Путь файла на сервере: '))
                    connect.send(name_file.encode()) 
                    send_prov_files = connect.recv(1024)
                    send_prov_files = send_prov_files.decode()
                    
                    if send_prov_files == "True":              
                        downloads_files = open(save_files_client,'wb')
                        print('Сохранение файла с сервера...')
                        time.sleep(4)
                        while True:
                            data = connect.recv(1024)
                            lens = lens +1
                            print(f"Скачано: {lens} КБ")
                            downloads_files.write(data)
                            
                            if not data: break
                        downloads_files.close()     
                        print('Сохранение файла завершено!')
                        connect.close()
                        time.sleep(2)
                        print('Название файла: ', name_file)
                        time.sleep(3)
                        print('Переподключение')
                        Connect_Client()
                    elif send_prov_files == "False":
                        print(f'Файл {name_file} на сервере не найден!')
                        time.sleep(2)
                        print('Переподключение')
                        Connect_Client()
                else:
                    send_files_log = 'False'
                    connect.send(send_files_log.encode())
                    print(f'Директория {save_file} не найдена')
                    time.sleep(2)
                    print('Переподключение')
                    Connect_Client()

            #Загрузка файла на сервер
            if command == 'load':
                connect.send(command.encode())
                way_files_client = input(str("Путь файла на клиенте: "))
                lens = 0
                #Проверка директории на клиенте
                if os.path.isfile(way_files_client):
                    connect.send(way_files_client.encode())
                    send_way_files = input('Директория сохранения файла на сервере: ')
                    connect.send(send_way_files.encode())
                    error_dispatch_log = (connect.recv(1024)).decode()

                    #Проверка директории на сервере
                    if error_dispatch_log == 'True':
                        way_files_server = input(f'Файл для сохранения на сервере: {send_way_files}/ ')
                        connect.send(way_files_server.encode())
                        message_Server = (connect.recv(1024)).decode()
                        
                        print(f'Сервер: {message_Server}')
                        if message_Server == "Файл в данной директории уже есть! Заменить его?":
                            recent_file = input()
                            connect.send(recent_file.encode())
                            # self.progressbar(way_files_client,way_files_server)
                            send_files = open(way_files_client, 'rb')
                            time.sleep(2)
                            print('Передача файла серверу...')
                            line = send_files.read(1024)
                            time.sleep(3)
                            while line:
                                connect.send(line)
                                lens = lens+1
                                print(f"Загружено: {lens} КБ")
                                line = send_files.read(1024)
                            send_files.close()
                            print('Передача файла завершена!')
                            connect.close()
                            time.sleep(8)
                            print('Переподключение')
                            time.sleep(1)
                            Connect_Client()

                        elif message_Server == 'Файла в данной директории нет!':
                            # self.progressbar(way_files_client,way_files_server)
                            send_files = open(way_files_client, 'rb')
                            time.sleep(2)
                            print('Передача файла серверу...')
                            line = send_files.read(1024)
                            time.sleep(3)
                            while line:
                                connect.send(line)
                                lens = lens + 1
                                print(f"Загружено: {lens} КБ")
                                line = send_files.read(1024)
                            send_files.close()
                            print('Передача файла завершена!')
                            connect.close()
                            time.sleep(8)
                            print('Переподключение')
                            time.sleep(1)
                            Connect_Client()

                    elif error_dispatch_log == 'False':
                        error_dispatch = (connect.recv(1024)).decode()
                        print(error_dispatch)
                        time.sleep(2)
                        print('Переподключение')
                        Connect_Client()
                else:
                    print('Файл не найден в клиенте!')
                    time.sleep(2)
                    print('Переподключение')
                    Connect_Client()

            #Открытие папки
            if command == 'ls':
                connect.send(command.encode())
                way_search = input(str('ls: '))
                connect.send(way_search.encode())
                error_dir_serv = (connect.recv(1024)).decode()

                if error_dir_serv == 'True':
                    file_list = (connect.recv(1024)).decode()
                    file_format_list = str(file_list)[1:-1]
                    print('Название')
                    print('-'*20)
                    for i in file_format_list.split(','):
                        i = re.sub(r"[,  ']" , " ", i)
                        print(i)
                        print('-'*20)
                    time.sleep(2)
                    print('Переподключение')
                    Connect_Client()
                else:#False
                    time.sleep(2)
                    print('Переподключение')
                    Connect_Client()
            
              #Создание папки
            if command == 'create_folder':
                connect.send(command.encode())
                way_create_folder = input('Путь создания папки на сервере: ')
                connect.send(way_create_folder.encode())
                check_dict = (connect.recv(1024)).decode()

                if check_dict == 'True':
                    create_folder = input('Название папки: ')
                    connect.send(create_folder.encode())
                    folder_dict = connect.recv(1024)
                    folder_dict = folder_dict.decode()
                    print(f'Путь: {folder_dict}')

                elif check_dict == 'False':
                    message_error = connect.recv(1024)
                    message_error = message_error.decode()
                    print(message_error)
                    time.sleep(2)
                    print('Переподключение')
                    Connect_Client()

			#Запуск файла на сервере
            if command == 'start_file':
                error_start_file = (connect.recv(1024)).decode()

                if error_start_file == 'True':
                    connect.send(command.encode())
                    start_file = input(str('start: '))
                    connect.send(start_file.encode())
                    send_start_file = (connect.recv(1024)).decode()
                    print(send_start_file)

                else:#False
                    time.sleep(2)
                    print('Переподключение')
                    Connect_Client()

            #Создание папки
            if command == 'create_folder':
                connect.send(command.encode())
                way_create_folder = input('Путь создания папки на сервере: ')
                connect.send(way_create_folder.encode())
                check_dict = (connect.recv(1024)).decode()

                if check_dict == 'True':
                    create_folder = input('Название папки: ')
                    connect.send(create_folder.encode())
                    folder_dict = connect.recv(1024)
                    folder_dict = folder_dict.decode()
                    print(f'{folder_dict}')

                elif check_dict == 'False':
                    message_error = connect.recv(1024)
                    message_error = message_error.decode()
                    print(message_error)
                    time.sleep(2)
                    print('Переподключение')
                    Connect_Client()

            #Получение текущей директории сервера
            if command == 'current_dir':
                connect.send(command.encode())
                dir = (connect.recv(1024)).decode()
                print(dir)
            
            #Получение размера файла
            if command == 'file_size':
                connect.send(command.encode())
                file_size = input('Укажите файл для получения размера: ')
                connect.send(file_size.encode())
                size_file = (connect.recv(1024)).decode()
                print(size_file)

            #Отключение клиента
            if command == 'exit':  
                connect.send(command.encode())               
                print('Клиент отключен!')
                exit(connect)  
    
    #Авторизация на сервере
    def authorization(self, connect):
        time.sleep(1)
        login = getpass.getuser()
        connect.send(login.encode())
        print(f'Логин: {login}')      
        time.sleep(1)  
        password = input('Введите пароль: ')
        connect.send(password.encode())
        check_password = (connect.recv(1024)).decode()

        if check_password == 'True':
            message_entrance = (connect.recv(1024)).decode()
            print(message_entrance)
            self.control_Remote_Desktop(connect)
        else:
            error_entrance = (connect.recv(1024)).decode()
            print(error_entrance)
                         

#Принять доступ от сервера на хранилище и управлять им(просмотр, удаление, редактирование информации)
if __name__=='__main__':
    Connect_Client()