# 🕵️ SocialSpyAgent

<div align="center">
  <h3>Your All-in-One Social Media Intelligence Tool</h3>
  <p>Created by <a href="https://www.youtube.com/@kenkaidoesai">Ken Kai</a></p>
  <p>Easily gather data from YouTube, Instagram, TikTok, and hundreds of other platforms</p>
</div>

## 📋 What is SocialSpyAgent?

SocialSpyAgent is a powerful, easy-to-use command-line tool that helps you gather intelligence from various social media platforms. Whether you're researching competitors, tracking social media trends, or just curious about someone's online presence, SocialSpyAgent makes it simple.

## ✨ Features

- 🔍 **Search across platforms** - Find content using keywords
- 📊 **Competitor analysis** - Track what your competitors are posting
- 🕵️ **Username search** - Find accounts across hundreds of websites
- 📱 **Multi-platform support** - YouTube, Instagram, TikTok, and more
- 📂 **Data export** - Save results as JSON and CSV files
- 🎨 **Beautiful interface** - Colorful, interactive command-line experience

## 🚀 Quick Start Guide

### 💻 For Windows Users

#### Step 1: Download the Project
- Download this project by clicking the green "Code" button at the top of the GitHub page and selecting "Download ZIP"
- Extract the ZIP file to a location on your computer (e.g., your Documents folder)

#### Step 2: Run the Setup Script
1. Open File Explorer and navigate to where you extracted the project
2. Double-click on the `setup.bat` file
   - If you see a security warning, click "More info" and then "Run anyway"
3. A command prompt window will open and guide you through the setup process
4. The setup will:
   - Check if Python is installed (and install it if needed)
   - Create a virtual environment
   - Install all required dependencies
   - Create a template `.env` file for your API keys

#### Step 3: Get Your API Keys
You'll need two API keys to use all features:

1. **Google API Key** (for YouTube):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "Create Project" at the top of the page
   - Give your project a name (e.g., "SocialSpyAgent") and click "Create"
   - In the search bar, type "YouTube Data API v3" and click on it in the results
   - Click "Enable" to activate the API
   - Go to "Credentials" in the left sidebar
   - Click "Create Credentials" and select "API key"
   - Copy your new API key

