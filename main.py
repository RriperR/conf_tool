import re
import json
import sys

# Словарь для хранения констант
constants = {}


# Функция для вычисления постфиксных выражений
def eval_postfix(expression):
    stack = []
    for token in expression:
        if token.isdigit():
            stack.append(int(token))
        elif token == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif token == '-':
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif token == '*':
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        elif token == 'pow':
            b = stack.pop()
            a = stack.pop()
            stack.append(pow(a, b))
    return stack[0]


# Парсинг конфигурационного файла
def parse_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        # Игнорируем комментарии
        if line.startswith('//') or not line:
            continue
        # Обработка объявления константы
        if 'is' in line:
            name, value = line.split('is')
            name = name.strip()
            value = value.strip().rstrip(';')
            if value.startswith('$') and value.endswith('$'):
                # Постфиксная нотация
                expression = value[1:-1].split()
                result = eval_postfix(expression)
                constants[name] = result
            else:
                # Присваиваем числовое значение
                constants[name] = int(value)
        elif line.startswith('[') and line.endswith(']'):
            array_values = line[1:-1].split(';')
            array_values = [int(v.strip()) for v in array_values]
            constants["array"] = array_values


# Генерация JSON
def generate_json():
    return json.dumps(constants, indent=4)


# Главная функция
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    parse_file(filepath)
    print(generate_json())


if __name__ == "main":
    main()