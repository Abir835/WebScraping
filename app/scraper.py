import requests
from bs4 import BeautifulSoup


def scrape_quotes():
    url = 'https://www.goodreads.com/quotes'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_list = []

    quote_containers = soup.find_all('div', class_='quoteDetails')
    for container in quote_containers:
        quote_text = container.find('div', class_='quoteText').text.strip().split('\n')[0].strip()
        author_tag = container.find('span', class_='authorOrTitle')
        author = author_tag.text.strip() if author_tag else 'Unknown'
        quotes_list.append({'text': quote_text, 'author': author})

    return quotes_list


if __name__ == "__main__":
    quotes = scrape_quotes()
    for quote in quotes:
        print(f"{quote['text']} - {quote['author']}")
