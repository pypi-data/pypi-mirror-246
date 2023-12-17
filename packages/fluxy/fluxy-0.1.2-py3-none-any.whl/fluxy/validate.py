import re

class Validator:
    @staticmethod
    async def phone_number(phone_number):
        phone_pattern = re.compile(r'^\+998\d{9}$')
        is_valid = bool(re.match(phone_pattern, phone_number))

        if is_valid:
            print(f"Ваш номер {phone_number} соответствует узбекскому формату. ")
            return True
        else:
            print(f"Ваш номер {phone_number} не соответствует узбекскому формату.")
            return False

    @staticmethod
    async def passport_number(passport_number):
        passport_pattern = re.compile(r'^[A-Z]{2}\d{7}$')

        if re.match(passport_pattern, passport_number):
            print(f"Номер узбекского паспорта {passport_number} соответствует шаблону.")
            return True
        else:
            print(f"Номер узбекского паспорта {passport_number} не соответствует шаблону.")
            return False
