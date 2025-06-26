import re

# Contoh string yang mengandung Google Cloud API Key
test_string = "Contoh penggunaan API dengan key: AIzaSyD4C6N3R_example_key1234567890"

# Pola regex untuk mendeteksi Google Cloud API Key
pattern = r"(?i)AIza[A-Za-z0-9-_]{35}"

# Mencari semua kecocokan dengan pola
matches = re.findall(pattern, test_string)

if matches:
    print("Ditemukan Google Cloud API Key:", matches)
else:
    print("Tidak ada Google Cloud API Key yang terdeteksi.")
