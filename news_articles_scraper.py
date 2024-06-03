"""
News Article Scraper
====================
This script scrapes the latest news articles from a specified news website.
It uses the Beautiful Soup library to parse HTML content and extracts the titles
and links of the news articles. The extracted data is then stored in a Pandas DataFrame
and exported to a CSV file.

Usage:
- Specify the URL of the news website to scrape.

Example:
    To scrape news articles from 'https://example.com/news':
    python news_scraper.py
    python3 news_scraper.py

Note: Ensure you have installed the required libraries using pip:
    pip install requests beautifulsoup4 pandas
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_news_articles(url):
    """
    Fetch news articles from a specified news website.

    Parameters:
    url (str): The URL of the news website to scrape.

    Returns:
    pd.DataFrame: A DataFrame containing the titles and links of the news articles.
    """
    response = requests.get(url)  # Send a GET request to the specified URL
    soup = BeautifulSoup(response.content, 'html.parser')  # Parse the HTML content using Beautiful Soup

    # Find all article elements (customize the tag and class based on the website structure)
    articles = soup.find_all('article', class_='news-article')

    # Extract the titles and links of the news articles
    data = []
    for article in articles:
        title = article.find('h2').text.strip()  # Extract the title (customize the tag based on the website structure)
        link = article.find('a')['href']  # Extract the link
        data.append([title, link])

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['Title', 'Link'])
    return df

def export_to_csv(df, filename):
    """
    Export the DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to export.
    filename (str): The name of the CSV file to save the data.
    """
    df.to_csv(filename, index=False)  # Export the DataFrame to a CSV file without the index
    print(f'Data exported to {filename}')  # Print a message indicating successful export

# Example usage
news_url = 'https://bbc.com'  # Replace with the URL of the news website to scrape
news_df = fetch_news_articles(news_url)  # Fetch the news articles
print(news_df.head())  # Print the first few rows of the DataFrame to the console

# Export the DataFrame to a CSV file
export_to_csv(news_df, 'news_articles.csv')