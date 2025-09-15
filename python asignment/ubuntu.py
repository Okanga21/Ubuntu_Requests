import os
import requests
from urllib.parse import urlparse
import hashlib

# Directory to save images
SAVE_DIR = "Fetched_Images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Keep track of downloaded image hashes to avoid duplicates
downloaded_hashes = set()


def is_safe_content(response):
    """
    Check if the HTTP headers suggest this is a safe image to download.
    - Only allow common image MIME types.
    - Respect content length if available.
    """
    content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        print(f"⚠️ Skipped: Content type '{content_type}' is not an image.")
        return False

    # Optional: limit file size (e.g., max 10MB)
    content_length = response.headers.get("Content-Length")
    if content_length and int(content_length) > 10 * 1024 * 1024:
        print("⚠️ Skipped: File too large (>10MB).")
        return False

    return True


def get_file_hash(content):
    """Generate a hash for the content to detect duplicates."""
    return hashlib.sha256(content).hexdigest()


def fetch_image(url):
    """Fetch and save a single image from the given URL safely."""
    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Safety check: ensure it's really an image
        if not is_safe_content(response):
            return

        # Read content
        content = response.content
        file_hash = get_file_hash(content)

        # Prevent duplicate downloads
        if file_hash in downloaded_hashes:
            print("⏩ Skipped duplicate image.")
            return
        downloaded_hashes.add(file_hash)

        # Extract filename or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename or "." not in filename:  # No proper filename
            filename = f"image_{len(downloaded_hashes)}.jpg"

        save_path = os.path.join(SAVE_DIR, filename)

        # Save safely in binary mode
        with open(save_path, "wb") as f:
            f.write(content)

        print(f"✅ Image saved: {save_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error: {http_err}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Check your internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")


def main():
    print("🌐 Multi-Image Fetcher (separate multiple URLs with spaces)")
    print("Type 'exit' to quit.\n")

    while True:
        urls = input("Enter image URL(s): ").strip()
        if urls.lower() == "exit":
            print("👋 Exiting. All done!")
            break

        url_list = urls.split()
        for url in url_list:
            fetch_image(url)


if __name__ == "__main__":
    main()
