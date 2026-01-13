#импорт библиотеки, так как данные мы будем получать именно из json-файла
import json


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
