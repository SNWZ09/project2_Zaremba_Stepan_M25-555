#парсер для функции вставки значений
def parse_insert_values(args):

    #у меня это реализовано через поиск слова 'values'
    try:
        values_position = [arg.lower() for arg in args].index('values')
    except ValueError:
        raise ValueError("Ошибка. в INSERT отсутсвует слово 'values'.")

    #все, что после 'values', - нужные значения
    values_parts = args[values_position + 1:]

    #теперь просто всё соединяю в одну строку и чищу + разделяю по зяпятым
    full_values_str = " ".join(values_parts)
    cleaned_str = full_values_str.strip().strip('()')
    values = [v.strip() for v in cleaned_str.split(',')]
    
    return values
    
    
#парсер для функции обновления значений
def parse_update_clauses(args):

    #ищем 'set' и 'where'
    try:
        set_position = [arg.lower() for arg in args].index('set')
        where_position = [arg.lower() for arg in args].index('where')
    except ValueError:
        raise ValueError("Ошибка. в UPDATE должны быть 'set' и 'where'.")
        
    #упрощаем ввод пользователя с помощью подсказки в ValueError
    set_parts = args[set_position + 1 : where_position]
    if len(set_parts) != 3 or set_parts[1] != '=':
        raise ValueError("Ошибка 'set': ожидается 'ключ = значение'.")
    set_key = set_parts[0]
    set_value = set_parts[2]
    set_clause = {set_key: set_value}

    #упрощаем ввод пользователя с помощью подсказки в ValueError
    where_parts = args[where_position + 1:]
    if len(where_parts) != 3 or where_parts[1] != '=':
        raise ValueError("Ошибка 'where': ожидается 'ключ = значение'.")
    where_key = where_parts[0]
    where_value = where_parts[2]
    where_clause = {where_key: where_value}

    return set_clause, where_clause
    
#парсер для функции поиска значений
def parse_where_clause(args):

    #ищем слово 'where'.
    try:
        where_position = [arg.lower() for arg in args].index('where')
    except ValueError:
        return None

    condition_parts = args[where_position + 1:]
    
    #разбираем условие 
    #оно состоит из 3 частей (ключ, =, значение)
    if len(condition_parts) != 3 or condition_parts[1] != '=':
        raise ValueError("Ошибка 'where': ожидается 'ключ = значение'.")

    key = condition_parts[0]
    value = condition_parts[2]
    
    return {key: value}




