from PIL import Image
import numpy as np

# ---------- Method 1: XOR Encryption ----------
def xor_encrypt_decrypt(input_path, output_path, key=50):
    img = Image.open(input_path)
    img_array = np.array(img)

    # XOR every pixel value with the key
    encrypted_array = img_array ^ key

    result_img = Image.fromarray(encrypted_array)
    result_img.save(output_path)
    print(f"Saved: {output_path}")

# ---------- Method 2: Pixel Swap Encryption ----------
def swap_encrypt(input_path, output_path):
    img = Image.open(input_path)
    img_array = np.array(img)

    # Swap pixels: flip image horizontally + vertically
    swapped_array = img_array[::-1, ::-1]

    result_img = Image.fromarray(swapped_array)
    result_img.save(output_path)
    print(f"Saved: {output_path}")

def swap_decrypt(input_path, output_path):
    # Decryption is just swapping again
    swap_encrypt(input_path, output_path)

# ---------- Main Program ----------
if __name__ == "__main__":
    input_image = "input.jpg"   # your original image
    encrypted_image1 = "encrypted_xor.png"
    decrypted_image1 = "decrypted_xor.png"
    encrypted_image2 = "encrypted_swap.png"
    decrypted_image2 = "decrypted_swap.png"

    # Method 1: XOR
    print("\n--- XOR ENCRYPTION ---")
    xor_encrypt_decrypt(input_image, encrypted_image1, key=123)
    xor_encrypt_decrypt(encrypted_image1, decrypted_image1, key=123)

    # Method 2: Pixel Swap
    print("\n--- SWAP ENCRYPTION ---")
    swap_encrypt(input_image, encrypted_image2)
    swap_decrypt(encrypted_image2, decrypted_image2)
