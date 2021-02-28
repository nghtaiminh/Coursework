from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# ===== Encryption =====

file_to_encrypt = 'message.txt'
key_file = 'key.txt'

# Open input and output files
input_file = open(file_to_encrypt, 'rb')
output_file = open('encrypted.txt', 'wb')  # Output file that contain the encrypted data
output_key_file = open(key_file, 'wb')  # Output file of the key

# Generate a key and store in a file
key = get_random_bytes(16) 
output_key_file.write(key)

# Create cipher object and encrypt the data
data = input_file.read()
cipher = AES.new(key, AES.MODE_CBC) # Create a AES cipher object with the key using the mode CBC (Cipher block chaining)
ciphered_data = cipher.encrypt(pad(data, AES.block_size)) # Pad the input data and then encrypt

output_file.write(cipher.iv) 
output_file.write(ciphered_data) 


input_file.close()
output_file.close()
output_key_file.close()
