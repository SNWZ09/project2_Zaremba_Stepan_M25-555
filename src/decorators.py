import time


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
    
        #если всё норм - возвращаем результат
        try:
            return func(*args, **kwargs)
        
        #если внутри функции возникает ошибка - идет "перехват"
        except (KeyError, ValueError, FileNotFoundError) as e:
            
            #выводим сообщение об ошибке
            print(f"Ошибка: {e}")
    
    return wrapper
    
    
def confirm_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            confirmation_message = (f'Вы уверены, что хотите выполнить "{action_name}"?'
                                    '[y/n]: ')
            confirmation_input = input(confirmation_message).lower()
        
            #если пользователь ввел y - выполняем функцию
            if confirmation_input == 'y':
                return func(*args, **kwargs)
        
            #если пользователь ввел n - не выполняем
            else:
                print(f'"{action_name}" не будет выполнено.')
            
        return wrapper
    
    return decorator


def log_time(func):
    def wrapper(*args, **kwargs):
        
        #засекаем время
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        
        #засекаем время после выполнения
        end_time = time.monotonic()
        
        #вычисляем сколько времени прошло
        total_time = end_time - start_time
        
        #округляем результат до 3-ех знаков после запятушки
        print(f'Функция "{func.__name__}" выполнилась за {total_time:.3f} секунд.')
        return result
    return wrapper
