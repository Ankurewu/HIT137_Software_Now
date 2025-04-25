import string

INPUT_FILE = "raw_text.txt"
OUTPUT_FILE = "encrypted_text.txt"

def shift_char(char, shift, base, limit=13):
    return chr(((ord(char) - base + shift) % limit) + base)

def encrypt_char(char, n, m):
    if char.islower():
        return (
            shift_char(char, n * m, ord('a')) if char <= 'm'
            else shift_char(char, -(n + m), ord('n'))
        )
    elif char.isupper():
        return (
            shift_char(char, -n, ord('A')) if char <= 'M'
            else shift_char(char, m ** 2, ord('N'))
        )
    return char

def decrypt_char(char, n, m):
    if char.islower():
        return (
            shift_char(char, -(n * m), ord('a')) if char <= 'm'
            else shift_char(char, (n + m), ord('n'))
        )
    elif char.isupper():
        return (
            shift_char(char, n, ord('A')) if char <= 'M'
            else shift_char(char, -(m ** 2), ord('N'))
        )
    return char

def encrypt_content(content, n, m):
    return ''.join(encrypt_char(c, n, m) for c in content)

def decrypt_content(content, n, m):
    return ''.join(decrypt_char(c, n, m) for c in content)

def run_cipher():
    try:
        n = int(input("🔢 Enter value for n: "))
        m = int(input("🔢 Enter value for m: "))

        with open(INPUT_FILE, "r", encoding="utf-8") as infile:
            text = infile.read()

        encrypted_text = encrypt_content(text, n, m)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
            outfile.write(encrypted_text)

        decrypted_text = decrypt_content(encrypted_text, n, m)

        if text == decrypted_text:
            print("✅ Encryption and decryption are working correctly!")
        else:
            print("❌ Decryption mismatch detected.")

    except ValueError:
        print("Please provide valid integer inputs for n and m.")
    except FileNotFoundError:
        print("Input file not found. Make sure 'raw_text.txt' exists.")
    except UnicodeDecodeError:
        print("Encoding issue: Non-decodable characters found.")
    except IOError:
        print("File read/write error.")
    except PermissionError:
        print("Cannot write to file — permission denied.")

if __name__ == "__main__":
    run_cipher()
