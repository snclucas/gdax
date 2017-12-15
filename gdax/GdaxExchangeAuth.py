import hmac, hashlib, time, base64, math
from requests.auth import AuthBase


class GdaxExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())

        if request.body is not None:
            r = request.body.decode()
        else:
            r = request.body

        message = timestamp + request.method + request.path_url + (r or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        time.localtime(time.time())
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
