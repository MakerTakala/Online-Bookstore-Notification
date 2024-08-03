# Online Bookstore Notification

This tool is designed to notify users of new book releases based on their personalized book lists. Utilizing Selenium and BeautifulSoup for web crawling, it is powered by GitHub Actions to run daily.

## Features

-   **Automated Daily Crawling:** Leverages Selenium and BeautifulSoup to scrape new book releases from various sources.
-   **Personalized Notifications:** Delivers email notifications based on your customized book queries.
-   **Easy Setup:** Simple configuration with environment secrets and variables.

## Supported Stores

-   **金石堂 (KingStone)**

Additional online bookstores may be added in future updates

## Usage

### 1. Fork the Repository

Begin by forking this repository to your GitHub account.

### 2. Configure Environment Secrets

Set the following environment secrets in your repository settings:

-   **EMAIL_SENDER:** The email address from which notifications will be sent.
-   **EMAIL_SENDER_PASSWORD:** The password for the sender's email account.

### 3. Configure Environment Variables

Define the following environment variables in your GitHub Actions workflow:

-   **QUERIES:** The book queries to track new releases (e.g., specific titles, authors, or genres).
-   **REGISTER:** The email address where you want to receive the notifications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
