import http.client
import uuid
from Citi.API import Global


class MoneyMovement:
    # r source_account_id string:加密之后的付款人id，通常不展示给用户
    # r transaction_amount number类型（具体是double）:转账总金额
    # r transfer_currency_indicator
    # r payee_id string:加密后的收款人id，通常不展示给用户
    # r chargeBearer
    # r paymentMethod
    # fxDealReferenceNumber
    # transferPurpose

    # r authorization string: 令牌
    # r client_id
    # r accept jason
    @staticmethod
    def create_personal_transfer(source_account_id, payee_id, ransaction_amount, access_token):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")
        payload = "{\"sourceAccountId\":\"%s\",\"" \
                  "transactionAmount\":%d,\"" \
                  "transferCurrencyIndicator\":\"SOURCE_ACCOUNT_CURRENCY\",\"" \
                  "payeeId\":\"%s\",\"" \
                  "chargeBearer\":\"BENEFICIARY\",\"" \
                  "paymentMethod\":\"GIRO\",\"" \
                  "fxDealReferenceNumber\":\"%s\",\"" \
                  "transferPurpose\":\"CASH_DISBURSEMENT\"}"

        headers = {
            'authorization': "Bearer %s" % access_token,
            'uuid': str(uuid.uuid1()),
            'client_id': Global.get_client_id(),
            'content-type': "application/json",
            'accept': "application/json"
        }

        conn.request("POST", "/gcb/api/v1/moneyMovement/personalDomesticTransfers/preprocess", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

    # control_flow_id string: the control flaw id (控制流程id),创建转账成功后获得的id
    # authorization string: 令牌
    # client_id
    # accept
    @staticmethod
    def confirm_personal_transfer(control_flow_id, access_token):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")
        payload = "{\"controlFlowId\":\"%s\"}" % control_flow_id

        headers = {
            'authorization': "Bearer %s" % access_token,
            'uuid': str(uuid.uuid1()),
            'client_id': Global.get_client_id(),
            'content-type': "application/json",
            'accept': "application/json"
        }

        conn.request("POST", "/gcb/api/v1/moneyMovement/personalDomesticTransfers", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))


# MoneyMovement.create_personal_transfer('11', '11', '11', '11')

