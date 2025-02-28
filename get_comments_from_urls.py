import requests
import csv

def extract_comments(data):
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
    comment = comment.replace('\n', ' ').replace('\r', ' ')
    comment = comment.replace('"', '""')
    return comment

def do_request(url):
    post_url = url + '.json'
    response = requests.get(post_url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        return response.json()

def do_comments_page(data):
    return extract_comments(data[1]['data']['children'])

def write_comments_to_csv(comments, output_filename="comments_output.csv"):
    with open(output_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for comment in comments:
            writer.writerow([comment])

def read_urls_from_csv(input_filename="urls_input.csv", limit=float('inf')):
    urls = []
    with open(input_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i < limit:
                urls.append(row[0])
            else:
                break
    return urls

if __name__ == "__main__": 
    print("Fetching comments from Reddit posts...")
    urls = read_urls_from_csv("top_posts_ck.csv")
    
    for url in urls:
        print(f"Processing URL: {url}")
        data = do_request(url)
        
        if data:
            comments = do_comments_page(data)
            write_comments_to_csv(comments, "CK_comments.csv")

    print("Finished fetching and writing comments.")
