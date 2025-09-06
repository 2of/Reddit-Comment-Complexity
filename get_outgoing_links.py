import requests
import pickle

def get_list_of_top_posts(base_url, pages=5, time_range='all'):
    """
    Function to fetch top posts from Reddit, allowing sorting by time range.
    
    :param base_url: Base URL of the Reddit API endpoint.
    :param pages: Number of pages to fetch (default: 5).
    :param time_range: Time range for sorting posts ('all', 'day', 'week', 'month', 'year', 'hour').
    :return: A list of dictionaries containing 'id', 'URL', and 'has_downloaded'.
    """
    posts = []
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
        
        for post in data['data']['children']:
            post_id = post['data']['id']
            post_url = f"https://old.reddit.com{post['data']['permalink']}"
            posts.append({
                'id': post_id,
                'URL': post_url,
                'has_downloaded': 0  # Initialize to 0
            })
        
        after = data['data'].get('after')
        
        if not after:
            print("No more pages to fetch.")
            break
        
    return posts

def save_to_pkl(data, filename="top_posts_ck.pkl"):
    """
    Save the list of posts to a .pkl file.
    
    :param data: List of dictionaries containing post data.
    :param filename: Name of the .pkl file to save.
    """
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    
    print(f"Data successfully saved to {filename}")

if __name__ == "__main__":
    base_url = 'https://old.reddit.com/r/NewZealand/top.json'
    time_range = 'all'
    top_posts = get_list_of_top_posts(base_url, pages=10, time_range=time_range)
    save_to_pkl(top_posts, 'top_posts_NZ.pkl')