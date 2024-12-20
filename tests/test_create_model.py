import requests

# API endpoint and headers
url = "http://localhost:4000/model/new"
headers = {
    "api_key_header": "sk-cVek69kBvShIm0DjXPomJQ",
    "Content-Type": "application/json"
}

# Request payload
payload = {
    "model_name": "Titan Text Large",
    "litellm_params": {
        "custom_llm_provider": "Amazon",
        "aws_access_key_id": "***REMOVED***",
        "aws_secret_access_key": "***REMOVED***",
        "aws_region_name": "us-east-1",
        "model": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-tg1-large",
        "timeout": 60,
        "max_retries": 3
    },
    "model": "amazon.titan-tg1-large",
    "model_info": {
        "id": "amazon.titan-tg1-large",
        "db_model": False,
        "base_model": "Titan Text Large",
        "providerName": "Amazon"
    }
}

# Send POST request
def create_model():
    try:
        response = requests.post(url, headers=headers, json=payload)

        # Print response for debugging
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

        # Test success condition
        if response.status_code == 201:
            print("Model created successfully!")
        else:
            print("Failed to create model:", response.json())
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    create_model()