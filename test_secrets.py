from llm_guard.input_scanners import Anonymize
from llm_guard.vault import Vault

vault = Vault()

scanner = Anonymize(vault=vault)

prompt = """
Given the personal profile of Johnathan Edward Doe, please summarize the following resume:

Profile:

- Full Name: Johnathan Edward Doe.
- Date of Birth: April 12, 1990.
- Address: 123 Elm Street, Springfield, IL, 62701.
- Email: john.doe@example.com.
- Phone Number: (123) 456-7890.
- Educational Background:
    - Springfield High School, Graduated in 2008;
    - Springfield University, B.Sc. Computer Science, Graduated in 2012.
- Employment:
    - ABC Tech Solutions, Software Engineer, 2012-2015;
    - XYZ Global Systems, Senior Software Developer, 2015-2021.
"""

sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)

print("Sanitized Prompt:\n", sanitized_prompt)
print("\nIs Valid:", is_valid)
print("Risk Score:", risk_score)
