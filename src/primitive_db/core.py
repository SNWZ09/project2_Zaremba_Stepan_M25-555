#импортируем декораторы
from ..decorators import confirm_action, handle_db_errors, log_time
from .utils import create_cacher, load_table_data


#создаем таблицу
@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')
        
    schema = {}
    
    if not columns:
        raise ValueError("Нельзя создать таблицу без колонок.")

    for col_def in columns:
        try:
            col_name, col_type = col_def.split(':')
            schema[col_name] = col_type
        except ValueError:
            # Обработка случая, если колонка задана неверно (например, 'name' вместо 'name:str')
            raise ValueError(f"Неверный формат колонки: '{col_def}'. Ожидается 'имя:тип'.")
    
    final_schema = {'id': 'int'}
    final_schema.update(schema)

    metadata[table_name] = final_schema
  
    return metadata
    
#удаляем таблицу
@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):

    #проверяем, существует ли таблица с таким именем
    if table_name not in metadata:
        raise ValueError(f'Error: Таблица "{table_name}" не существует.')
        
    #если есть - удаляем ее
    del metadata[table_name]

    #возвращаем обновленные метаданные
    return metadata


#добавляем новую запись в таблицу (добавил так же table_data)
@handle_db_errors
@log_time
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
         
_select_cacher = create_cacher()        
#выбирает данные из таблицы, пришлось добавить столбцы для кэша
@log_time
def select(table_name, columns, where_clause=None):
       
    cache_key = (table_name, tuple(columns), str(where_clause))
    
    def selection_process():
        table_data = load_table_data(table_name)
        actual_columns = columns

        result_table = []
        
        if not where_clause:
            for row in table_data:
                result_row = {col: row.get(col, 'N/A') for col in actual_columns}
                result_table.append(result_row)
        else:
            where_key, where_value = list(where_clause.items())[0]
            for row in table_data:
                if where_key in row and str(row[where_key]) == str(where_value):
                    result_row = {col: row.get(col, 'N/A') for col in actual_columns}
                    result_table.append(result_row)
        
        return result_table

    return _select_cacher(cache_key, selection_process)



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
@handle_db_errors
@confirm_action("удаление строки")
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
