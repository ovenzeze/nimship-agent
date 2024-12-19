import requests

# API endpoint and headers
url = "http://localhost:4000/models"
headers = {
    "accept": "application/json",
    "x-goog-api-key": "sk-cVek69kBvShIm0DjXPomJQ"
}

def test_get_models():
    try:
        # Send GET request
        response = requests.get(url, headers=headers)

        # Output response for debugging
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

        # Test assertions
        assert response.status_code == 200, "Expected status code 200"
        assert isinstance(response.json(), list), "Expected response to be a list of models"
        print("Test passed: Models list retrieved successfully.")
    except Exception as e:
        print("Test failed:", str(e))

if __name__ == "__main__":
    test_get_models()