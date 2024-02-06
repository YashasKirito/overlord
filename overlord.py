import trafilatura
import requests
import pdfkit
from bs4 import BeautifulSoup


def download_html(url):
    # Download the webpage
    response = requests.get(url)
    html_content = response.text

    return html_content


def get_next_page_url(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    # Find the "next" button element on the webpage
    next_button = soup.find("a", attrs={"rel": "next"})
    print(next_button)
    # next_vol = soup.find("a", string="Next Volume")

    if bool(next_button != None):
        # Construct the URL of the next page
        print("Found Next Chapter")
        try:
            next_page_url = next_button["href"]
            return next_page_url
        except KeyError:
            return None

    # if next_vol:
    #     # Construct the URL of the next page
    #     print("Found Next Volume")
    #     next_page_url = next_vol["href"]
    #     return next_page_url

    return None


# URL of the first webpage
base = "https://animedaily.net/"
base_url = "https://genesistls.com/childhood-friend-of-the-zenith-chapter-0/"
current_url = base_url

# Number of pages to download
predefined_count = 100
downloaded_count = 0

chap_num = 1

# Create an EPUB book

# Set metadata for the book

# Create a table of contents
extracted_contents = []

while downloaded_count <= predefined_count:
    # Download and print the HTML content

    html = download_html(current_url)

    # if downloaded_count == 1:
    #     current_url = get_next_page_url(html, base_url)
    #     downloaded_count += 1
    #     continue

    # Parse the HTML using Trafilatura
    xml_content = trafilatura.extract(
        html, include_formatting=True, output_format="xml"
    )
    r = xml_content.replace('<head rend="h1">', "<h1>")
    r2 = r.replace("</head>", "</h1>")
    r2 = r2.replace("</p>", "</p> <br />")
    extracted_contents.append(r2)

    print(f"progress: {int(downloaded_count * 100 / predefined_count)}%")

    downloaded_count += 1

    # Get the URL of the next page
    next_page_url = get_next_page_url(html, base_url)

    # while str(chap_num) in next_page_url:
    #     next_page_url = get_next_page_url(download_html(next_page_url), next_page_url)

    chap_num += 1

    if next_page_url:
        current_url = next_page_url
    else:
        break


# Concatenate the extracted content into a single string
combined_content = "\n\n".join(extracted_contents)
# Configure PDF options
options = {
    "page-size": "Letter",
    "encoding": "UTF-8",
}

# Convert the modified HTML content to PDF with original formatting
pdfkit.from_string(combined_content, "CFOZ_0_100.pdf", options=options)
print("PDF created successfully!")
