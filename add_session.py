# Store session strings for users
session_strings = {}

# Function to handle the /addsession command
async def add_session_command(client, message):
    try:
        # Extract the session string from the message
        parts = message.text.split(" ")
        
        if len(parts) < 2:
            await message.reply("Please provide the session string.")
            return
        
        session_string = parts[1]
        
        # Store the session string
        user_id = message.chat.id
        if user_id not in session_strings:
            session_strings[user_id] = []
        
        session_strings[user_id].append(session_string)
        await message.reply(f"Session string added successfully! You now have {len(session_strings[user_id])} session(s).")
    
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
