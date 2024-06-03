"""
Reddit Data Fetcher
===================
This script fetches posts from Reddit using the PRAW (Python Reddit API Wrapper) library.
It authenticates using Reddit API credentials and fetches posts from a specific subreddit
based on a search query, storing them in a Pandas DataFrame. The DataFrame is then exported
to a CSV file.

Usage:
- Replace 'client_id', 'client_secret', and 'user_agent' with your actual Reddit API credentials.
- Run the script with the subreddit and search query as command-line arguments.

Example:
    To fetch posts containing the keyword 'bitcoin' from the 'bitcoin' subreddit:
    python reddit_data.py bitcoin bitcoin
    python3 reddit_data.py bitcoin bitcoin

Note: Ensure you have installed the PRAW and pandas libraries using pip:
    pip install praw pandas
"""

import praw
import pandas as pd
import argparse

# Initialize the Reddit instance with your own credentials
reddit = praw.Reddit(
    client_id='OWRtInTv4zZdqbLztfmEXQ',           # Your Reddit application client ID
    client_secret='QMEyOO5arcZ5WBAaVaYwyFmUgKfrSA', # Your Reddit application client secret
    user_agent='Sweaty_Confusion_744'              # A unique identifier for your application
)

def fetch_reddit_posts(subreddit, query, limit=100):
    """
    Fetch posts from a specified subreddit based on a search query.

    Parameters:
    subreddit (str): The name of the subreddit to search.
    query (str): The search query to filter posts.
    limit (int): The maximum number of posts to fetch. Default is 100.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched posts with columns 'timestamp' and 'title'.
    """
    subreddit = reddit.subreddit(subreddit)          # Get the subreddit object
    posts = subreddit.search(query, limit=limit)     # Search for posts matching the query within the subreddit
    post_list = [[post.created_utc, post.title] for post in posts]  # Extract the creation time and title of each post
    df = pd.DataFrame(post_list, columns=['timestamp', 'title'])    # Create a DataFrame from the extracted data
    df['date'] = pd.to_datetime(df['timestamp'], unit='s').dt.date  # Convert the timestamp to a readable date format
    df.set_index('date', inplace=True)                # Set the date column as the index of the DataFrame
    return df                                         # Return the DataFrame

def export_to_csv(df, filename):
    """
    Export the DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to export.
    filename (str): The name of the CSV file to save the data.
    """
    df.to_csv(filename)                               # Export the DataFrame to a CSV file
    print(f'Data exported to {filename}')             # Print a message indicating successful export

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Fetch and export Reddit posts based on a search query.")
parser.add_argument('subreddit', type=str, help='The subreddit to search in')
parser.add_argument('query', type=str, help='The search query to filter posts')
args = parser.parse_args()

# Fetch posts based on command-line arguments
reddit_df = fetch_reddit_posts(args.subreddit, args.query, limit=100)  # Fetch posts based on subreddit and query
print(reddit_df.head())  # Print the first few rows of the DataFrame to the console

# Export the DataFrame to a CSV file
csv_filename = f'reddit_{args.subreddit}_{args.query}_posts.csv'  # Create a filename based on the subreddit and query
export_to_csv(reddit_df, csv_filename)
