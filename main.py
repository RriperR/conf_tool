import argparse
import json
import re

class ConfigParser:
    def __init__(self):
        self.constants = {}
        self.result = {}
        self.expression_count = 0  # Счетчик для выражений

    def parse(self, content):
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("//") or not line:
                continue
            if "is" in line:
                self.parse_constant(line)
            elif line.startswith("$") and line.endswith("$"):
                self.evaluate_expression(line)
            else:
                raise SyntaxError(f"Invalid syntax: {line}")
        return self.result

    def parse_constant(self, line):
        match = re.match(r"([_a-zA-Z]+)\s+is\s+(.+);", line)
        if match:
            name, value = match.groups()
            value = value.strip()
            # Проверка на вещественное число
            if re.match(r"^-?\d+\.\d+$", value):  # Вещественное число
                self.constants[name] = float(value)
            elif re.match(r"^-?\d+$", value):  # Целое число
                self.constants[name] = int(value)
            elif value.startswith("[") and value.endswith("]"):
                self.constants[name] = self.parse_array(value)
            elif value.startswith('"') and value.endswith('"'):
                self.constants[name] = value.strip('"')
            else:
                raise SyntaxError(f"Invalid constant value: {value}")

            # Сохранение констант в результат
            self.result[name] = self.constants[name]
        else:
            raise SyntaxError(f"Invalid constant declaration: {line}")

    def parse_array(self, value):
        # Функция для рекурсивного парсинга массивов
        def parse_element(element):
            element = element.strip()
            if element.startswith('"') and element.endswith('"'):  # Строка
                return element.strip('"')
            elif element.startswith('[') and element.endswith(']'):  # Вложенный массив
                return parse_array(element)
            elif re.match(r"^-?\d+\.\d+$", element):  # Вещественное число
                return float(element)
            elif re.match(r"^-?\d+$", element):  # Целое число
                return int(element)
            else:
                raise SyntaxError(f"Invalid array element: {element}")

        def parse_array(array_str):
            elements = []
            stack = []
            current = ''
            for char in array_str[1:-1]:
                if char == '[':
                    stack.append('[')
                    current += char
                elif char == ']':
                    stack.pop()
                    current += char
                elif char == ';' and not stack:
                    elements.append(current.strip())
                    current = ''
                else:
                    current += char

            if current:
                elements.append(current.strip())

            return [parse_element(element) for element in elements]

        return parse_array(value)

    def evaluate_expression(self, line):
        expression = line[1:-1].split()
        stack = []
        for token in expression:
            if re.match(r"^-?\d+(\.\d+)?$", token):
                stack.append(float(token))
            elif token in self.constants:
                stack.append(self.constants[token])
            elif token == '+':
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif token == '-':
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token == '*':
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            elif token == 'pow()':
                b, a = stack.pop(), stack.pop()
                stack.append(pow(a, b))
            else:
                raise SyntaxError(f"Unknown token: {token}")

        self.expression_count += 1
        result_value = stack[0]
        self.result[f"expression_{self.expression_count}"] = result_value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as file:
            content = file.read()

        config_parser = ConfigParser()
        result = config_parser.parse(content)
        print(json.dumps(result, indent=4))

    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
    except SyntaxError as e:
        print(f"Syntax error: {e}")

if __name__ == "__main__":
    main()