2. **RapidAPI Key** (for Instagram and TikTok):
   - Go to [RapidAPI](https://rapidapi.com/) and create an account
   - Once logged in, go to [instagram360 API](https://rapidapi.com/DavidGelling/api/instagram360)
   - Click "Subscribe to Test" and select a plan (there's a free option)
   - Go to [TikTok API](https://rapidapi.com/omarmhaimdat/api/tiktok-api6)
   - Click "Subscribe to Test" and select a plan (there's a free option)
   - Find your API key by clicking your profile icon → "My Apps" → "Security" → copy the "X-RapidAPI-Key"

#### Step 4: Add Your API Keys
1. Open the project folder
2. Find and open the `.env` file with Notepad or any text editor
3. Replace the placeholder text with your actual API keys:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   RAPIDAPI_KEY=your_actual_rapidapi_key_here
   ```
4. Save and close the file

#### Step 5: Run the Application
1. Double-click on the `run_app.bat` file
2. The application will start in a command prompt window with a colorful menu

### 🍎 For Mac/Linux Users

#### Step 1: Download the Project
- Download this project by clicking the green "Code" button at the top of the GitHub page and selecting "Download ZIP"
- Extract the ZIP file to a location on your computer (e.g., your home directory)

#### Step 2: Run the Setup Script
1. Open Terminal
2. Navigate to the project directory:
   ```
   cd path/to/extracted/folder
   ```
3. Make the setup script executable:
   ```
   chmod +x setup.sh
   ```
4. Run the setup script:
   ```
   ./setup.sh
   ```
5. The script will:
   - Check if Python is installed (and guide you through installation if needed)
   - Create a virtual environment
   - Install all required dependencies
   - Create a template `.env` file for your API keys

#### Step 3: Get Your API Keys
Follow the same instructions as in the Windows section above to get your:
- Google API Key (for YouTube)
- RapidAPI Key (for Instagram and TikTok)

#### Step 4: Add Your API Keys
1. Open the `.env` file with a text editor:
   ```
   nano .env
   ```
   or
   ```
   open -e .env
   ```
2. Replace the placeholder text with your actual API keys:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   RAPIDAPI_KEY=your_actual_rapidapi_key_here
   ```
3. Save and close the file

#### Step 5: Create a Virtual Environment in Python
1. source venv/bin/activate

#### Step 6: Run the Application
1. Make the run script executable:
   ```
   chmod +x run_app.sh
   ```
2. Run the application:
   ```
   ./run_app.sh
   ```

## 📝 How to Use SocialSpyAgent

### Main Menu Options

When you start SocialSpyAgent, you'll see a colorful menu with these options:

#### 1. Search by Query
This option lets you search for content across platforms using keywords:
1. Type your search query (e.g., "artificial intelligence", "travel tips")
2. Select a time frame:
   - Last 24 hours
   - Last week
   - Last 30 days
   - All time
3. The tool will search YouTube, Instagram, and TikTok for matching content
4. Results will be displayed in the terminal and saved to output files

#### 2. Competitor Analysis
This option analyzes all accounts listed in your `config.json` file:
1. Select a time frame for the analysis
2. The tool will gather data from all accounts across all platforms
3. Results will be displayed in the terminal and saved to output files

#### 3. Spy on Username
This option searches for a username across hundreds of websites:
1. Enter the username you want to search for
2. The tool will check if that username exists on various platforms
3. Results will be displayed in a table showing where the username was found
4. A detailed report will be saved in the "Output Spy" folder

### Customizing Accounts to Monitor

You can customize which accounts to monitor in two ways:

#### Option 1: Using the Terminal UI (Recommended for Beginners)

SocialSpyAgent includes a built-in menu option to manage your accounts:

1. Start the application using `run_app.bat` (Windows) or `run_app.sh` (Mac/Linux)
2. From the main menu, select the option to manage accounts
3. Follow the on-screen prompts to:
   - Add new accounts to monitor
   - Remove existing accounts
   - View current accounts

The changes will be saved automatically, and you can use them right away.

#### Option 2: Editing the Config File Directly

If you prefer, you can manually edit the `config.json` file:

1. Open `config.json` with any text editor
2. Add or remove usernames from each platform section:
   ```json
   {
       "youtube_accounts": [
           "GoogleDevelopers",
           "TensorFlow",
           "MicrosoftDeveloper"
       ],
       "instagram_accounts": [
           "instagram",
           "natgeo",
           "nasa"
       ],
       "tiktok_accounts": [
           "tiktok",
           "charlidamelio",
           "khaby.lame"
       ]
   }
   ```
3. Save the file and restart the application

## 📊 Understanding the Output

### Where to Find Your Data

SocialSpyAgent saves data in three main folders:
- `Output JSON` - Contains detailed data in JSON format
- `Output CSV` - Contains the same data in CSV format (can be opened in Excel)
- `Output Spy` - Contains results from username searches

### YouTube Data Includes:
- Video title
- View count
- Like count
- Comment count
- Publication date
- Direct link to the video

### Instagram Data Includes:
- Username
- Caption
- View count
- Like count
- Comment count
- Publication date
- Direct link to the post
- Engagement rate

### TikTok Data Includes:
- Username
- Caption
- View count
- Like count
- Comment count
- Share count
- Publication date
- Direct link to the video
- Engagement rate

## ❓ Troubleshooting

### "Python is not recognized as an internal or external command"
- The setup script should install Python automatically
- If you still see this error, download and install Python from [python.org](https://www.python.org/downloads/)
- During installation, make sure to check "Add Python to PATH"
- Restart your computer after installation

### API Key Issues
- Make sure you've copied the entire API key without any extra spaces
- Check that you've subscribed to the correct APIs on RapidAPI
- Verify that you've enabled the YouTube Data API v3 in Google Cloud Console

### Sherlock Not Working
- Make sure you're using the provided run scripts (`run_app.bat` or `run_app.sh`)
- If running manually, ensure you've activated the virtual environment
- Try reinstalling Sherlock: `pip install sherlock-project --upgrade`

### Other Issues
- Try deleting the `venv` folder and running the setup script again
- Make sure your internet connection is stable
- Check that you have sufficient disk space

## 🔄 Updating SocialSpyAgent

To update to the latest version:
1. Download the latest version from GitHub
2. Extract it to a new folder
3. Copy your `.env` file from the old installation to the new one
4. Copy your `config.json` file if you've customized it
5. Run the setup script in the new folder

## 📚 Advanced Usage

For advanced users, SocialSpyAgent supports command-line options:

```
python main.py --platform youtube --query "machine learning" --timeframe 2
python main.py --platform instagram --query "travel"
python main.py --platform all --query "artificial intelligence"
```

Available options:
- `--platform`: youtube, instagram, tiktok, or all
- `--output`: Custom output directory
- `--interactive`: Force interactive mode
- `--query`: Search query
- `--timeframe`: 1=24h, 2=7d, 3=30d, 4=all

**Notes**:
- Videos with 2,000 or fewer views are automatically filtered out from the results.
- Comments are not fetched to reduce API usage and improve performance.

## 📱 Supported Social Media Platforms

### YouTube
SocialSpyAgent uses the official YouTube Data API to fetch:
- Videos from specific channels
- Search results based on keywords
- Detailed video statistics

### Instagram
SocialSpyAgent uses the instagram360 API to fetch:
- User reels and posts
- Search results for reels based on keywords
- Engagement metrics and video statistics

### TikTok
SocialSpyAgent uses the TikTok API to fetch:
- Videos from specific users
- Search results based on keywords
- Engagement metrics and video statistics

### Hundreds More (via Sherlock)
The "Spy on username" feature uses Sherlock to check if a username exists on:
- Major social networks (Twitter, Facebook, etc.)
- Professional sites (LinkedIn, GitHub, etc.)
- Forums and communities (Reddit, Discord, etc.)
- Dating apps, gaming platforms, and much more

## 🔒 Privacy and Terms of Use

- SocialSpyAgent only accesses publicly available data
- Please use this tool responsibly and ethically
- Respect the terms of service of each platform
- Do not use for harassment or illegal activities

## 🤝 Need Help?

If you encounter any issues or have questions:
1. Check the Troubleshooting section above
2. Look for similar issues in the GitHub Issues tab
3. Create a new issue with details about your problem

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <p>Made with ❤️ by <a href="https://www.youtube.com/@kenkaidoesai">Ken Kai</a> for social media researchers and marketers</p>
  <p>Check out my YouTube channel: <a href="https://www.youtube.com/@kenkaidoesai">https://www.youtube.com/@kenkaidoesai</a></p>
  <p>Happy spying! 🕵️</p>
</div>
# socialspyagent
# socialspyagent
