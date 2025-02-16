def format_post_content(message):
    return {
        'message': message
    }

def handle_api_request(url, payload, access_token):
    import requests
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()