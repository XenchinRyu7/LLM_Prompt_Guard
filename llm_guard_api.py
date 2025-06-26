# pip install fastapi uvicorn llm-guard

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from llm_guard.input_scanners import Anonymize
from llm_guard.vault import Vault

app = FastAPI(title="LLM Guard PII Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vault = Vault()
# Configure Anonymize with specific entity types and thresholds
pii_scanner = Anonymize(
    vault=vault,
    entity_types=["EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "US_SSN", "IP_ADDRESS", "CRYPTO", "IBAN_CODE", "US_BANK_NUMBER", "UUID"],
    use_faker=False,
    threshold=0.8  # Higher threshold to reduce false positives
)

class ValidationRequest(BaseModel):
    text: str

class ValidationResponse(BaseModel):
    valid: bool
    detected: List[str]
    redacted: str

def restore_pronouns(redacted_text: str, original_text: str) -> str:
    """
    Clean up redacted text - merge split emails and phone numbers.
    """
    import re
    result = redacted_text
    
    # Merge consecutive EMAIL_ADDRESS redactions
    result = re.sub(r'\[REDACTED_EMAIL_ADDRESS_\d+\]\[REDACTED_EMAIL_ADDRESS_\d+\]', '[REDACTED_EMAIL_ADDRESS]', result)
    
    # Merge consecutive PHONE_NUMBER redactions  
    result = re.sub(r'\[REDACTED_PHONE_NUMBER_\d+\]\[REDACTED_PHONE_NUMBER_\d+\]', '[REDACTED_PHONE_NUMBER]', result)
    
    # Clean up numbered redactions to be simpler
    result = re.sub(r'\[REDACTED_EMAIL_ADDRESS_\d+\]', '[REDACTED_EMAIL_ADDRESS]', result)
    result = re.sub(r'\[REDACTED_PHONE_NUMBER_\d+\]', '[REDACTED_PHONE_NUMBER]', result)
    result = re.sub(r'\[REDACTED_CREDIT_CARD_\d+\]', '[REDACTED_CREDIT_CARD]', result)
    result = re.sub(r'\[REDACTED_US_SSN_\d+\]', '[REDACTED_US_SSN]', result)
    result = re.sub(r'\[REDACTED_IP_ADDRESS_\d+\]', '[REDACTED_IP_ADDRESS]', result)
    
    return result

@app.post("/validate", response_model=ValidationResponse)
async def validate_text(request: ValidationRequest):
    """
    Validate text for PII (Personally Identifiable Information) detection.
    Returns whether the text is valid (no PII detected), list of detected PII types, dan prompt yang sudah di-redact.
    """
    try:
        sanitized_prompt, is_valid, risk_score = pii_scanner.scan(request.text)
        
        detected_types = []
        if not is_valid:
            detected_types = _extract_detected_types(request.text, sanitized_prompt)
        
        sanitized_prompt = restore_pronouns(sanitized_prompt, request.text)
        
        return ValidationResponse(
            valid=is_valid,
            detected=detected_types,
            redacted=sanitized_prompt
        )
    
    except Exception as e:
        return ValidationResponse(
            valid=False,
            detected=[f"ERROR: {str(e)}"],
            redacted=""
        )

def _extract_detected_types(original_text: str, sanitized_text: str) -> List[str]:
    """
    Extract detected PII types by analyzing differences between original and sanitized text.
    """
    detected_types = set()
    
    import re
    
    redacted_patterns = {
        r'\[REDACTED_PERSON_\d+\]': 'PERSON',
        r'\[REDACTED_EMAIL_ADDRESS_\d+\]': 'EMAIL_ADDRESS', 
        r'\[REDACTED_PHONE_NUMBER_\d+\]': 'PHONE_NUMBER',
        r'\[REDACTED_CREDIT_CARD_\d+\]': 'CREDIT_CARD',
        r'\[REDACTED_US_SSN_\d+\]': 'US_SSN',
        r'\[REDACTED_IP_ADDRESS_\d+\]': 'IP_ADDRESS',
        r'\[REDACTED_CRYPTO_\d+\]': 'CRYPTO',
        r'\[REDACTED_IBAN_CODE_\d+\]': 'IBAN_CODE',
        r'\[REDACTED_US_BANK_NUMBER_\d+\]': 'US_BANK_NUMBER',
        r'\[REDACTED_UUID_\d+\]': 'UUID',
        r'\[REDACTED_CREDIT_CARD_RE_\d+\]': 'CREDIT_CARD',
        r'\[REDACTED_EMAIL_ADDRESS_RE_\d+\]': 'EMAIL_ADDRESS',
        r'\[REDACTED_US_SSN_RE_\d+\]': 'US_SSN',
    }
    
    for pattern, pii_type in redacted_patterns.items():
        if re.search(pattern, sanitized_text):
            detected_types.add(pii_type)
    
    return list(detected_types)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "LLM Guard PII Detection API"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "LLM Guard PII Detection API",
        "version": "1.0.0",
        "endpoints": {
            "validate": "POST /validate - Validate text for PII detection",
            "health": "GET /health - Health check"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
