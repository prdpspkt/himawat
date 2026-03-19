#!/usr/bin/env python
"""Test AI API connection"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'himwat.settings')
django.setup()

from dashboard.models import AIConfiguration
from openai import OpenAI

def test_ai_connection():
    """Test the AI API connection"""
    print("Fetching active AI configuration...")
    ai_config = AIConfiguration.get_active()

    if not ai_config:
        print("[ERROR] No active AI configuration found!")
        return False

    print(f"[SUCCESS] Found config: {ai_config.name}")
    print(f"   Model: {ai_config.model_name}")
    print(f"   Endpoint: {ai_config.api_endpoint}")
    print(f"   API Key: {ai_config.api_key[:10]}...{ai_config.api_key[-5:] if len(ai_config.api_key) > 15 else ''}")

    try:
        print("\nInitializing OpenAI client...")
        client = OpenAI(
            api_key=ai_config.api_key,
            base_url=ai_config.api_endpoint
        )
        print("[SUCCESS] Client initialized successfully")

        print("\nTesting API connection with simple request...")
        response = client.chat.completions.create(
            model=ai_config.model_name,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'Say "API connection successful!"'}
            ],
            max_tokens=50,
            stream=False
        )

        content = response.choices[0].message.content
        print(f"[SUCCESS] API Response: {content}")
        return True

    except Exception as e:
        print(f"[ERROR] API Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ai_connection()
    sys.exit(0 if success else 1)
