import json
import requests
from config import keys


class MSGException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(From, To, Amount):
        try:
            From_key = keys[From.lower()]
        except KeyError:
            raise MSGException(f"Валюта {From} не найдена!")

        try:
            To_key = keys[To.lower()]
        except KeyError:
            raise MSGException(f"Валюта {To} не найдена!")

        if From_key == To_key:
            raise MSGException(f'Невозможно перевести одинаковые валюты {From}!')

        try:
            Amount = float(Amount)
        except ValueError:
            raise MSGException(f'Не удалось обработать количество {Amount}!')

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={From_key}&symbols={To_key}")
        total_value = json.loads(r.content)[keys[From]]

        return total_value
