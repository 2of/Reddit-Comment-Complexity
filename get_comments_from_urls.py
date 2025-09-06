import requests
import json
import pickle
import sys
import os
import uuid

def extract_comments(data):
    """
    Recursively extract comments from Reddit API response data.
    """
    comments_list = []

    for comment in data:
        if comment['kind'] == 'more':
            continue

        comment_body = comment['data']['body']
        comment_body = clean_comment(comment_body)
        comments_list.append(comment_body)

        if 'replies' in comment['data']:
            replies = comment['data']['replies']
            if replies:
                comments_list.extend(extract_comments(replies['data']['children']))

    return comments_list

def clean_comment(comment):
    """
    Clean the comment text by removing newlines and escaping double quotes.
    """
    comment = comment.replace('\n', ' ').replace('\r', ' ')
    comment = comment.replace('"', '""')
    return comment

def do_request(url):
    """
    Perform a request to the Reddit API to fetch comments for a given post URL.
    If a 429 error or a timeout is encountered, save progress and stop the script.
    """
    post_url = url + '.json'
    try:
        response = requests.get(post_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        print(f"Response status code for {url}: {response.status_code}")
        
        if response.status_code == 429:
            print("Received 429 Too Many Requests. Saving progress and stopping the script.")
            return None  # Stop fetching more data, but don't crash

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.Timeout:
        print(f"Request to {url} timed out. Saving progress and stopping.")
        return None

    return None

def do_comments_page(data):
    """
    Extract comments from the Reddit API response data.
    """
    return extract_comments(data[1]['data']['children'])

def write_comments_to_json(data, output_directory):
    """
    Write the collected comments data to a JSON file with a random filename in the specified directory.
    """
    # Generate a random filename
    random_filename = str(uuid.uuid4()) + ".json"
    output_path = os.path.join(output_directory, random_filename)
    
    with open(output_path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"Comments written to {output_path}")

def load_from_pkl(input_filename):
    """
    Load the list of posts from a .pkl file.
    """
    with open(input_filename, 'rb') as file:
        return pickle.load(file)

def save_to_pkl(data, output_filename):
    """
    Save the updated list of posts to a .pkl file.
    """
    with open(output_filename, 'wb') as file:
        pickle.dump(data, file)

if __name__ == "__main__":
    print("Fetching comments from Reddit posts...")
    
    # Define the path for the .pkl file
    pkl_file_path = "./data/top_posts_NZ.pkl"
    
    # Load the posts from the .pkl file
    posts = load_from_pkl(pkl_file_path)
    
    results = []  # This will hold our final data
    output_directory = "./data/NZ"  # Specify the directory for output files
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for post in posts:
        if post['has_downloaded'] == 1:
            print(f"Skipping already downloaded post: {post['URL']}")
            continue

        url = post['URL']
        print(f"Processing URL: {url}")
        data = do_request(url)
        
        if data:
            comments = do_comments_page(data)
            result = {
                "URL": url,
                "COMMENTS": comments
            }
            results.append(result)

            # Mark as downloaded
            post['has_downloaded'] = 1
        else:
            # Handle timeout or 429 error
            print("Saving collected comments before stopping due to timeout or 429.")
            write_comments_to_json(results, output_directory)
            save_to_pkl(posts, pkl_file_path)  # Save using the single pkl file path variable
            sys.exit(1)  # Exit script with a non-zero status

    # Final save
    save_to_pkl(posts, pkl_file_path)  # Save using the single pkl file path variable
    write_comments_to_json(results, output_directory)

    print("Finished fetching and writing comments.")
