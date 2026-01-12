#!/usr/bin/env python3

#импортируем созданные команды
from .engine import welcome


def main():
    print("DB project is running!")
    
    welcome()


if __name__ == "__main__":
    main()
