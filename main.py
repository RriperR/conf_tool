import json
import re
import sys

def parse_line(line):
    line = line.strip()
    if line.startswith('//'):
        return None  # Однострочный комментарий, игнорируем
    match = re.match(r'([\w_]+)\s+is\s+(.+);', line)
    if match:
        name, value = match.groups()
        return name, eval_value(value)
    else:
        raise SyntaxError(f"Ошибка синтаксиса: {line}")

def eval_value(value):
    if re.match(r'^\[.*\]$', value):
        return parse_array(value)
    elif re.match(r'^\d+$', value):
        return int(value)
    elif re.match(r'^"[^"]*"$', value):  # Обработка строковых значений
        return value[1:-1]  # Убираем кавычки
    elif re.match(r'^\$[\w_]+\s*\d*\s*[\+\-\*/]\s*\$$', value):
        return eval_expression(value)
    else:
        raise ValueError(f"Неподдерживаемое значение: {value}")

def parse_array(value):
    return [eval_value(v.strip()) for v in value[1:-1].split(';')]

def eval_expression(value):
    # Пример реализации для обработки математических выражений
    expression = value.strip('$').replace('$', '')
    return eval(expression)  # Внимание: использовать eval с осторожностью!

def process_file(file_path):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            try:
                result = parse_line(line)
                if result:
                    name, value = result
                    config[name] = value
            except (SyntaxError, ValueError) as e:
                print(f"Ошибка: {e}")
                sys.exit(1)
    return config

def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <путь к файлу>")
        sys.exit(1)

    file_path = sys.argv[1]
    config = process_file(file_path)
    print(json.dumps(config, indent=4))

if __name__ == "__main__":
    main()
