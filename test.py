from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

query = 'Health Canada'
num_results = 30

# extract the publication date
def extract_date(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        meta_date = soup.find("meta", {"name": "date"})
        if meta_date:
            return meta_date.get("content")

        # Look for date in YYYY-MM-DD format
        content_date = re.search(r'\b\d{4}-\d{2}-\d{2}\b', soup.get_text())
        if content_date:
            return content_date.group()

        return "Date not found"
    except Exception as e:
        print(f"Failed to retrieve or parse date for {url}: {e}")
        return "Date not found"

# scrape details from URL
def scrape_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return ' '.join(soup.get_text().split())
        else:
            return None
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

# get and save information
def main():
    search_results = search(query, num_results=num_results)

    with open(r'C:\tmp\webscrap_output2.txt', 'w', encoding='utf-8') as file:
        for link in search_results:
            print(f"Processing: {link}")
            date = extract_date(link)
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            title = ' '.join(soup.title.string.split()) if soup.title else "No title"
            snippet = ' '.join(soup.get_text().split()[:50]) if soup else "No snippet"

            output = (
                f"Date: {date}\n"
                f"Title: {title}\n"
                f"Link: {link}\n"
                f"Snippet: {snippet}\n"
            )
            print(output)
            file.write(output + '\n')

            page_content = scrape_page(link)
            if page_content:
                content_output = f"Content: {page_content[:1000]}...\n"
                print(content_output)
                file.write(content_output + '\n')
            else:
                error_output = "Content could not be retrieved.\n"
                print(error_output)
                file.write(error_output + '\n')

            separator = "=" * 80 + "\n"
            print(separator)
            file.write(separator + '\n')

if __name__ == "__main__":
    main()
