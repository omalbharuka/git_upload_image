import os
import requests
import time
import sys

IG_USER_ID = os.environ['INSTAGRAM_USER_ID']
ACCESS_TOKEN = os.environ['INSTAGRAM_ACCESS_TOKEN']
IMAGE_URL = os.environ['IMAGE_URL']
CAPTION = os.environ.get('CAPTION', 'Posted via GitHub Actions!')

def create_container(image_url, caption):
    """Step 1: Create media container"""
    url = f"https://graph.facebook.com/v24.0/{IG_USER_ID}/media"
    params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    data = response.json()
    
    if 'id' in data:
        print(f"✓ Container created: {data['id']}")
        return data['id']
    else:
        print(f"✗ Error creating container: {data}")
        sys.exit(1)

def check_container_status(container_id):
    """Step 2: Check if container is ready"""
    url = f"https://graph.facebook.com/v24.0/{container_id}"
    params = {
        'fields': 'status_code',
        'access_token': ACCESS_TOKEN
    }
    
    for attempt in range(10):
        response = requests.get(url, params=params)
        data = response.json()
        status = data.get('status_code')
        
        if status == 'FINISHED':
            print(f"✓ Container ready to publish")
            return True
        elif status == 'ERROR':
            print(f"✗ Container processing error")
            sys.exit(1)
        
        print(f"⏳ Waiting... Status: {status} (attempt {attempt + 1}/10)")
        time.sleep(5)
    
    print("✗ Timeout waiting for container")
    sys.exit(1)

def publish_container(container_id):
    """Step 3: Publish the container"""
    url = f"https://graph.facebook.com/v24.0/{IG_USER_ID}/media_publish"
    params = {
        'creation_id': container_id,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    data = response.json()
    
    if 'id' in data:
        print(f"✓ Published! Media ID: {data['id']}")
        return data['id']
    else:
        print(f"✗ Publish error: {data}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== Instagram Publishing Script ===")
    container_id = create_container(IMAGE_URL, CAPTION)
    check_container_status(container_id)
    media_id = publish_container(container_id)
    print(f"=== Success! Check Instagram for post {media_id} ===")
