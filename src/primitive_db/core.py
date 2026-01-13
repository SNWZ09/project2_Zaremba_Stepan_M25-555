def create_table(metadata, table_name, columns):
    
    #проверяем, не существует ли уже таблица с таким именем
    #решил это поставить в начале, тк мне кажется,
    #что это более эффективное использование ресурсов компьютера
    if table_name in metadata:
        raise ValueError(f'Error: Таблица "{table_name}" уже существует.')

    #автоматически добавлять столбец ID:int в начало списка столбцов
    id_column = {"ID": "int"}

    #обрабатываем каждый столбец из списка
    for each_column in columns:
    
        #разделяем строку "имя:тип" на две части
        try:
            col_name, col_type = each_column.split(':')
        
        #если .split() не вернул 2 элемента, значит формат неверный
        #не знаю, как по-другому это нормально реализовать((
        except ValueError:
            raise ValueError(f'Некорректное значение в столбце "{each_column}". '
                             'Столбец должен быть в формате "имя:тип".')

        #если тип не "int", "str", "bool" - возвращаем ошибку
        if col_type not in {"int", "str", "bool"}:
            raise ValueError(f'Некорректный тип: "{col_type}". '
                             'Поддерживаемые типы: int, str, bool.')

        #если всё норм - добавляем столбец в словарь
        id_column[col_name] = col_type

    metadata[table_name] = id_column

    #возвращаем обновленные метаданные
    return metadata
    
    
def drop_table(metadata, table_name):

    #проверяем, существует ли таблица с таким именем
    if table_name not in metadata:
        raise ValueError(f'Error: Таблица "{table_name}" не существует.')
        
    #если есть - удаляем ее
    del metadata[table_name]

    #возвращаем обновленные метаданные
    return metadata


