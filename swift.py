

# from rave_python import Rave, RaveExceptions, Misc
import requests
from functools import lru_cache
import datetime
import json
from django.conf import settings

TEST_PUBLIC = "FLWPUBK_TEST-60c00b51d6cf9dd5f372c47e9efc8587-X"
TEST_SECRET = "FLWSECK_TEST-c08f710bd7097c8e3f22bf6a3dacab68-X"

class FlutterConnection:

    headers = {
        "Authorization" : "Bearer {}".format(TEST_SECRET),
        "Content-Type" : "application/json"
    }

    def make_request(self, method, url, request_payload=None, header_extensions=None):
        if method=='GET':
            request_object=requests.Request(method=method, url=url, headers=self.headers)
        else:
            request_object=requests.Request(method=method, url=url, data=request_payload, headers=self.headers)

        # Prepare the request by using the Request object
        prepared_request = request_object.prepare()
        # Create a Session object and send the request
        with requests.Session() as session:
            response = session.send(prepared_request)

        return response.json()



endpoint = "https://api.flutterwave.com/v3/payments"
payload= {
  "tx_ref": "hooli-tx-1920bbtytty",
  "amount": "100",
  "currency": "NGN",
  "redirect_url": "https://webhook.site/9d0b00ba-9a69-44fa-a43d-a82c33c36fdc",
  "payment_options": "banktransfer, card",
  "meta": {
    "consumer_id": 23,
    "consumer_mac": "92a3-912ba-1192a"
  },
  "customer": {
    "email": "swifthmd@gmail.com",
    "phonenumber": "08035977671",
    "name": "Yemi Desola"
  },
  "customizations": {
    "title": "Pied Piper Payments",
    "description": "Middleout isn't free. Pay the price",
    "logo": "https://assets.piedpiper.com/logo.png"
  }
}

data = json.dumps(payload)
result= FlutterConnection().make_request("POST", endpoint, data)

print("RES : ",result)




# def process_payment(name,email,amount,phone):
#     auth_token= TEST_SECRET
#     hed = {'Authorization': 'Bearer ' + auth_token}
#     data = {
#             "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
#             "amount":amount,
#             "currency":"NGN",
#             "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment", #"http://localhost:8000/callback",
#             "payment_options":"banktransfer, card",
#             "meta":{
#                 "consumer_id":23,
#                 "consumer_mac":"92a3-912ba-1192a"
#             },
#             "customer":{
#                 "email":email,
#                 "phonenumber":phone,
#                 "name":name
#             },
#             "customizations":{
#                 "title":"Supa Electronics Store",
#                 "description":"Best store in town",
#                 "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
#             }
#             }
#     url = ' https://api.flutterwave.com/v3/payments'
#     response = requests.post(url, json=data, headers=hed)
#     response=response.json()
#     link=response['data']['link']
#     # return link
#     print("LINK : ", link)

# process_payment("Sulaiman Hammed", "officialswiftstand.com", 300, "+2349035977671")



# rave = Rave(TEST_PUBLIC, TEST_SECRET, usingEnv = False)
# # account payload
# payload = {
#    "amount":20000,
#    "PBFPubKey":"ENTER_YOUR_PUBLIC_KEY",
#    "currency":"NGN",
#    "email":"user@example.com",
#    "meta":[
#       {
#          "metaname":"test",
#          "metavalue":"12383"
#       }
#    ],
#    "ip":"123.0.1.3",
#    "firstname":"Flutterwave",
#    "lastname":"Tester"
# }

# try:
#     res = rave.Account.charge(payload)
#     if res["authUrl"]:
#         print(res["authUrl"])

#     elif res["validationRequired"]:
#         rave.Account.validate(res["flwRef"], "12345")

#     res = rave.Account.verify(res["txRef"])
#     print(res)

# except RaveExceptions.AccountChargeError as e:
#     print(e.err)
#     print(e.err["flwRef"])

# except RaveExceptions.TransactionValidationError as e:
#     print(e.err)
#     print(e.err["flwRef"])

# except RaveExceptions.TransactionVerificationError as e:
#     print(e.err["errMsg"])
#     print(e.err["txRef"])