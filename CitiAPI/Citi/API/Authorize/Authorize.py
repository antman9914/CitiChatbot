import http.client
from Citi.API import Global
import json


class Authorize:
    @staticmethod
    def get_access_token_by_client_credentials_grant(scope):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

        payload = "grant_type=client_credentials&scope=%s" % scope

        headers = {
            'authorization': "Basic %s" % Global.get_pressed_id_secret_pair(),
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/json"
        }

        conn.request("POST", "/gcb/api/clientCredentials/oauth2/token/hk/gcb", payload, headers)

        res = conn.getresponse()
        data = res.read()

        json_str = data.decode("utf-8")
        dict = json.loads(json_str)
        if "access_token" not in dict.keys():
            print(json_str)
            return "error"
        else:
            token = dict["access_token"]
            return token

    # r scope 申请权限集合，以空格分隔
    # r country_code 国家3316二位码，大写
    # r business_code 商业行为码
    # r locale 地区
    # r state
    # r redirect_uri 重定位uri，注册app时获得的uri
    @staticmethod
    def get_authorization_code(scope, country_code, business_code, locale, state, redirect_uri):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")
        headers = {'accept': "application/json"}

        conn.request("GET",
                     "/gcb/api/authCode/oauth2/authorize?response_type=code&"
                     "client_id=%s&"
                     "scope=%s&"
                     "countryCode=%s&"
                     "businessCode=%s&"
                     "locale=%s&"
                     "state=%s&"
                     "redirect_uri=%s" % (Global.get_client_id(), scope, country_code, business_code,
                                          locale, state, redirect_uri),
                     headers=headers)

        res = conn.getresponse()
        print(res)
        data = res.read()

        # print(data.decode("utf-8"))
        print(data)
        return res

    # r code api2处返回的结果获得的code
    # r redirect_uri code api2处传入的redirect_uri
    @staticmethod
    def get_access_token_by_authorization_code_grant(code, uri):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

        payload = "grant_type=authorization_code&code=%s&redirect_uri=%s" % (code, uri)

        headers = {
            'authorization': "Basic %s" % Global.get_pressed_id_secret_pair(),
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/json"
        }

        conn.request("POST", "/gcb/api/authCode/oauth2/token/hk/gcb", payload, headers)

        res = conn.getresponse()
        data = res.read()

        json_str = data.decode("utf-8")
        dict = json.loads(json_str)

        if "access_token" not in dict.keys():
            print(json_str)
            return "error"
        else:
            access_token = dict["access_token"]
            refresh_token = dict["refresh_token"]
            ret_dic = {"access_token": access_token, "refresh_token": refresh_token}
            print(ret_dic)
            return ret_dic

    # 此处的refresh_token 到底是什么？
    @staticmethod
    def refresh_access_token():
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

        payload = "grant_type=refresh_token&refresh_token=%s" % Global.get_refresh_token()

        headers = {
            'authorization': "Basic %s" % Global.get_pressed_id_secret_pair(),
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/json"
        }

        conn.request("POST", "/gcb/api/authCode/oauth2/refresh", payload, headers)

        res = conn.getresponse()
        data = res.read()

        json_str = data.decode("utf-8")
        dict = json.loads(json_str)

        print(data.decode("utf-8"))

    # revoke_token 要回收的token
    # token_type_hint 要回收的token的种类，access_token或refresh_token
    @staticmethod
    def revoke_access(revoke_token, token_type_hint):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

        payload = "token=%s&token_type_hint=%s" % (revoke_token, token_type_hint)

        headers = {
            'authorization': "Basic %s" % Global.get_pressed_id_secret_pair(),
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/json"
        }

        conn.request("POST", "/gcb/api/authCode/oauth2/revoke", payload, headers)

        res = conn.getresponse()
        data = res.read()

        json_str = data.decode("utf-8")
        dict = json.loads(json_str)

        if "status" not in dict.keys() or dict["status"] != "success":
            print(json_str)
            return "error"
        else:
            return "success"


# print(Authorize.get_access_token_by_client_credentials_grant("/api"))
# res = Authorize.get_authorization_code("accounts_details_transactions", "US", "GCB", "en_US", "OSd2m1dsaodOSDAwaW1",
#                                  "https://sandbox.developerhub.citi.com/playground/default.html")
# print("res",res)
# print("res status",res.status)
Authorize.get_access_token_by_authorization_code_grant("", "http://129.204.225.110/huaqi/")

# Authorize.refresh_access_token()
# Authorize.revoke_access()
