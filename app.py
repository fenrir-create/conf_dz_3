import toml
import argparse
import re

def validate_name(name):
    # Проверка соответствия имени шаблону: [_a-zA-Z]+
    pattern = r'^[_a-zA-Z]+$'
    return bool(re.match(pattern, name))

def transform_to_custom_config(data):
    output = []

    if isinstance(data, dict):
        output.append("begin")
        for key, value in data.items():
            if not validate_name(key):
                raise ValueError(f"Неверное имя ключа: {key}")

            if isinstance(value, (int, float, str)):
                output.append(f"{key} := {value};")
            elif isinstance(value, list):
                array_values = ', '.join(map(str, value))
                output.append(f"{key} := #( {array_values} );")
            elif isinstance(value, dict):
                nested_dict = transform_to_custom_config(value)
                output.append(f"{key} := {nested_dict}")
            else:
                raise ValueError(f"Неподдерживаемый тип значения: {type(value)}")

        output.append("end")
    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Преобразование TOML в учебный конфигурационный язык.")
    parser.add_argument("--input", required=True, help="Путь к входному файлу TOML")
    parser.add_argument("--output", required=True, help="Путь к выходному файлу")

    args = parser.parse_args()

    # Чтение TOML файла
    try:
        with open(args.input, 'r',encoding='utf-8') as file:
            toml_data = toml.load(file)
    except Exception as e:
        print(f"Ошибка при чтении входного файла: {e}")
        return

    try:
        output_data = transform_to_custom_config(toml_data)
    except ValueError as e:
        print(f"Синтаксическая ошибка: {e}")
        return

    try:
        with open(args.output, 'w') as file:
            file.write(output_data)
    except Exception as e:
        print(f"Ошибка при записи в выходной файл: {e}")

if __name__ == "__main__":
    main()
