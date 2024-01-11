import requests
from functools import lru_cache
import datetime
import json
from django.conf import settings


PUBLIC_VAL = settings.PUBLIC_KEY
SECRET_VAL = settings.SECRET_KEY

class FlutterConnection:

    headers = {
        "Authorization" : "Bearer {}".format(SECRET_VAL),
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


def initialize_transaction(transaction_body):
    endpoint = "https://api.flutterwave.com/v3/payments"
    data = json.dumps(transaction_body
                      )
    return FlutterConnection().make_request("POST", endpoint, data)

def verify_transaction(trans_id):
    endpoint = f"https://api.flutterwave.com/v3/transactions/{trans_id}/verify"
    return FlutterConnection().make_request("GET", endpoint)


def verify_by_reference(reference):
    endpoint = f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={reference}"
    return FlutterConnection().make_request("GET", endpoint)
