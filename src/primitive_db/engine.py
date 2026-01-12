#библиотека для получения ввода пользователя
import prompt

#функция приветственных сообщений
def welcome():
    
    print("Первая попытка запустить проект!")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    
    #пока пользователь не введет exit - программа от него не отстанет
    while True:
        command = prompt.string("Введите команду: ")
        
        #если exit, то выходим из цикла
        if command == "exit":
            break
            
        #если help - выводим доступные команды
        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
