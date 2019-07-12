import http.client
from Citi.API import Global
import json
import uuid


class Cards:
    @staticmethod
    def get_cards_info(card_function):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

        headers = {
            'authorization': "Bearer %s" % Global.get_access_token(),
            'client_id': Global.get_client_id(),
            'uuid': str(uuid.uuid1()),
            'accept': "application/json"
        }

        conn.request("GET", "/gcb/api/v1/cards?cardFunction=%s" % card_function, headers=headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))