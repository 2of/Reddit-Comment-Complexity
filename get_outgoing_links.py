import requests
import csv

def get_list_of_top_posts(base_url, pages=5, time_range='all'):
    """
    Function to fetch top posts URLs from Reddit, allowing sorting by time range.
    
    :param base_url: 
    :param pages: 
    :param time_range: ('all', 'day', 'week', 'month', 'year', 'hour').
    :return: A list of URLs 
    """
    post_urls = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    after = None
    
    for _ in range(pages):
        params = {'limit': 50, 't': time_range}
        
        if after:
            params['after'] = after
        
        response = requests.get(base_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            break
        
        data = response.json()
        
        post_urls.extend([f"https://old.reddit.com{post['data']['permalink']}" for post in data['data']['children']])
        
        after = data['data'].get('after')
        
        if not after:
            print("No more pages to fetch.")
            break
        
    return post_urls

def write_to_csv(post_urls, filename="top_posts.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Post URL"])
        for url in post_urls:
            writer.writerow([url])
    
    print(f"URLs successfully written to {filename}")

if __name__ == "__main__":
    base_url = 'https://old.reddit.com/r/NewZealand/top.json'
    time_range = 'all'
    top_posts = get_list_of_top_posts(base_url, pages=10, time_range=time_range)
    write_to_csv(top_posts, 'top_posts_nz.csv')
