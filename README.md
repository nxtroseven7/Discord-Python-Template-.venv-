# My Discord Bot

A modular Python template for building and hosting a Discord bot locally on your PC using `discord.py` and a `.venv` virtual environment.

## How to Set Up and Run (Beginner Guide)

### 1. Get Your Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and open your application.
2. Click the **Bot** tab on the left sidebar.
3. Click the blue **Reset the token** button and copy your new token.
4. Scroll down to **Privileged Gateway Intents** and turn on **Server Members Intent** and **Message Content Intent**.

![Reset Discord Bot Token](assets/bot_token.png)

### 2. Download the Project

Clone or download this repository to a folder on your PC:

```bash
git clone https://github.com/nxtroseven7/Discord-Python-Template-.venv-.git
cd Discord-Python-Template-.venv-
```

### 3. Open the Terminal in Your Project Folder

1. Open the project folder in File Explorer.
2. Click the top address bar, type `cmd`, and press **Enter** to open Command Prompt directly inside the folder.

![Open Command Prompt in Project Folder](assets/cmd.png)

### 4. Create and Activate the Virtual Environment

In the terminal window, create a `.venv` folder to keep your bot's libraries isolated:

```bash
python -m venv .venv
```

Activate it:

* **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
* **Mac / Linux:**
  ```bash
  source .venv/bin/activate
  ```

*(You will see `(.venv)` appear at the start of your terminal line. if not then there is a problem that uhhh idk how to fix...)*

### 5. Install the Required Libraries
Install this in your command prompt (Python 3.X is required or else it won't work ) :
```bash
pip install discord.py 
pip install python-dotenv
```

### 6. Add Your Token to `.env`

1. Create a new file named `.env` in the same folder as `bot.py` (or open the existing `.env` file).
2. Paste your copied bot token inside and save the file:
   ```env
   DISCORD_TOKEN=your_copied_token_here
   ```

### 7. Start Your Bot

Run the bot with:

```bash
python bot.py
```

Your bot is now online! Keep the terminal window open while you want the bot to stay running on your PC.