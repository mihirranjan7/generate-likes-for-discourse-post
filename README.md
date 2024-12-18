# Discourse Topic Liking Bot

This script automates the process of liking the first post in multiple topics on a Discourse forum using multiple accounts concurrently. The script fetches topic IDs from a file or directly from the forum and likes the first post in each topic using different user accounts.

**Disclaimer:**  
This script is **not intended to be used on a real community**. It is designed solely for **testing purposes** or **personal use** on a test forum. Using this on a real community without permission can violate the community guidelines and may lead to rate-limiting or banning of user accounts.

## Requirements

- Python 3.6 or later
- Python libraries: `requests`, `dotenv`
  - Install the required libraries using:
    ```bash
    pip install requests python-dotenv
    ```

## Setup

1. **Clone or Download the Repository:**
   - Download or clone this repository to your local machine.

2. **Environment Variables:**
   - Create a `.env` file in the same directory as the script and add the following variables:
     - `DISCOURSE_URL`: The base URL of your Discourse forum (e.g., `https://your-forum.com`).
     - `USER1_API_KEY`, `USER2_API_KEY`, ..., `USER20_API_KEY`: API keys for your user accounts (1-20).
     - `USER1_USERNAME`, `USER2_USERNAME`, ..., `USER20_USERNAME`: The corresponding usernames for the API keys.
     - `API_KEY`: Admin API key to fetch topics if the topic file is empty.
     - `API_USERNAME`: Admin username to fetch topics if the topic file is empty.

   Example `.env` file:
   ```env
   DISCOURSE_URL=https://your-forum.com
   USER1_API_KEY=your_api_key_1
   USER1_USERNAME=your_username_1
   USER2_API_KEY=your_api_key_2
   USER2_USERNAME=your_username_2
   ...
   API_KEY=your_admin_api_key
   API_USERNAME=your_admin_username
   ```

3. **Topic IDs:**
   - The script will check if `topic_ids.txt` exists. If it does, it will use the IDs in that file. If not, it will fetch all topic IDs from the Discourse forum using the admin account and store them in the `topic_ids.txt` file.

4. **Adjusting Thread Pool:**
   - The `MAX_WORKERS` constant controls the number of concurrent threads (workers). Adjust this based on the server's rate limits and the number of available accounts.

## How to Use

1. **Ensure `.env` is configured properly** as mentioned above.
2. **Run the script:**
   ```bash
   python discourse_like_bot.py
   ```
   This will:
   - Fetch topic IDs (either from `topic_ids.txt` or by querying the forum).
   - Use multiple accounts to like the first post in each topic concurrently.

## How it Works

- **Fetching Topic IDs:**
  - The script first attempts to read topic IDs from `topic_ids.txt`. If the file does not exist or is empty, it will fetch the latest topics from the Discourse forum using the admin API.

- **Processing Accounts Concurrently:**
  - The script will process accounts concurrently using a thread pool. Each account will like the first post of each topic, helping distribute the load.

- **Liking Posts:**
  - The first post in each topic is identified, and a "like" action is performed for each account.

## Customization

- **Change the Post Action:**
  - If you want to change the action (e.g., "like" to "dislike"), modify the `post_action_type_id` in the `like_post` function. A value of `2` corresponds to "like". Check the Discourse API documentation for other action types.

- **Adjust Thread Pool Size:**
  - Adjust `MAX_WORKERS` to match your server's rate limits and the number of available accounts. More workers will allow for faster processing but may hit rate limits.

## Notes

- This script assumes that the Discourse API is set up to allow API key-based access for liking posts.
- **Use caution** when running the script, as it can send a large number of requests, potentially triggering rate limits or other restrictions on the server.
- This script should only be used in controlled environments such as test forums and not on real communities.

## License

This project is licensed under the MIT License.

---
