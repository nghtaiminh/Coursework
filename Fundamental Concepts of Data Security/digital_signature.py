from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384

message = b'123456'

# ===== Creating a signature =====
key = RSA.generate(2048)
private_key = key


signer = PKCS1_v1_5.new(private_key)
hash_object = SHA384.new(message)

signature = signer.sign(hash_object)

# ===== Verifying a signature =====

public_key = key.publickey()
verifier = PKCS1_v1_5.new(public_key)

hash_object = SHA384.new()
hash_object.update(message)
if verifier.verify(hash_object, signature):
    print('The signature is authentic.')
else:
    print('The signature is not authentic.')