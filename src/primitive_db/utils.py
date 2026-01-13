#импорт библиотеки, так как данные мы будем получать именно из json-файла
import json

#пришлось импортировать эту библиотеку, тк, судя по информации в интернете
#она поможет в создании папок
import os


#загрузка данных из json-файла
def load_metadata(filepath):
    try:
        #открываем файл
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
        
    #если файл не найден - возвращает пустой словарь
    except FileNotFoundError:
        return {}
        
#сохранение переданных данных в json-файл  
def save_metadata(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        
        #превразение словаря в json-файл  
        json.dump(data, f)
        

#функция, которая работает по аналогии с load_metadata, но + директория data
def load_table_data(table_name):

    #добавляем наш "путь" к папке, в остальном код такой же
    filepath = f'data/{table_name}.json'
    try:
        #открываем файл
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
        
    #если файл не найден - возвращает пустой словарь
    except FileNotFoundError:
        return []
        
        
#функция, которая работает по аналогии с save_metadata, но + директория data
def save_table_data(table_name, data):
    
    #создаем директорию data
    #если такая уже есть - программа ничего не сделает
    os.makedirs("data", exist_ok=True)
    
    #добавляем наш "путь" к папке, в остальном код такой же
    filepath = f'data/{table_name}.json'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        
        #превразение словаря в json-файл
        json.dump(data, f)
    
    
def create_cacher():

    #тут будет храниться кэш
    cache = {}
        
    def cache_result(key, value_func):
        
        #проверка результата функции в кэше по ключу
        if key in cache:
            print('Результат для этого запроса найден в кэше')
            return cache[key]
            
        #если результата функции нет
        else:
            print('В кэше нет результата')
            result = value_func()
            cache[key] = result
            return result
    return cache_result
