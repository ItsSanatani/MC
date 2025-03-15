from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Report command handler
async def report(client, message):
    # Check if user provided both group/channel link and message link
    try:
        parts = message.text.split(" ")
        
        if len(parts) < 3:
            await message.reply("Please provide both the Group/Channel link and the Message link. Example: /report @group_or_channel https://t.me/your_message_link")
            return
        
        group_channel_link = parts[1]  # Extract group/channel link
        message_link = parts[2]  # Extract message link

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
    
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Register report command
report_command = filters.command("report")(report)
