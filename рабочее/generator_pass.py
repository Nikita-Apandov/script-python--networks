import random
import string
import argparse

def generate_password(length=12, use_uppercase=True, use_lowercase=True, 
                     use_digits=True, use_symbols=True, exclude_ambiguous=False):
    """
    Генерирует случайный пароль заданной длины.
    
    Параметры:
    - length (int): длина пароля (по умолчанию 12)
    - use_uppercase (bool): использовать заглавные буквы
    - use_lowercase (bool): использовать строчные буквы
    - use_digits (bool): использовать цифры
    - use_symbols (bool): использовать спецсимволы
    - exclude_ambiguous (bool): исключить неоднозначные символы (l, 1, O, 0 и т.п.)
    """
    
    # Определяем наборы символов
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Исключаем неоднозначные символы при необходимости
    if exclude_ambiguous:
        uppercase = uppercase.replace('O', '').replace('L', '')
        lowercase = lowercase.replace('l', '').replace('o', '')
        digits = digits.replace('0', '').replace('1', '')
    
    # Собираем разрешённые символы
    allowed_chars = ""
    if use_uppercase:
        allowed_chars += uppercase
    if use_lowercase:
        allowed_chars += lowercase
    if use_digits:
        allowed_chars += digits
    if use_symbols:
        allowed_chars += symbols
    
    # Проверяем, что есть хотя бы один разрешённый символ
    if not allowed_chars:
        raise ValueError("Нет разрешённых символов для генерации пароля!")
    
    # Генерируем пароль
    password = ''.join(random.choice(allowed_chars) for _ in range(length))
    
    return password

def main():
    parser = argparse.ArgumentParser(description="Генератор случайных паролей")
    parser.add_argument("-l", "--length", type=int, default=12,
                        help="Длина пароля (по умолчанию: 12)")
    parser.add_argument("--no-upper", action="store_true",
                        help="Не использовать заглавные буквы")
    parser.add_argument("--no-lower", action="store_true",
                        help="Не использовать строчные буквы")
    parser.add_argument("--no-digits", action="store_true",
                        help="Не использовать цифры")
    parser.add_argument("--no-symbols", action="store_true",
                        help="Не использовать спецсимволы")
    parser.add_argument("--exclude-ambiguous", action="store_true",
                        help="Исключить неоднозначные символы (l,1,O,0)")
    
    args = parser.parse_args()
    
    try:
        password = generate_password(
            length=args.length,
            use_uppercase=not args.no_upper,
            use_lowercase=not args.no_lower,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous
        )
        print(f"Сгенерированный пароль: {password}")
    except ValueError as e:
        print(f"!Ошибка: {e}")

if __name__ == "__main__":
    main()
