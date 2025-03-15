from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Initialize your app with the bot token
api_id = '28795512'
api_hash = 'c17e4eb6d994c9892b8a8b6bfea4042a'
bot_token = '7893027318:AAHrAT8VukzZq3xUtAZuOuF2sKhhCok8gDg'

# List of session strings (You can add new ones dynamically)
session_strings = []

app = Client("mass_report_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Start command - Asks for group/channel link and message link
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "Welcome! Please provide the Group/Channel link and then the Message link you want to report.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Session", callback_data="add_session")]
        ])
    )

# Command to add session string
@app.on_message(filters.command("addsession"))
async def add_session(client, message):
    await message.reply("Please provide the session string you want to add.")
    # Wait for the session string
    session_strings.append(message.text.split(" ", 1)[1])
    await message.reply("Session string added successfully!")

# Report reason selection
@app.on_message(filters.command("report"))
async def report(client, message):
    group_channel_link = message.text.split(" ")[1]  # Extract group/channel link
    message_link = message.text.split(" ")[2]  # Extract message link

    # Ask for the reason
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Spam", callback_data="spam")],
        [InlineKeyboardButton("Child Abuse", callback_data="child_abuse")],
        [InlineKeyboardButton("Violence", callback_data="violence")],
        [InlineKeyboardButton("Illegal Content", callback_data="illegal_content")],
        [InlineKeyboardButton("Scam or Spam", callback_data="scam_spam")],
        [InlineKeyboardButton("Other", callback_data="other")]
    ])
    
    await message.reply("Select the reason for reporting:", reply_markup=reply_markup)

# Handle button presses for reason selection
@app.on_callback_query()
async def handle_reason(client, callback_query):
    reason = callback_query.data
    # Asking for the report count
    await callback_query.message.reply(f"You selected {reason}. How many reports would you like to send?", 
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton("1", callback_data="1")],
                                          [InlineKeyboardButton("5", callback_data="5")],
                                          [InlineKeyboardButton("10", callback_data="10")]
                                      ]))
    await callback_query.answer()

# Handle report count selection and perform the reports
@app.on_callback_query()
async def handle_report_count(client, callback_query):
    count = int(callback_query.data)
    # Logic to send reports using session strings
    group_channel_link = 'your_group_or_channel_link'  # Get from previous context
    message_link = 'your_message_link'  # Get from previous context
    reason = 'selected_reason'  # Get from previous context

    # Iterate through session strings and send reports
    for session in session_strings:
        async with Client(session_string=session) as user_client:
            for _ in range(count):
                # Send the report
                await user_client.report(message_link, reason)
    await callback_query.message.reply(f"Reported {count} times using {len(session_strings)} sessions.")
    await callback_query.answer()

# Run the bot
app.run()
