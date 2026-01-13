#библиотека для получения ввода пользователя
#для надежного разбора строки
import shlex

import prompt
from prettytable import PrettyTable

#импортируем созданные мудули
from . import core, parser, utils


#функция приветственных сообщений
def welcome():
    print("\n***База данных***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> - создать таблицу")
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
        
        command = args[0].lower()
        
        #загружаем актуальную версию дб
        metadata =  utils.load_metadata('db_meta.json')
            
        try:
        
            #если exit, то выходим из цикла
            if command == 'exit':
                break
            
            #если help - выводим доступные команды
            elif command == 'help':
                welcome()
                continue
                
            elif command == 'create_table':
                    
                table_name = args[1]
                columns = args[2:]
                
                #обновляем данные с учетом новой таблицы и сохр.
                updated_metadata = core.create_table(metadata, table_name, columns)
                utils.save_metadata('db_meta.json', updated_metadata)
                
                #в эту переменную засовываем все части строки,
                #а потом соединяем её в единую строчку таблицы
                row_parts = []
                schema = updated_metadata[table_name]
                for key, value in schema.items():
                    formatted_part = f"{key}:{value}"
                    row_parts.append(formatted_part)
                    row_str = ", ".join(row_parts)
                
                print(f'Таблица "{table_name}" успешно создана!')
                print(row_str)
                
            elif command == 'drop_table':
                    
                table_name = args[1]
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
                        
            #добавляем новую запись в таблицу (добавил так же table_data)         
            elif command == 'insert':
                if len(args) < 4 or args[1].lower() != 'into':
                    raise ValueError('Ошибка'
                                    'ожидается "insert into <имя_таблицы> values"')
                
                table_name = args[2]
                values = parser.parse_insert_values(args)
                
                table_data = utils.load_table_data(table_name)
                updated_data, new_id = core.insert(metadata, table_name, table_data, values)
                utils.save_table_data(table_name, updated_data)
                
                print(f'Запись с ID={new_id} успешно добавлена в {table_name}.')
            
            
            #выбирает данные из таблицы
            elif command == 'select':
                
                #всё та же проверка на ключ, =, значение, что и в parser.py
                if len(args) < 3 or args[1].lower() != 'from':
                    raise ValueError('Ошибка: ожидается "select from <имя_таблицы>"')
                
                table_name = args[2]
                if table_name not in metadata:
                    raise ValueError(f'Ошибка: Таблица "{table_name}" не существует.')

                #используем созданный парсер
                where_clause = parser.parse_where_clause(args)
                
                table_data = utils.load_table_data(table_name)
                results = core.select(table_data, where_clause)

                
                if not results:
                    print('Нет записей, удовлетворяющих условию.')
                else:
                    schema = metadata[table_name]
                    table = PrettyTable()
                    table.field_names = schema.keys()
                    
                    #вот это с помощью ии, не очень понял PrettyTable по документации
                    #извините
                    for record in results:
                        row = [record.get(col, 'N/A') for col in table.field_names]
                        table.add_row(row)
                    print(table)
            
            
            #обновляет данные в таблице
            elif command == 'update':
                table_name = args[1]
                set_clause, where_clause = parser.parse_update_clauses(args)
                
                table_data = utils.load_table_data(table_name)
                updated_data, updated_ids = core.update(table_data, 
                                                    set_clause, where_clause)
                utils.save_table_data(table_name, updated_data)

                if updated_ids:
                    print(f'Обновлено {len(updated_ids)} записей в {table_name}.')
                else:
                    print('Не найдено записей для обновления.')

            elif command == 'delete':
            
                #всё та же проверка на ключ, =, значение, что и в parser.py
                if len(args) < 3 or args[1].lower() != 'from':
                    raise ValueError('Ошибка: ожидается "delete from <имя_таблицы>"')
                
                table_name = args[2]
                where_clause = parser.parse_where_clause(args)
                
                table_data = utils.load_table_data(table_name)
                updated_data, deleted_count = core.delete(table_data, where_clause)
                utils.save_table_data(table_name, updated_data)

                print(f'Удалено {deleted_count} записей из таблицы {table_name}.')
            
            else:
                print('Такая команда не предусмотрена')
                
        except (ValueError, IndexError) as e: 
            print(e)
