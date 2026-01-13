#импортируем для красивого вывода таблиц в консоль

def create_table(metadata, table_name, columns):
    
    #проверяем, не существует ли уже таблица с таким именем
    #решил это поставить в начале, тк мне кажется,
    #что это более эффективное использование ресурсов компьютера
    if table_name in metadata:
        raise ValueError(f'Error: Таблица "{table_name}" уже существует.')

    #автоматически добавлять столбец ID:int в начало списка столбцов
    id_column = {'ID': 'int'}

    #обрабатываем каждый столбец из списка
    for each_column in columns:
    
        #разделяем строку 'имя:тип' на две части
        try:
            col_name, col_type = each_column.split(':')
        
        #если .split() не вернул 2 элемента, значит формат неверный
        #не знаю, как по-другому это нормально реализовать((
        except ValueError:
            raise ValueError(f'Некорректное значение в столбце "{each_column}". '
                             'Столбец должен быть в формате "имя:тип".')

        #если тип не 'int', 'str', 'bool' - возвращаем ошибку
        if col_type not in {'int', 'str', 'bool'}:
            raise ValueError(f'Некорректный тип: "{col_type}". '
                             'Поддерживаемые типы: int, str, bool.')

        #если всё норм - добавляем столбец в словарь
        id_column[col_name] = col_type

    metadata[table_name] = id_column

    #возвращаем обновленные метаданные
    return metadata
    
#удаляем таблицу    
def drop_table(metadata, table_name):

    #проверяем, существует ли таблица с таким именем
    if table_name not in metadata:
        raise ValueError(f'Error: Таблица "{table_name}" не существует.')
        
    #если есть - удаляем ее
    del metadata[table_name]

    #возвращаем обновленные метаданные
    return metadata


#добавляем новую запись в таблицу (добавил так же table_data)
def insert(metadata, table_name, table_data, values):

    #проверяем, существует ли таблица с таким именем
    if table_name not in metadata:
        raise ValueError(f'Error: Таблица "{table_name}" не существует.')
    

    schema = metadata[table_name]
    
    #создаём пустой список, в который будем класть все столбцы
    user_columns = []
    
    #проверка на то, чтобы мы не брали ID
    for col_name in schema.keys():
        if col_name != 'ID':
            user_columns.append(col_name)
        
    if len(values) != len(user_columns):
        raise ValueError(f'Ошибка: Ожидалось {len(user_columns)} значений, '
                         f'но было передано {len(values)}.')
                         
    #здесь хранятся новые данные
    new_row = {}
    
    #проверяем введенные типы данных и изначальные в таблице
    for col_name, value_str in zip(user_columns, values):
        expected_type = schema[col_name]
        try:
            if expected_type == 'int':
                converted_value = int(value_str)
            elif expected_type == 'str':
                
                #тут ии подсказала учесть, каюсь
                converted_value = value_str.strip('"\'')
            elif expected_type == 'bool':
                if value_str.lower() == 'true':
                    converted_value = True
                elif value_str.lower() == 'false':
                    converted_value = False
                else:
                    raise ValueError('Bool должен быть "true" или "false"')
                
            new_row[col_name] = converted_value
        except ValueError:
            raise ValueError(f'Значение {value_str}'
                            'не соответствует ожидаемому типу {expected_type}')
        
    #генерируем новый ID + учтем ситуацию с первой записью в таблице
    if not table_data:
        new_id = 1
    else:
        max_id = 0
        for row in table_data:
            if row['ID'] > max_id:
                max_id = row['ID']
        new_id = max_id + 1
        
    new_row['ID'] = new_id
    
    #добавляем запись
    table_data.append(new_row)
    
    return table_data, new_id
         
        
#выбирает данные из таблицы
def select(table_data, where_clause=None):
    if not where_clause:
        return table_data

    where_key, where_value = list(where_clause.items())[0]
    results = []
    for row in table_data:
        
        #приводим всё к строкам (на всякий-всякий случай, чтоб ничего не ругалось)
        if where_key in row and str(row[where_key]) == str(where_value):
            results.append(row)
    return results


#обновляет данные в таблице
def update(table_data, set_clause, where_clause):

    set_key, set_value = list(set_clause.items())[0]
    where_key, where_value = list(where_clause.items())[0]
    updated_ids = []

    for row in table_data:
        
        #через эту конструкцию находим нужную строчку
        if where_key in row and str(row[where_key]) == str(where_value):
            row[set_key] = set_value
            updated_ids.append(row['ID'])

    return table_data, updated_ids


#удаляет данные в таблице
def delete(table_data, where_clause):

    #проверяем, есть ли условие
    if not where_clause:
        raise ValueError('Ошибка: Нет условия для удаления.')
        
    where_key, where_value = list(where_clause.items())[0]
    
    rows_to_keep = []
    
    #логика будет такой: если строчка не удовлетворяет условиям where - запоминаем её
    #если удовлетворяет - не запоминаем
    for row in table_data:
        
        #проверяем, нужно ли удалять строчку
        descision_delete = (where_key in row and 
                                str(row[where_key]) == str(where_value))
        # Если удалять НЕ нужно, то мы ее сохраняем
        if not descision_delete:
            rows_to_keep.append(row)
    
    deleted_count = len(table_data) - len(rows_to_keep)
    
    return rows_to_keep, deleted_count
