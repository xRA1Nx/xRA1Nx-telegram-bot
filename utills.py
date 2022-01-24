import requests
import json
from config import d_currency


class UserError(Exception):
    pass


class CheckInput:
    @staticmethod
    def get_price(words):
        if len(words) != 3:
            raise UserError("необходимо указать 3 параметра")
        val_from, val_to, count = words

        if val_from not in d_currency.keys():
            raise UserError(f"'{val_from}' нет в списке допустимых валют\n\
/currency - список возможных валют")
        if val_to not in d_currency.keys():
            raise UserError(f"'{val_to}' нет в списке допустимых валют\n\
/currency - список возможных валют")
        try:
            count = float(count)
        except ValueError:
            raise UserError(f"'{count}' кол-во валюты д.б. числом")
        else:
            count = float(count)

        r = requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=a6f4046ceb91a5e7d1566e72e860470d")
        data = json.loads(r.content)["rates"]
        if val_from == val_to:
            res = count
        else:
            res = round(
                float(data[d_currency[val_to]]) / float(data[d_currency[val_from]]) * float(
                    data[d_currency[val_to]]) * count, 2)
        txt = f"{count} {val_from} = {res} {val_to}"
        return txt
