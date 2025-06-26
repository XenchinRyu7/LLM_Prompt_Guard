#!/usr/bin/env python3
"""
Test script for LLM Guard PII Detection API
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_api():
    print("=== Testing LLM Guard PII Detection API ===\n")
    
    # Test cases
    test_cases = [
        {
            "name": "Text with PII data",
            "text": "My name is John Doe, email john.doe@example.com, phone (123) 456-7890"
        },
        {
            "name": "Clean text without PII",
            "text": "The weather is beautiful today. I love programming!"
        },
        {
            "name": "Credit card information",
            "text": "Please process payment with card number 4532-1234-5678-9012"
        },
        {
            "name": "Mixed content",
            "text": "Hello, I'm Jane Smith. Visit our website at example.com for more info."
        }
    ]
    
    # Test health endpoint
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Health Check: {response.json()}")
        print()
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return
    
    # Test validation endpoint
    for i, case in enumerate(test_cases, 1):
        print(f"Test {i}: {case['name']}")
        print(f"Input: {case['text']}")
        
        try:
            response = requests.post(
                f"{API_URL}/validate",
                json={"text": case["text"]}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Valid: {result['valid']}")
                print(f"Detected PII: {result['detected']}")
            else:
                print(f"Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_api()
