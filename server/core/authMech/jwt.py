"""
This is Json Web Token(JWT) module for authorization mechanism in endpoints/ APIs services.
It follows RFC 7519 guidelines and easy maintainable, bare computational needs.
It is featured with configurable token expiry and token hash algo validation.
"""
# Author : Krishnasagar <pagesagar@gmailcom>

import json
import base64
import hashlib
import hmac
import time


# References:
# https://hdknr.github.io/docs/identity/impl_jws.html
# https://codereview.stackexchange.com/questions/150063/validating-hmac-sha256-signature-in-python
# https://jwt.io/introduction/
# http://www.seedbox.com/en/blog/2015/06/05/oauth-2-vs-json-web-tokens-comment-securiser-un-api/
# https://zapier.com/engineering/apikey-oauth-jwt/

# claim keys derived from RFC7519
KEY_ISSUED_AT = 'iat'
KEY_SUBJECT = "sub"
KEY_AUDIENCE = "aud"


class JWTException(Exception):
    pass


class JWT(object):
    """
    JSON Web Token(JWT) protocol customized.
    Base guidelines set to RFC7519.
    Default algorithm = HmacSHA256

    Token formulation:
    header, payload,
    signature ==> HMACSHA256(base64URLEncode(header) +"."+ base64URLEncode(payload), SK)

    Payload and SK(Secret Key) should be provided for token generation.
    """
    __version__ = '0.1.0'

    def __init__(self, SK, algo='HS256', token_expiry=None):
        """
        SK = Secret Key for signature type string

        Optional parameters:
        algo = Algorithm for signature type string
        token_expiry = expiry for token in seconds
        """
        self.header = {
            "alg": algo,
            "typ": "JWT"
        }
        self.tkalg = algo
        self.SK = SK.encode('utf-8')
        self.encsafe_str = "."
        self.tk_expiry = token_expiry and token_expiry * 1000

    @staticmethod
    def encode(data):
        """
        Encodes to base64 urlsafe.
        :param data: input to encode
        :return: string plain text
        """
        # data is converted to json string as any typed data can be encoded.
        return base64.urlsafe_b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')

    @staticmethod
    def decode(enc_data):
        """
        Decodes encoded data from base64 urlsafe.
        :param enc_data: encoded data input.
        :return: decoded data
        """
        return json.loads(base64.urlsafe_b64decode(enc_data))

    def sign_prep(self, packet):
        if self.header['alg'] == self.tkalg:
            return hmac.new(self.SK, packet.encode('utf-8'), hashlib.sha256).hexdigest()

    def curr_time(self):
        return int(time.time() * 1000)  # milliseconds

    def tokenize(self, payload=None):
        """
        Generate JWT with:
        payload type preference = dict
        returns JWT
        """
        if isinstance(payload, dict):
            payload[KEY_ISSUED_AT] = self.curr_time()
        msg = self.encode(self.header) + self.encsafe_str + self.encode(payload)
        return msg + self.encsafe_str + self.sign_prep(msg)

    def parse_token(self, rtoken):
        """
        Parses received token and raised for any tamper of token as per formation
        :param rtoken: JWT token string
        :return: payload object
        """
        try:
            rheader, rpayload, rsign = rtoken.split(self.encsafe_str)
            if hmac.compare_digest(rsign, self.sign_prep(rheader + self.encsafe_str + rpayload)):
                # Signature matched. Token is genuine.
                rpayload = self.decode(rpayload)
                # Check for token expiry.
                if not rpayload[KEY_ISSUED_AT]:
                    raise JWTException('No timestamp in token found.')
                elif self.tk_expiry and (abs(rpayload[KEY_ISSUED_AT] - self.curr_time()) > self.tk_expiry):
                    raise JWTException('Received token is expired.')
                return rpayload
            else:
                raise JWTException('Received token signature is invalid.')
        except Exception as e:
            raise e

    def detokenize(self, rtoken):
        """
        Detokenizes of received JWT. It will return JWT data derived from rtoken
        :param rtoken: input JWT
        :return: Decoded payload of received JWT
        """
        try:
            return self.parse_token(rtoken)
        except Exception as e:
            print(str(e))
            raise JWTException(e)


if __name__ == '__main__':
    JWT = JWT('dfd98724548asbd#%%^*&!@#$', token_expiry=2)
    tk = JWT.tokenize({'key': '23492woih9890324876712e<<myJWT>>'})
    print("Token generated %s" % (tk))
    time.sleep(1)
    print(JWT.detokenize(tk))
    tk = JWT.tokenize({'key': '23492woih9890324876712f<<myJWT>>'})
    print("Token generated %s" % (tk))
    time.sleep(3)
    print(JWT.detokenize(tk))