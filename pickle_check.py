import pickle

def load_from_pkl(filename="top_posts.pkl"):
    """
    Load the list of posts from a .pkl file.
    
    :param filename: Name of the .pkl file to load.
    :return: List of dictionaries containing post data.
    """
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

# Example usage
if __name__ == "__main__":
    posts = load_from_pkl('./data/top_posts_nz.pkl')
    
    print(f"Total number of posts: {len(posts)}\n")  # Print the number of rows
    
    for post in posts:
        print(post)
