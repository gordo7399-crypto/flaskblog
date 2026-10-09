import requests
import json

# Target URL for your running Flask application
TARGET_URL = "http://127.0.0.1:5000/login"

# Test Payload Suite: Designed to attempt backend crashes and database buffer overflows
test_cases = [
    {
        "name": "1. Malformed JSON Syntax (Broken Bracket)",
        "headers": {"Content-Type": "application/json"},
        "data": '{"email": "test@example.com", "password":', # Intentionally unclosed JSON string
        "expected_status": 400
    },
    {
        "name": "2. Missing Content-Type Header",
        "headers": {"Content-Type": "text/plain"},
        "data": '{"email": "test@example.com", "password": "Password123!"}',
        "expected_status": 400
    },
    {
        "name": "3. Type Injection Attack (Integer Password)",
        "headers": {"Content-Type": "application/json"},
        "data": json.dumps({"email": "test@example.com", "password": 123456789}),
        "expected_status": 422
    },
    {
        "name": "4. Null Value Injection",
        "headers": {"Content-Type": "application/json"},
        "data": json.dumps({"email": None, "password": None}),
        "expected_status": 422
    },
    {
        "name": "5. Database Buffer Overflow Attack (100,000-character payload)",
        "headers": {"Content-Type": "application/json"},
        "data": json.dumps({"email": "A" * 100000 + "@example.com", "password": "B" * 100000}),
        "expected_status": [400, 422, 401] # Caught gracefully without crashing DB
    },
    {
        "name": "6. SQL Injection Pattern",
        "headers": {"Content-Type": "application/json"},
        "data": json.dumps({"email": "' OR '1'='1", "password": "' OR '1'='1"}),
        "expected_status": 401
    },
    {
        "name": "7. Invalid Authentication Credentials",
        "headers": {"Content-Type": "application/json"},
        "data": json.dumps({"email": "nonexistent_user@example.com", "password": "WrongPassword!"}),
        "expected_status": 401
    }
]


def run_hard_tests():
    print("\n=======================================================")
    print(" STARTING BACKEND HARD-TEST SUITE FOR ERROR ROUTINES ")
    print("=======================================================\n")

    passed_count = 0

    for idx, test in enumerate(test_cases, 1):
        print(f"Executing Test {idx}: {test['name']}")
        
        try:
            # Send HTTP request to local server
            response = requests.post(TARGET_URL, data=test['data'], headers=test['headers'])
            status = response.status_code
            
            try:
                response_json = response.json()
            except Exception:
                response_json = {"message": "Non-JSON response returned"}

            # Check if status code matches expected failure codes
            expected = test['expected_status']
            is_valid_status = status in expected if isinstance(expected, list) else status == expected

            if is_valid_status:
                print(f"  [PASS] Status Code: {status}")
                print(f"         Returned Message: '{response_json.get('message', 'N/A')}'")
                passed_count += 1
            else:
                print(f"  [FAIL] Unexpected Status Code: {status}")
                print(f"         Response Body: {response.text}")

        except requests.exceptions.ConnectionError:
            print("  [CRITICAL FAIL] Could not connect to server. Is Flask running on http://127.0.0.1:5000?")
            return

        print("-" * 55)

    print(f"\nTEST SUMMARY: {passed_count}/{len(test_cases)} Hard Tests Passed Cleanly.\n")


if __name__ == "__main__":
    run_hard_tests()