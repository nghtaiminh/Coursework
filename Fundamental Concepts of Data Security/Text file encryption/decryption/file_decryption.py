from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ====== Decryption ======

file_to_decrypt = 'encrypted.txt'
key_file = 'key.txt'
# Open input and output files
input_file = open(file_to_decrypt, 'rb')
input_key_file = open(key_file, 'rb') # Output file of the key
output_file = open('decrypted.txt', 'w') # Output file


# Get the key from file contain the key
key = input_key_file.read()

# Read the data from the encrypted file, decrypting then writing to the new file
iv = input_file.read(16) # Read the iv out - this is 16 bytes long
ciphered_data = input_file.read() # Read the rest of the data

cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size).decode() # Decrypt and then up-pad the result

output_file.write(original_data)

# Close the input and output files
input_file.close()
input_key_file.close()
output_file.close()