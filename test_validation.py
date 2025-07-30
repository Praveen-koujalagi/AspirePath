#!/usr/bin/env python3
"""
Test script to verify email validation and other validation functions work correctly.
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers import validate_email, validate_password, validate_name

def test_email_validation():
    """Test email validation function"""
    print("Testing Email Validation:")
    print("-" * 30)
    
    # Valid emails
    valid_emails = [
        "user@example.com",
        "test.email@domain.co.uk",
        "user123@gmail.com",
        "first.last@company.org",
        "user+tag@example.net"
    ]
    
    # Invalid emails
    invalid_emails = [
        "invalid",
        "user@",
        "@domain.com",
        "user@domain",
        "user..name@domain.com",
        "user@domain..com",
        ""
    ]
    
    print("Valid emails:")
    for email in valid_emails:
        result = validate_email(email)
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {email:<25} - {status}")
    
    print("\nInvalid emails:")
    for email in invalid_emails:
        result = validate_email(email)
        status = "✅ PASS" if not result else "❌ FAIL"
        print(f"  {email:<25} - {status}")

def test_password_validation():
    """Test password validation function"""
    print("\n\nTesting Password Validation:")
    print("-" * 30)
    
    # Valid passwords
    valid_passwords = [
        "Password123!",
        "MySecure@Pass1",
        "Strong#Pass99",
        "Complex$123abc"
    ]
    
    # Invalid passwords
    invalid_passwords = [
        "weak",
        "password123",
        "PASSWORD123",
        "Password123",
        "Pass@1",
        ""
    ]
    
    print("Valid passwords:")
    for password in valid_passwords:
        is_valid, message = validate_password(password)
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"  {password:<20} - {status}")
        if not is_valid:
            print(f"    Error: {message}")
    
    print("\nInvalid passwords:")
    for password in invalid_passwords:
        is_valid, message = validate_password(password)
        status = "✅ PASS" if not is_valid else "❌ FAIL"
        print(f"  {password:<20} - {status}")
        if not is_valid:
            print(f"    Error: {message}")

def test_name_validation():
    """Test name validation function"""
    print("\n\nTesting Name Validation:")
    print("-" * 30)
    
    # Valid names
    valid_names = [
        "John Doe",
        "Alice Smith",
        "Mary Jane Watson",
        "Jean-Pierre",
        "Anna"
    ]
    
    # Invalid names
    invalid_names = [
        "A",
        "John123",
        "Name@Domain",
        "",
        "   ",
        "123456"
    ]
    
    print("Valid names:")
    for name in valid_names:
        result = validate_name(name)
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:<20} - {status}")
    
    print("\nInvalid names:")
    for name in invalid_names:
        result = validate_name(name)
        status = "✅ PASS" if not result else "❌ FAIL"
        print(f"  {name:<20} - {status}")

if __name__ == "__main__":
    print("AspirePath Validation Functions Test")
    print("=" * 50)
    
    try:
        test_email_validation()
        test_password_validation()
        test_name_validation()
        
        print("\n" + "=" * 50)
        print("All validation tests completed!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
