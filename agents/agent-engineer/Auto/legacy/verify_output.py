#!/usr/bin/env python3
"""
Simple verification script to check if the advanced transformation module is working
"""
import json
from plugins.advanced_transformation_module import transform

def test_transformation():
    # Test with a sample record
    sample_record = {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-1234",
        "value": 123.45,
        "category": "A",
        "timestamp": "2023-01-15T10:30:00Z",
        "description": "Sample record 1"
    }

    print("Original record:")
    print(json.dumps(sample_record, indent=2))

    transformed = transform(sample_record)

    print("\nTransformed record:")
    print(json.dumps(transformed, indent=2))

    print("\nVerification:")
    print(f"- Quality score: {transformed.get('_quality_score', 'N/A')}")
    print(f"- Processed at: {transformed.get('_processed_at', 'N/A')}")
    print(f"- Transform version: {transformed.get('_transform_version', 'N/A')}")
    print(f"- Record hash: {transformed.get('_record_hash', 'N/A')[:16]}...")

    if 'email' in transformed:
        print(f"- Email domain: {transformed.get('email_domain', 'N/A')}")
    if 'phone' in transformed:
        print(f"- Phone formatted: {transformed.get('phone_formatted', 'N/A')}")

if __name__ == "__main__":
    test_transformation()