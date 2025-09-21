# Caesar Cipher Program

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():  # Encrypt only letters
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char  # keep spaces, numbers, punctuation unchanged
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

# Main Program
print("=== Caesar Cipher Encryption & Decryption ===")
message = input("Enter your message: ")
shift = int(input("Enter shift value (e.g., 3): "))

encrypted = encrypt(message, shift)
decrypted = decrypt(encrypted, shift)

print("\nEncrypted message:", encrypted)
print("Decrypted message:", decrypted)
