# Reddit Data Collection (Pushshift/PRAW)

```python
# data/reddit_scraper.py
import praw
import pandas as pd
from datetime import datetime, timedelta
import time
import json

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        """Initialize Reddit API client."""
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
    
    def scrape_subreddit(self, subreddit_name, start_date, end_date, limit=None):
        """
        Scrape posts and comments from a subreddit within date range.
        
        Args:
            subreddit_name: Name of subreddit (e.g., 'wallstreetbets')
            start_date: Start date (datetime object)
            end_date: End date (datetime object)
            limit: Max number of posts to retrieve (None = all)
        
        Returns:
            DataFrame with columns: [id, created_utc, title, selftext, score, num_comments, author]
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        
        print(f"Scraping r/{subreddit_name} from {start_date} to {end_date}...")
        
        # Fetch posts (sorted by new)
        for submission in subreddit.new(limit=limit):
            created = datetime.utcfromtimestamp(submission.created_utc)
            
            if created < start_date:
                break  # Stop if we've gone past the date range
            
            if start_date <= created <= end_date:
                posts.append({
                    'id': submission.id,
                    'created_utc': submission.created_utc,
                    'created_date': created.strftime('%Y-%m-%d %H:%M:%S'),
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'author': str(submission.author),
                    'url': submission.url
                })
            
            # Rate limiting
            time.sleep(0.1)
        
        df = pd.DataFrame(posts)
        print(f"Collected {len(df)} posts from r/{subreddit_name}")
        return df
    
    def scrape_comments(self, submission_id, limit=None):
        """Scrape comments from a specific post."""
        submission = self.reddit.submission(id=submission_id)
        submission.comments.replace_more(limit=0)  # Remove "load more comments" objects
        
        comments = []
        for comment in submission.comments.list()[:limit]:
            comments.append({
                'id': comment.id,
                'parent_id': submission_id,
                'created_utc': comment.created_utc,
                'body': comment.body,
                'score': comment.score,
                'author': str(comment.author)
            })
        
        return pd.DataFrame(comments)

    def save_to_csv(self, df, filename):
        """Save DataFrame to CSV."""
        df.to_csv(f"data/raw/{filename}", index=False)
        print(f"Saved {len(df)} records to {filename}")

# Example usage
if __name__ == "__main__":
    # Load credentials from config file
    with open('config/reddit_creds.json', 'r') as f:
        creds = json.load(f)
    
    scraper = RedditScraper(
        client_id=creds['client_id'],
        client_secret=creds['client_secret'],
        user_agent=creds['user_agent']
    )
    
    # Define date range
    start = datetime(2020, 1, 1)
    end = datetime(2024, 12, 31)
    
    # Scrape multiple subreddits
    subreddits = ['wallstreetbets', 'investing', 'stocks', 'cryptocurrency', 'forex']
    
    for sub in subreddits:
        df = scraper.scrape_subreddit(sub, start, end, limit=10000)
        scraper.save_to_csv(df, f"reddit_{sub}_{start.year}_{end.year}.csv")
```
