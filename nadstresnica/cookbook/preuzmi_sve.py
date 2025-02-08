# import requests
# from bs4 import BeautifulSoup
# import os
# from urllib.parse import urljoin
# import time
# import random
# import json

# # URL of the webpage
# url = "https://www.srbija.gov.rs/dokument/844348/dokumenta-ministarstva-gradjevinarstva-saobracaja-i-infrastrukture-koja-se-ticu-moguceg-izvrsenja-krivicnog-dela-povodom-pada-nadstresnice-na-zeleznickoj-stanici-u-novom-sadu-1-novembra-2024-godine-22.php"

# # Directory to save downloaded files
# output_dir = "str-2-downloaded_documents"
# os.makedirs(output_dir, exist_ok=True)

# # List to store downloaded links
# downloaded_links = []

# # Send HTTP GET request to the URL
# response = requests.get(url)
# response.raise_for_status()

# # Parse the webpage content
# soup = BeautifulSoup(response.content, "html.parser")

# # File extensions to look for
# file_extensions = [".pdf", ".zip", ".rar", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"]

# # Find all links
# for link in soup.find_all("a", href=True):
#     href = link["href"]
#     link_title = link.get_text(strip=True)
#     if any(href.lower().endswith(ext) for ext in file_extensions):
#         file_url = urljoin(url, href)
#         file_name = os.path.join(output_dir, os.path.basename(href))

#         # Download the file
#         try:
#             print(f"Downloading {file_url}...")
#             file_response = requests.get(file_url)
#             file_response.raise_for_status()
#             with open(file_name, "wb") as f:
#                 f.write(file_response.content)
#             print(f"Saved to {file_name}")

#             # Save the link to the list
#             downloaded_links.append({
#                 "file_name": file_name,
#                 "file_url": file_url,
#                 "link_title": link_title
#             })
#             print(f"------------------LINK TITLE-----------------------------")
#             print(link_title)
#             print(f"---------------------------------------------------------")
#         except requests.RequestException as e:
#             print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#             print(f">>>>>>>>>>>>>>>>>>>>>>>> Failed to download {file_url}: {e} >>>>>>>>>>>>>>>>>>>>>")
#             print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

#         # Add a random delay between downloads
#         time_delay = random.uniform(2, 5)  # Random delay between 2 to 5 seconds
#         print(f"Waiting for {time_delay:.2f} seconds before the next download...")
#         time.sleep(time_delay)

# # Save the links to a JSON file
# json_path = os.path.join(output_dir, "str-2-downloaded_documents.json")
# with open(json_path, "w", encoding="utf-8") as json_file:
#     json.dump(downloaded_links, json_file, indent=4, ensure_ascii=False)

# print("Download completed.")

import json
import os
import random
import sys  # For flushing printed output
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://infrazs.rs/dokumenta_o_padu_nadstresnice/"

# Directory to save downloaded files
output_dir = "dokumenta-zeleznica-srbije"
os.makedirs(output_dir, exist_ok=True)

# List to store downloaded links
downloaded_links = []

# Send HTTP GET request to the URL
response = requests.get(url)
response.raise_for_status()

# Parse the webpage content
soup = BeautifulSoup(response.content, "html.parser")

# File extensions to look for
file_extensions = [".pdf", ".zip", ".rar", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"]

# Find all links
for link in soup.find_all("a", href=True):
    href = link["href"]
    link_title = link.get_text(strip=True)
    if any(href.lower().endswith(ext) for ext in file_extensions):
        file_url = urljoin(url, href)
        file_name = os.path.join(output_dir, os.path.basename(href))

        # Download the file using streaming
        try:
            print(f"Downloading {file_url}...")
            with requests.get(file_url, stream=True) as file_response:
                file_response.raise_for_status()
                total_length = file_response.headers.get("content-length")

                if total_length is None:
                    # No content length header; just write the content
                    with open(file_name, "wb") as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:  # Filter out keep-alive chunks
                                f.write(chunk)
                    print("Download complete (total size unknown).")
                else:
                    total_length = int(total_length)
                    downloaded = 0
                    with open(file_name, "wb") as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                percent = downloaded / total_length * 100
                                # Print progress; the \r returns the cursor to the start of the line
                                sys.stdout.write(f"\rDownloaded {downloaded} of {total_length} bytes ({percent:.2f}%)")
                                sys.stdout.flush()
                    # Make sure to move to the next line after progress output
                    print("\nDownload complete.")
            print(f"Saved to {file_name}")

            # Save the link to the list
            downloaded_links.append({"file_name": file_name, "file_url": file_url, "link_title": link_title})
            print("------------------LINK TITLE-----------------------------")
            print(link_title)
            print("---------------------------------------------------------")
        except requests.RequestException as e:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(f"Failed to download {file_url}: {e}")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        # Add a random delay between downloads
        time_delay = random.uniform(2, 5)  # Random delay between 2 to 5 seconds
        print(f"Waiting for {time_delay:.2f} seconds before the next download...")
        time.sleep(time_delay)

# Save the links to a JSON file
json_path = os.path.join(output_dir, "dokumenta-zeleznica-srbije.json")
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(downloaded_links, json_file, indent=4, ensure_ascii=False)

print("Download completed for all files.")
