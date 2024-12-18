import requests
import os
import time
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
load_dotenv()

# Constants
DISCOURSE_URL = os.getenv("DISCOURSE_URL")
TOPIC_FILE = "topic_ids.txt"
MAX_WORKERS = 5  # Number of concurrent threads (adjust based on your server's rate limits)

# Function to get all accounts from the environment variables
def get_accounts_from_env():
    accounts = []
    for i in range(1, 21):  # Loop through USER1 to USER20
        api_key = os.getenv(f"USER{i}_API_KEY")
        username = os.getenv(f"USER{i}_USERNAME")
        if api_key and username:
            accounts.append({"api_key": api_key, "username": username})
    return accounts

# Function to get the first post ID from a topic
def get_first_post_id(topic_id, headers):
    topic_url = f"{DISCOURSE_URL}/t/{topic_id}.json"
    response = requests.get(topic_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        first_post_id = data.get("post_stream", {}).get("posts", [])[0].get("id")
        return first_post_id
    else:
        print(f"Failed to fetch topic {topic_id}. Status: {response.status_code}")
        return None

# Function to like a specific post
def like_post(post_id, headers):
    like_payload = {
        "id": post_id,
        "post_action_type_id": 2,  # 2 is the ID for "like"
    }
    like_url = f"{DISCOURSE_URL}/post_actions.json"
    response = requests.post(like_url, headers=headers, json=like_payload)

    if response.status_code == 200:
        print(f"Successfully liked post {post_id}.")
    else:
        print(f"Failed to like post {post_id}. Status: {response.status_code}")

# Worker function to process a single account
def process_account(account, topic_ids):
    headers = {"Api-Key": account["api_key"], "Api-Username": account["username"]}
    print(f"Processing topics with account: {account['username']}")

    for topic_id in topic_ids:
        first_post_id = get_first_post_id(topic_id, headers)
        if first_post_id:
            like_post(first_post_id, headers)

    print(f"Finished processing with account: {account['username']}")

# Function to fetch topic IDs (if file is empty)
def fetch_all_topic_ids(headers):
    topic_ids = []
    page = 0

    while True:
        response = requests.get(f"{DISCOURSE_URL}/latest.json", headers=headers, params={"page": page})
        if response.status_code != 200:
            print(f"Failed to fetch topics. Status: {response.status_code}")
            break

        data = response.json()
        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            break

        topic_ids.extend([topic["id"] for topic in topics])
        print(f"Fetched page {page + 1}, Topics: {len(topics)}")
        page += 1

    return topic_ids

# Main function to process all accounts concurrently
def process_topics_concurrently():
    # Read topic IDs from file
    if os.path.exists(TOPIC_FILE):
        with open(TOPIC_FILE, "r") as file:
            topic_ids = [line.strip() for line in file if line.strip()]
    else:
        print(f"File {TOPIC_FILE} not found. Fetching all topics.")
        topic_ids = []

    # If no topic IDs, fetch all using the admin account
    if not topic_ids:
        print("No topic IDs found in file. Fetching all topics...")
        admin_headers = {
            "Api-Key": os.getenv("API_KEY"),
            "Api-Username": os.getenv("API_USERNAME"),
        }
        topic_ids = fetch_all_topic_ids(admin_headers)

    print(f"Processing {len(topic_ids)} topics...")

    # Get accounts from environment
    accounts = get_accounts_from_env()
    if not accounts:
        print("No accounts found in the environment variables.")
        return

    print(f"Using {len(accounts)} accounts to like posts.")

    # Use ThreadPoolExecutor to process accounts concurrently
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_account, account, topic_ids) for account in accounts]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")

# Entry point
if __name__ == "__main__":
    process_topics_concurrently()
