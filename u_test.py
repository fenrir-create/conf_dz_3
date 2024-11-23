import unittest
import tempfile
import os
from app import transform_to_custom_config 

class TestTOMLToCustomConfig(unittest.TestCase):

    def test_simple_key_value(self):
        input_data = {
            "title": "Пример TOML файла"
        }
        expected_output = "begin\ntitle := Пример TOML файла;\nend"
        self.assertEqual(transform_to_custom_config(input_data), expected_output)

    def test_nested_dictionary(self):
        input_data = {
            "owner": {
                "name": "Иван Иванов",
                "age": 30
            }
        }
        expected_output = "begin\nowner := begin\nname := Иван Иванов;\nage := 30;\nend\nend"
        self.assertEqual(transform_to_custom_config(input_data), expected_output)

    def test_array(self):
        input_data = {
            "ports": [8001, 8002, 8003]
        }
        expected_output = "begin\nports := #( 8001, 8002, 8003 );\nend"
        self.assertEqual(transform_to_custom_config(input_data), expected_output)

    def test_complex_structure(self):
        input_data = {
            "database": {
                "server": "192.168.1.1",
                "ports": [8001, 8002],
                "enabled": True
            }
        }
        expected_output = (
            "begin\n"
            "database := begin\n"
            "server := 192.168.1.1;\n"
            "ports := #( 8001, 8002 );\n"
            "enabled := True;\n"
            "end\n"
            "end"
        )
        self.assertEqual(transform_to_custom_config(input_data), expected_output)

    def test_invalid_key(self):
        input_data = {
            "123invalid": "value"
        }
        with self.assertRaises(ValueError) as context:
            transform_to_custom_config(input_data)
        self.assertTrue("Неверное имя ключа" in str(context.exception))

if __name__ == "__main__":
    unittest.main()
