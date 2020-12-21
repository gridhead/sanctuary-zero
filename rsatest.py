import base64
import rsa

strg = "A QUICK BROWN FOX JUMPED OVER A LAZY FOX " + \
       "A QUICK BROWN FOX JUMPED OVER A LAZY FOX " + \
       "A QUICK BROWN FOX JUMPED OVER A LAZY FOX " + \
       "A QUICK BROWN FOX JUMPED OVER A LAZY FOX " + \
       "A QUICK BROWN FOX JUMPED OVER A LAZY FOX " + \
       "A QUICK BROWN FOX JUMPED OVER A LAZY FOX"

print(len(strg))

# ENCRYPTION AND DECRYPTION

def encryption_and_decryption():
    publckey, privtkey = rsa.newkeys(2048, poolsize=8)
    byte = strg.encode("utf-8")
    encr = rsa.encrypt(byte, publckey)
    b64e = base64.b64encode(encr).decode("utf-8")
    tr64 = base64.b64decode(b64e.encode("utf-8"))
    decr = rsa.decrypt(tr64, privtkey)
    strd = decr.decode("utf-8")
    print(strd)

# SIGNING AND VERIFICATION
publckey, privtkey = rsa.newkeys(512)


byte = strg.encode("utf-8")
hush = rsa.compute_hash(byte, 'SHA-1')

print(hush)

signature = rsa.sign_hash(hush, privtkey, 'SHA-256')
print(signature)

bytc = strg.encode('utf-8')
print(rsa.verify(bytc, signature, publckey))
