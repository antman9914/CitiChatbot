import http.client
from Citi.API import Global
import uuid
import json


class Utilities:
    @staticmethod
    def metadata_inquiry(api_uri, api_method):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

        headers = {
            'authorization': "Bearer %s" % Global.get_2_foot_token(),
            'uuid': str(uuid.uuid1()),
            'client_id': Global.get_client_id(),
            'accept': "application/json"
        }

        conn.request("GET", "/gcb/api/v1/utilities/metaData?apiUri=%s&apiMethod=%s" % (api_uri, api_method),
                     headers=headers)

        res = conn.getresponse()
        data = res.read()

        json_str = data.decode("utf-8")
        # dict = json.loads(json_str)
        print(json_str)

    @staticmethod
    def get_valid_values(value):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

        headers = {
            'authorization': "Bearer %s" % Global.get_2_foot_token(),
            'uuid': str(uuid.uuid1()),
            'client_id': Global.get_client_id(),
            'accept': "application/json"
        }

        conn.request("GET", "/gcb/api/v1/apac/utilities/referenceData/%s" % value, headers=headers)

        res = conn.getresponse()
        data = res.read()

        json_str = data.decode("utf-8")

        print(json_str)


Utilities.get_valid_values("locale")

