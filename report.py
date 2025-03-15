from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import PeerIdInvalid

# Dictionary to store active report requests
report_requests = {}

# Function to handle the /report command
async def report(client, message):
    try:
        # Split the message to extract group/channel link
        parts = message.text.split(" ")
        if len(parts) < 2:
            await message.reply("Please provide a group/channel link.")
            return
        
        group_channel_link = parts[1]  # Get the group/channel link
        report_requests[message.chat.id] = {
            'group_channel_link': group_channel_link,
            'user_id': message.chat.id
        }

        # Ask for the message link to report
        await message.reply("Please provide the message link to report.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Function to handle reason selection for the report
async def handle_reason_selection_command(client, callback_query: CallbackQuery):
    try:
        # Handle the reason selection for the report
        reason = callback_query.data
        report_requests[callback_query.message.chat.id]['reason'] = reason
        await callback_query.answer(f"Selected reason: {reason}")

        # Ask for the report count (how many reports)
        await callback_query.message.reply("How many times would you like to report this message?")
    except Exception as e:
        await callback_query.message.reply(f"An error occurred: {str(e)}")

# Function to handle the report count input
async def handle_report_count_command(client, message):
    try:
        chat_id = message.chat.id
        report_data = report_requests.get(chat_id, {})

        if not report_data:
            await message.reply("No active report request found. Please start a new report.")
            return
        
        # Get the report count (how many reports to send)
        try:
            report_count = int(message.text)
        except ValueError:
            await message.reply("Please enter a valid number.")
            return
        
        # Send the reports using all session strings
        await send_reports_from_sessions(report_data, report_count)
        await message.reply(f"Reports sent successfully using {len(session_strings.get(chat_id, []))} sessions!")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Function to send reports from multiple sessions
async def send_reports_from_sessions(report_data, report_count):
    reason = report_data['reason']
    group_channel_link = report_data['group_channel_link']
    message_link = report_data['message_link']

    # Iterate through all the session strings for the user
    user_id = report_data['user_id']
    sessions = session_strings.get(user_id, [])
    
    for session_string in sessions:
        try:
            # Start a new client for each session string
            async with Client(session_string, api_id="YOUR_API_ID", api_hash="YOUR_API_HASH") as client:
                for _ in range(report_count):
                    # Send the report (you may need to adjust the reporting method based on your use case)
                    try:
                        await client.send_message(group_channel_link, text=f"Reporting message {message_link} for reason {reason}")
                    except PeerIdInvalid:
                        pass  # Handle invalid peer errors gracefully
        except Exception as e:
            print(f"Error sending report with session {session_string}: {e}")
