#!/usr/bin/env python
"""Test AI endpoint through Django"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'himwat.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()

def test_ai_endpoint():
    """Test the AI generation endpoint"""
    print("Creating test client...")
    client = Client()

    # Find a staff user
    print("\nLooking for staff user...")
    staff_user = User.objects.filter(is_staff=True).first()

    if not staff_user:
        print("[ERROR] No staff user found!")
        return False

    print(f"[SUCCESS] Found staff user: {staff_user.username}")

    # Login as staff user
    print(f"\nLogging in as {staff_user.username}...")
    logged_in = client.login(username='pradeep', password='admin123')

    if not logged_in:
        print("[ERROR] Failed to login!")
        return False

    print("[SUCCESS] Logged in successfully")

    # Make API request
    print("\nMaking API request to /dashboard/api/ai/generate/...")
    test_data = {
        'prompt': 'Say "Hello World"',
        'action': 'generate',
        'current_content': ''
    }

    try:
        response = client.post(
            '/dashboard/api/ai/generate/',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print(f"\n[INFO] Response Status Code: {response.status_code}")
        print(f"[INFO] Response Content-Type: {response.get('Content-Type', 'Not set')}")

        if response.status_code == 200:
            print("[SUCCESS] Endpoint returned 200 OK")
            print("\n[INFO] Streaming response content (first 500 chars):")
            content = response.content.decode('utf-8')[:500]
            print(content)
        else:
            print(f"[ERROR] Endpoint returned error status: {response.status_code}")
            print("\n[INFO] Response content:")
            print(response.content.decode('utf-8'))

        return response.status_code == 200

    except Exception as e:
        print(f"[ERROR] Exception during request: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ai_endpoint()
    sys.exit(0 if success else 1)
