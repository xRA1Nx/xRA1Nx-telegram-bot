import requests
import json
from data import d_currency, d_massages
from config import ACCESS_KEY


class UserError(Exception):
    pass


class CheckInput:
    @staticmethod
    def get_price(words):
        if len(words) != 3:
            raise UserError("для конвертации валюты\
\n необходимо указать 3 параметра:\
\n ")
        val_from, val_to, count = words

        if val_from not in d_currency.keys():
            raise UserError(f"'{val_from}' нет в списке допустимых валют\n\
/currency - список возможных валют\
\n {d_massages['back']}")
        if val_to not in d_currency.keys():
            raise UserError(f"'{val_to}' нет в списке допустимых валют\n\
/currency - список возможных валют\
\n {d_massages['back']}")
        try:
            count = float(count)
        except ValueError:
            raise UserError(f"'{count}' кол-во валюты д.б. числом\
\n {d_massages['back']}")
        else:
            count = float(count)

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={ACCESS_KEY}")
        data = json.loads(r.content)["rates"]
        if val_from == val_to:
            res = count
        else:
            res = round(
                float(data[d_currency[val_to]]) / float(data[d_currency[val_from]]) * count, 2)
        txt = f"{count} {val_from} = {res} {val_to}"
        return txt
