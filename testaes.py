from Crypto.Cipher import AES
import base64
import os
from binascii import b2a_hex, a2b_hex, b2a_base64, a2b_base64

BLOCK_SIZE = 16
PADDING = " "

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

KEY = os.urandom(BLOCK_SIZE)
IV = os.urandom(BLOCK_SIZE)

cipher = AES.new(KEY, AES.MODE_CBC, IV)
dcipher = AES.new(KEY, AES.MODE_CBC, IV)

print 'IV:', base64.b64encode(IV)

encoded = EncodeAES(cipher, 'cckk')
print 'Encrypted string:', encoded

decoded = DecodeAES(dcipher, encoded)
print 'Decrypted string:', decoded
