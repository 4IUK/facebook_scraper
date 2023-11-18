import os
import requests
import shutil

def download_image_from_facebook(url, output_path):
    try:
        # Create the "unknown" directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Download the image from the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check the status of the request

        # Store the image to a file
        with open(output_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        print(f"Image has been downloaded and stored at: {output_path}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

'''
from get import download_image_from_facebook

# URL của ảnh trong một bài đăng Facebook
url = "https://scontent.fhan4-2.fna.fbcdn.net/v/t39.30808-6/402398687_734233355414669_1276441216685779263_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=5f2048&_nc_ohc=9fn0az0cwwYAX8KVp0L&_nc_ht=scontent.fhan4-2.fna&oh=00_AfDZ2HoxdA_LCLsdpRrsJf3oacvB57Vjdw49ePud1-sfpg&oe=655C7B2B"

# Đường dẫn để lưu trữ ảnh cục bộ
output_path = "./unknown/downloaded_image.jpg"

# Gọi hàm để tải ảnh và lưu trữ
download_image_from_facebook(url, output_path)

'''