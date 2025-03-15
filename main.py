from pyrogram import Client
from report import report_command, handle_reason_selection_command, handle_report_count_command
from add_session import add_session_command

# Initialize the bot with API credentials
api_id = '28795512'
api_hash = 'c17e4eb6d994c9892b8a8b6bfea4042a'
bot_token = '7893027318:AAHrAT8VukzZq3xUtAZuOuF2sKhhCok8gDg'

# Create a Pyrogram client
app = Client("mass_report_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Register all the command handlers
app.add_handler(report_command)  # Handle the /report command
app.add_handler(handle_reason_selection_command)  # Handle reason selection for report
app.add_handler(handle_report_count_command)  # Handle the report count input
app.add_handler(add_session_command)  # Handle adding new session strings

# Start the bot
if __name__ == "__main__":
    app.run()  # This will start the bot and keep it running
