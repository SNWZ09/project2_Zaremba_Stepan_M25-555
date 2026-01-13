#библиотека для получения ввода пользователя
#для надежного разбора строки
import prompt, shlex

#импортируем созданные мудули
from . import core, utils


#функция приветственных сообщений
def welcome():
    print("\n***База данных***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы") 
    print("<command> help - справочная информация")

#функция с основным циклом (while True)
def run():

    welcome()
    
    #пока пользователь не введет exit - программа от него не отстанет
    while True:
        user_input = prompt.string('Введите команду: ')
        
        #разбираем введенную строку
        args = shlex.split(user_input)
        
        #если пользователь ничего не ввёл - продолжаем ждать нормальную команду
        if not args:
            continue
        
        command = args[0]
        parameters = args[1:]
        
        #загружаем актуальную версию дб
        metadata =  utils.load_metadata('db_meta.json')
            
        try:
        
            #если exit, то выходим из цикла
            if command == 'exit':
                break
            
            #если help - выводим доступные команды
            elif command == 'help':
                welcome()
                
            elif command == 'create_table':
                
                #проверяем, что есть хотя бы мин. значение параметров
                if len(parameters) < 2:
                    print('Ошибка. Недостаточно параметров для создания таблицы.')
                    continue
                    
                table_name = parameters[0]
                columns = parameters[1:]
                
                #обновляем данные с учетом новой таблицы и сохр.
                updated_metadata = core.create_table(metadata, table_name, columns)
                utils.save_metadata('db_meta.json', updated_metadata)
                print(f'Таблица "{table_name}" успешно создана!')
                
            elif command == 'drop_table':
                
                #проверяем, что передано только название таблицы
                if len(parameters) != 1:
                    print('Ошибка. Для удаления таблицы передайте только её название.')
                    continue
                    
                table_name = parameters[0]
                
                #обновляем данные с учетом удаления таблицы и сохр.
                updated_metadata = core.drop_table(metadata, table_name)
                utils.save_metadata('db_meta.json', updated_metadata)
                print(f'Таблица "{table_name}" успешно удалена!')
                
            #этого в задании не было, но было в примере в начале второй страницы
            elif command == 'list_tables':
                
                #если таблиц нет - скажем об этом
                if not metadata:
                    print('Таблиц пока нет(')
                    
                else:
                    for name in metadata.keys():
                        print(name)
            
            else:
                print('Такая команда не предусмотрена')
                
        except ValueError as error:
            print(error)
