from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Function to fetch image posts from Reddit
def get_reddit_images(query):
    subreddit = "all"
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=off&sort=new"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        posts = []

        for post in data["data"]["children"]:
            post_data = post["data"]
            post_url = post_data["url"]

            # Check if the post URL is an image
            if post_url.endswith(('.jpg', '.png', '.gif')):
                posts.append({
                    'title': post_data['title'],
                    'image_url': post_url,
                    'subreddit': post_data['subreddit']
                })

        return posts
    else:
        return []

# Route to render the search page and display results
@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    posts = []
    
    if request.method == "POST":
        query = request.form.get("query")  # Get the search query from the form
        posts = get_reddit_images(query)  # Fetch Reddit image posts

    return render_template("index.html", posts=posts, query=query)

if __name__ == "__main__":
    app.run(debug=True)
