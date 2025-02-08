import json
import os
from urllib.parse import urljoin

import pytest
import requests
from bs4 import BeautifulSoup

# Constants
URL = "https://www.srbija.gov.rs/dokument/843976/dokumenta-ministarstva-gradjevinarstva-saobracaja-i-infrastrukture-koja-se-ticu-moguceg-izvrsenja-krivicnog-dela-povodom-pada-nadstresnice-na-zeleznickoj-stanici-u-novom-sadu-1-novembra-2024-godine-13.php"
OUTPUT_DIR = "/home/datatab/Documents/NADSTRESNICA/nadstresnica/cookbook/str-1-downloaded_documents"
JSON_FILE = os.path.join(OUTPUT_DIR, "/home/datatab/Documents/NADSTRESNICA/nadstresnica/cookbook/str-1-downloaded_documents/str-1-downloaded_documents.json")


@pytest.fixture
def get_links_from_website():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.fail(f"Failed to fetch website data: {e}")

    soup = BeautifulSoup(response.content, "html.parser")

    file_extensions = [".pdf", ".zip", ".rar", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"]
    links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        link_title = link.get_text(strip=True)

        if any(href.lower().endswith(ext) for ext in file_extensions):
            file_url = urljoin(URL, href)
            file_name = os.path.basename(href)

            link_info = {"file_name": file_name, "file_url": file_url, "link_title": link_title}

            links.append(link_info)

    if not links:
        pytest.fail("No downloadable links found on the website.")

    return links


@pytest.fixture
def get_downloaded_links():
    if not os.path.exists(JSON_FILE):
        pytest.fail(f"JSON file {JSON_FILE} does not exist.")

    try:
        with open(JSON_FILE) as json_file:
            downloaded_links = json.load(json_file)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to decode JSON file: {JSON_FILE}")

    # Remove full path to only keep file names
    for link in downloaded_links:
        link["file_name"] = os.path.basename(link["file_name"])

    if not downloaded_links:
        pytest.fail("No downloaded links found in the JSON file.")

    return downloaded_links


def test_links_match(get_links_from_website, get_downloaded_links):
    website_links = get_links_from_website
    downloaded_links = get_downloaded_links

    # Check if the number of links matches
    assert website_links is not None, "Failed to retrieve links from website."
    assert downloaded_links is not None, "Failed to retrieve downloaded links."

    assert len(website_links) == len(downloaded_links), "Mismatch in number of links."

    # Check if all files are downloaded correctly
    for website_link in website_links:
        matching_files = []

        for downloaded_link in downloaded_links:
            if downloaded_link["file_name"] == website_link["file_name"]:
                matching_files.append(downloaded_link)

        assert len(matching_files) > 0, f"File {website_link['file_name']} is missing."

        # Check if file exists in the directory
        file_path = os.path.join(OUTPUT_DIR, website_link["file_name"])
        assert os.path.exists(file_path), f"Downloaded file {file_path} does not exist."

        # Check if URLs match
        assert matching_files[0]["file_url"] == website_link["file_url"], f"URL mismatch for {website_link['file_name']}"

        # Check if titles match
        assert matching_files[0]["link_title"] == website_link["link_title"], f"Title mismatch for {website_link['file_name']}"
