import unittest
from main import ConfigParser  # Убедитесь, что main.py находится в той же директории или в PYTHONPATH


class TestConfigParser(unittest.TestCase):

    def test_constant_declaration(self):
        """Тест объявлений констант: целые числа, строки и массивы."""
        content = """
        // Конфигурация с константами
        port is 8080;
        host is "localhost";
        allowed_ips is [ "192.168.1.1"; "192.168.1.2" ];
        pi is 3.1415;
        """
        config_parser = ConfigParser()
        result = config_parser.parse(content)

        expected = {
            "port": 8080,
            "host": "localhost",
            "allowed_ips": ["192.168.1.1", "192.168.1.2"],
            "pi": 3.1415
        }
        self.assertEqual(result, expected)

    def test_expression_evaluation(self):
        """Тест вычисления постфиксных выражений."""
        content = """
        // Конфигурация для расчета площади круга
        pi is 3.1415;
        radius is 10;
        $pi radius radius * *$
        """
        config_parser = ConfigParser()
        result = config_parser.parse(content)

        expected = {
            "pi": 3.1415,
            "radius": 10,
            "expression_1": 314.15000000000003  # Площадь круга
        }
        self.assertEqual(result, expected)

    def test_syntax_error(self):
        """Тест на синтаксическую ошибку в конфигурации."""
        content = """
        // Некорректная конфигурация
        port is 8080
        host is "localhost";
        """
        config_parser = ConfigParser()
        with self.assertRaises(SyntaxError):
            config_parser.parse(content)

    def test_nested_arrays(self):
        """Тест массивов с вложенными конструкциями."""
        content = """
        // Массивы с вложенными конструкциями
        nested_array is [ 1; [2; 3]; [4; 5; [6; 7]] ];
        """
        config_parser = ConfigParser()
        result = config_parser.parse(content)

        expected = {
            "nested_array": [1, [2, 3], [4, 5, [6, 7]]]
        }
        self.assertEqual(result, expected)


# Запуск тестов
if __name__ == '__main__':
    unittest.main()
