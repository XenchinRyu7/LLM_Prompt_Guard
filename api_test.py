from llm_guard.input_scanners import Secrets

# Inisialisasi scanner dengan mode redaksi 'partial'
scanner = Secrets(redact_mode="partial")

# Contoh teks yang mengandung API key
prompt = """
Berikut adalah beberapa API key:
- OpenAI: sk-1234567890abcdef
- Google Cloud: AIzaSyD4C6N3R_example_key
- AWS: AKIAIOSFODNN7EXAMPLE
"""

# Lakukan pemindaian
sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)

# Tampilkan hasil
print("=== Teks Setelah Disamarkan ===")
print(sanitized_prompt)

print("\n=== Status Validitas ===")
print("Valid:", is_valid)
print("Skor Risiko:", risk_score)
