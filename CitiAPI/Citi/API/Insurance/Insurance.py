import http.client
import uuid
from Citi.API import Global


class Insurance:

    #
    #
    #
    #
    #
    @staticmethod
    def insurance_source_account_eligibility(access_token):
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")
        headers = {
            'authorization': "Bearer %s" % access_token,
            'uuid': str(uuid.uuid1()),
            'client_id': Global.get_client_id(),
            'clientdetails': "REPLACE_THIS_VALUE",
            'accept': "application/json"
        }

        conn.request("GET", "/gcb/api/v1/insurance/bookings/sourceAccounts", headers=headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

    #
    #
    #
    @staticmethod
    def insurance_booking(access_token):

        # 调用insurance_source_account_eligibility，如果可以预定则预定，否则不能预定
        conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")
        payload = "{\"policyDetails\":{\"insuranceProductCode\":\"PR001- PAGOS PROTEGIDOS BASICO\",\"" \
                  "insuranceProductCurrencyCode\":\"SGD\",\"insurancePolicyNumber\":\"83748374389\",\"" \
                  "insurancePolicyStatus\":\"CONFIRMED\",\"insuranceSumAssuredAmount\":25000.12,\"" \
                  "insurancePremiumPaymentFrequency\":\"MONTHLY\",\"policyTermType\":\"MONTHS\",\"" \
                  "policyTerm\":120,\"premiumPaymentTermType\":\"MONTHS\",\"premiumPaymentTerm\":180,\"" \
                  "policyBillingMode\":\"INTERNAL\",\"applicationDate\":\"2018-10-01'\",\"" \
                  "insurancePolicyEffectiveDate\":\"2018-11-01\",\"basePremiumAmount\":1000.21,\"" \
                  "addOnPremiumAmount\":100.52,\"totalPremiumAmount\":1110.73,\"" \
                  "policyMaturityDate\":\"2028-11-01'\",\"legalAgreementFlag\":true,\"" \
                  "firstPremiumDueDate\":\"2018-10-05'\"},\"offerDetails\":{\"waveId\":987654321,\"" \
                  "campaignId\":123456789,\"offerId\":111000125},\"riderDetails\":{\"riderCode\":\"TP1\",\"" \
                  "riderSumAssuredAmount\":25000.11,\"riderTermType\":\"MONTHS\",\"riderTerm\":60,\"" \
                  "riderEffectiveDate\":1546214400000},\"applicant\":{\"name\":{\"salutation\":\"MR.\",\"" \
                  "givenName\":\"Javier\",\"middleName\":\"Perez\",\"surname\":\"de Cuellar\"},\"" \
                  "identificationDocumentDetails\":{\"idType\":\"PASSPORT\",\"" \
                  "idNumber\":\"Passport- 443431, CIN- 123123123\"},\"demographics\":{\"gender\":\"MALE\",\"" \
                  "dateOfBirth\":\"1980-01-01\",\"maritalStatus\":\"SINGLE\",\"nationality\":\"SG\"},\"" \
                  "employmentDetails\":{\"occupationCode\":\"ACCOUNTANT\",\"businessNature\":\"BANKING\"},\"" \
                  "ownershipType\":\"OWNER\",\"additionalData\":{\"relationshipWithPrimary\":\"HUSBAND\"},\"" \
                  "email\":{\"emailAddress\":\"javier@abcd.com\"},\"" \
                  "address\":{\"addressLine1\":\"40A Orchard Road\",\"addressLine2\":\"#99-99 Macdonald House\",\"" \
                  "addressLine3\":\"Orchard Avenue 2\",\"addressLine4\":\"Street 65\",\"cityName\":\"Singapore\",\"" \
                  "state\":\"SINGAPORE\",\"postalCode\":520189},\"phone\":{\"phoneCountryCode\":\"65\"}},\"" \
                  "initialPaymentDetails\":{\"sourceAccountId\":\"aa\"},\"" \
                  "premiumSourceAccount\":{\"sourceAccountId\":\"aa\"},\"" \
                  "beneficiary\":{\"identificationDocumentDetails\":{\"idType\":\"PASSPORT\",\"" \
                  "idNumber\":\"Passport- 443431, CIN- 123123123\"},\"name\":{\"salutation\":\"MR.\",\"" \
                  "givenName\":\"Javier\",\"middleName\":\"Perez\",\"surname\":\"de Cuellar\"},\"" \
                  "demographics\":{\"gender\":\"MALE\",\"dateOfBirth\":\"1980-01-01\",\"" \
                  "maritalStatus\":\"SINGLE\",\"nationality\":\"SG\"},\"" \
                  "employmentDetails\":{\"occupationCode\":\"ACCOUNTANT\",\"" \
                  "businessNature\":\"BANKING\"},\"additionalData\":{\"relationshipWithPrimary\":\"HUSBAND\"}},\"" \
                  "questionnaire\":{\"questionId\":1,\"answerText\":\"Yes or No\",\"remarks\":\"Health Declartion1\"}}"

        headers = {
            'authorization': "Bearer %s" % access_token,
            'uuid': str(uuid.uuid1()),
            'client_id': Global.get_client_id(),
            'clientdetails': "REPLACE_THIS_VALUE",
            'content-type': "application/json",
            'accept': "application/json"
        }

        conn.request("POST", "/gcb/api/v1/insurance/bookings", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        print('ss')
