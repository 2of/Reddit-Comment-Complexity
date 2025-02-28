import requests

def extract_comments(data):
    comments_list = []  # List to store all comments

    for comment in data:
        # Check if the comment is of type 'more'
        if comment['kind'] == 'more':
            continue  # Skip 'more' comments, as they are placeholders for additional comments

        comment_body = comment['data']['body']
        comment_author = comment['data']['author']
        
        # Append the comment's body and author to the list
        comments_list.append(comment_body)

        # If there are nested replies, recursively extract them
        if 'replies' in comment['data']:
            replies = comment['data']['replies']
            if replies:
                comments_list.extend(extract_comments(replies['data']['children']))

    return comments_list

def do_request(url):
    # Send a GET request to the .json endpoint
    post_url = url + '.json'
    response = requests.get(post_url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code == 200:
        return response.json()  # Return the parsed JSON data

def do_comments_page(data):
    # Extract comments from the page
    return extract_comments(data[1]['data']['children'])

if __name__ == "__main__": 
    print("Fetching comments...")

    # URL for the Reddit post
    data = do_request("https://old.reddit.com/r/unpopularopinion/comments/1izrv6p/bobs_burgers_is_literally_fucking_unwatchable/")
    
    # Extract comments from the post
    comments = do_comments_page(data)
    
    # Display the comments (or handle as needed)
    print(comments)
