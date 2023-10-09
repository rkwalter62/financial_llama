from benzinga import news_data
import config
import os
import time
from datetime import datetime

# Directory to save articles
ARTICLES_DIR = 'articles'

# Ensure the articles directory exists
if not os.path.exists(ARTICLES_DIR):
    os.makedirs(ARTICLES_DIR)

fin = news_data.News(config.BENZINGA_API_KEY)
stories = fin.news(company_tickers="CDE", date_from="2023-03-05", date_to="2023-10-05")
print(stories)
symbols = ['MSFT', 'NVDA', 'GOOG', 'META', 'AAPL', 'TSM']
#symbols = ['CDE', 'AGI', 'HCL', 'AG', 'FSM', 'HCL', 'IAM', 'KGC', 'EGO']
for symbol in symbols:
    try:
        # Fetch news with additional parameters if needed
        stories = fin.news(company_tickers=symbol
                           #date_from="2021-01-01", date_to="2023-10-05"
                           ,pagesize=800, display_output='full')
        if stories and isinstance(stories, list):
            for story in stories:
                # Correct the way date is extracted and formatted
                created = story.get('created')
                if created:
                    try:
                        # Adjust the date format if necessary
                        created_date = datetime.strptime(created, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
                    except ValueError:
                        print(f"Could not parse date: {created}")
                        continue
                else:
                    print(f"Missing created date for {symbol}: {story.get('title')}")
                    continue

                title = story.get('title')
                body = story.get('body')

                if created and title and body:
                    # Create a filename based on the creation date and title
                    safe_title = ''.join(c if c.isalnum() else '_' for c in title)[
                                 :50]  # Making the title filesystem-safe
                    filename = f"{ARTICLES_DIR}/{created_date}-{symbol}-{safe_title}.html"

                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(body)

                    print(f"Saved article: {filename}  and title: {title}")
                else:
                    print(f"Missing data for {symbol}: {title}")
        else:
            print(f"No stories found for {symbol}.")

    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")

    time.sleep(2)  # Adjust delay as needed to respect API rate limits

