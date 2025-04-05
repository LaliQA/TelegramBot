import datetime
import logging
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, CallbackContext
from telegram.error import TelegramError
from typing import Final

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
# Function to log user messages
async def log_user_message(user_id, username, text, taskName):
    with open('file directory Url', 'a') as f:
        f.write(f'User  ID: {user_id}, ({username}): {text}, Task Name:{taskName}\n')

# Constants
Token: Final = 'Replace with your bot token'  
Bot_Username: Final = 'Telegram bot user name'
CHANNEL_LINK='Telegram Channel link'
GROUP1_LINK='Telegram group link'
GROUP2_LINK='Telegram group link'
TARGET_CHANNEL_CHAT_ID = 'Channel ID'
TARGET_GROUP1_CHAT_ID = 'Group1 ID'
TARGET_GROUP2_CHAT_ID = 'Group2 ID'

# Initialize the bot
app = Application.builder().token(Token).build()

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user  # Get the user who sent the message
    first_name = user.first_name
    logger.info(f"Chat ID: {chat_id}")
    video_url = 'https://i.ibb.co/m6Z7YZ1/welcome.gif'
    caption = (f"Hey {first_name} Welcome to the airdrop! 🎉\n"
               "\n⬇️ Complete the tasks below to earn <b>$50 worth of $CSM</b> tokens.\n"
               "\nℹ️ <b>About Caesium ($CSM):</b>\n"
               "Caesium ($CSM) is a secure cryptocurrency for decentralised finance.\n"
               "\nℹ️ <b>About Alpha Returns:</b>\n"
               "\n<b>Alpha Returns</b> is a Play-to-Earn PvP game where players engage in exciting solo, duo, and squad modes. <b>You can convert the gold coins earned while playing into $CSM tokens.</b>\n"
               "\nThe airdrop ends on <b>🚨 APRIL 30, 2025 🚨</b>, and valid participants will be rewarded.\n\n"
               "🗒 <b>Airdrop Rules:</b>\n"
               "🔘 Follow our Telegram Channel\n"
               "🔘 Follow us on Twitter\n"
               "🔘 Download the Caesium Wallet and complete the KYC\n"
               "🔘 Submit your wallet address and sponsor code\n"
               "🔘 Refer friends to earn more\n"
               "\nClick the <b>🚨 Join Airdrop 🚨</b> button to submit your details and verify tasks."
    )

    keyboard = [[InlineKeyboardButton("Join AirDrop", callback_data='join_airdrop')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_animation(chat_id, animation=video_url, caption=caption, parse_mode='HTML', reply_markup=reply_markup)

# Define the tasks
TASKS = [

    "Task 1:\n🔘 Follow our Telegram channel <a href= 'Telegram channel link'><b>Caesium Lab</b></a>\n🔘 Stay tuned for Airdrop updates Once done.",
    "Task 2:\n🔘 Join our Telegram group <a href= 'Telegram group link'><b>Caesium Lab Media</b></a>\n🔘 Connect and talk to fellow crypto enthusiasts",
    "Task 3:\n🔘 Join our Telegram group <a href=  'Telegram group link'><b>Alpha Returns</b></a>\n🔘 Connect with fellow gamers ",
    "Task 4:\n🔘 Follow us on <b>Twitter</b>: <a href= 'https://x.com/Caesiumlab'><b>Caesium Twitter</b></a>\n🔘 Retweet the pinned post & tag 3 friends.\n🔘 Submit your Twitter username: <b>@username</b>",
    "Task 5:\n🔘 Download the <b>Caesium Wallet</b> from the App Store or Google Play:\n\n    • <a href='https://apps.apple.com/my/app/caesium/id6473259036'>Apple AppStore</a>\n    • <a href='https://play.google.com/store/apps/details?id=com.csm_app&hl=en_IN'>Google Play</a>\n\n🔘 complete the sign-up process.\n\n🔘 Submit your Caesium Wallet address.",
    "Task 6:\n🔘 Complete KYC verification procedure in the Caesium Wallet to confirm your participation.\n\n<b>If you have any questions, visit our </b><a href='https://caesiumlab.com/blogs/complete-your-kyc-with-caesium--step-by-step-tutorial'><b>Website.</b></a>",
]
TASK_IMAGES = {
    5: "https://i.ibb.co/NV0FSB8/kyc.png",  # Image for Task 6

}

# Dictionary to track user task progress
user_tasks = {} #In this dictionary we can able to track the TASKS
User_tasks={} #In this dictinory we can able to track the More_task_List

MORE_TASK = "Wanna earn an additional $12.5 to the wallet? Then, click the button below"
More_task_List= ["🔘 Refer friends and submit your sponsor code.\n🔘 Open your Caesium Wallet, go to the 'Refer' section, copy your unique referral link, and share it with 5 friends.\n For additional rewards, then, click the “Done” button.",
                 ("Download Alpha Returns from the App Store or Google Play:\n"
               "\n    • <a href='https://apps.apple.com/in/app/alpha-returns/id6479646239'>Apple Store</a>\n"
               "    • <a href='https://play.google.com/store/apps/details?id=com.caesiumlab.alphareturns&hl=en_IN'>Google Play</a>\n"
               ),
                 ]
# Tasks
async def join_airdrop(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    user_tasks[user_id] = 0  # Start at the first task
    await send_task(update, context)

async def send_task(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    task_index = user_tasks[user_id]

    if task_index < len(TASKS):
        task_text = TASKS[task_index]
        image_path = TASK_IMAGES.get(task_index)
        keyboard = [
            [InlineKeyboardButton("✅Done", callback_data='done'),
             InlineKeyboardButton("❌Cancel", callback_data='cancel')],
        ]
        # Add additional button based on the task index
        if task_index == 4:  # Task 5 (index 4)
            keyboard.insert(0, [InlineKeyboardButton("Sign-Up Tutorial", url='https://youtu.be/jpKtvTGpLuE?si=FQ2kf21Y0WpQ0xd0')])
        elif task_index == 5:  # Task 6 (index 5)
            keyboard.insert(0, [InlineKeyboardButton("KYC Tutorial", url='https://youtu.be/22H_JuSh8ho?si=hYDQvBWmwpoQboGZ')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        if image_path:
                await context.bot.send_photo(chat_id=user_id, photo=image_path, caption=task_text, parse_mode='HTML', reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=user_id, text=task_text, parse_mode='HTML', reply_markup=reply_markup)
    else:
        await complete_tasks(update, context)



async def done_task(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    # Check if the user is in the user_tasks dictionary
    if user_id not in user_tasks:
        user_tasks[user_id] = 0  # Initialize the user's task index if not present
    task_index = user_tasks[user_id]

    if task_index == 1:  # Task 2: join the caesiumlab media group
        await check_membership1(update, context)
        return
    if task_index == 2:  # Task 3: join the alpha returns group
        await check_membership2(update, context)
        return

    if task_index == 3:  # Task 4: Twitter username submission
        await context.bot.send_message(chat_id=user_id, text="Please submit your Twitter username:")
        return

    if task_index == 4:  # Task 5: Wallet address submission
        await context.bot.send_message(chat_id=user_id, text="Please submit your Caesium Wallet Address:")
        return

    if task_index == 5:  # Task 6: KYC screenshot submission
        # Ask for KYC confirmation
        keyboard = [
            [InlineKeyboardButton("✅ Yes", callback_data='kyc_done'),
             InlineKeyboardButton("❌ No", callback_data='kyc_not_done')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=user_id, text="Have you finished your KYC?", reply_markup=reply_markup)
        return

    # Check if the user is a member of the target group
    await check_membership(update, context)


  # or any other function to continue the process

async def complete_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    video_url ='https://i.ibb.co/dPRbVYk/congrats.gif'
    await context.bot.send_animation(chat_id=user_id, animation= video_url,caption=" 🎉 Congratulations! 🎉\n Once your KYC is approved, you will receive $50 worth of CSM.💸 "
                 "Thank you for being a part of our community. Stay connected for more updates and future airdrops.")

    # Wait for 2 seconds before sending the "more" button
    await asyncio.sleep(2)
    video1_url='https://i.ibb.co/dgBqdvk/more.gif'
    # Send the "more" button
    keyboard = [
        [InlineKeyboardButton("More", callback_data='more')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_animation(chat_id=user_id,animation=video1_url, caption=MORE_TASK, reply_markup=reply_markup)

#checking channel did the user have joined in the channel

async def check_membership(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    logger.info(f"Checking membership for user_id: {user_id} in channel: {TARGET_CHANNEL_CHAT_ID}")

    try:
        channel_member = await context.bot.get_chat_member(TARGET_CHANNEL_CHAT_ID, user_id)
        logger.info(f"Channel member status: {channel_member.status}")

        if channel_member.status in ['member', 'administrator', 'creator']:
            user = update.effective_user  # Get the user who sent the message
            first_name = user.first_name
            await context.bot.send_message(chat_id=user_id, text=f"Tada 🤗 {first_name}, stay tuned for updates.")
            await asyncio.sleep(2)
            await done_task_proceed(update, context)
        else:
            # Resend the task until the user joins
            context.job_queue.run_once(remind_user, 1, data=user_id)  # Use 'data' instead of 'context'

    except TelegramError as e:
        logger.error(f"Error checking membership: {e}")
        if "chat not found" in str(e).lower():
            # Resend the task until the user joins
            context.job_queue.run_once(remind_user, 1, data=user_id)  # Use 'data' instead of 'context'
        else:
            await context.bot.send_message(chat_id=user_id, text=f"An error occurred: {e}")

async def remind_user(context: CallbackContext):
    user_id = context.job.data  # Get the user_id from the job data
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=CHANNEL_LINK),
         InlineKeyboardButton("✅ Done", callback_data='done')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text="Please follow our Caesium Lab Channel.", reply_markup=reply_markup)

#checking group if the user had joined in the caesium lab group

async def check_membership1(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    logger.info(f"Checking membership for user_id: {user_id} in group1: {TARGET_GROUP1_CHAT_ID}")
    try:
        # Check if the user is a member of the group
        group1_member = await context.bot.get_chat_member(TARGET_GROUP1_CHAT_ID, user_id)
        logger.info(f"Group member status: {group1_member.status}")
        if  group1_member.status in ['member', 'administrator', 'creator']:
            user = update.effective_user  # Get the user who sent the message
            first_name = user.first_name
            await context.bot.send_message(chat_id=user_id, text=f"🤩 {first_name}, we sincerely appreciate you joining us. Stay tuned for exciting updates.")
            await asyncio.sleep(2)
            await done_task_proceed(update, context)
        else:
             # Resend the task until the user joins
            context.job_queue.run_once(remind_user1, 1, data=user_id)
    except TelegramError as e:
        logger.error(f"Error checking membership: {e}")
        if "chat not found" in str(e).lower():
            # Resend the task until the user joins
            context.job_queue.run_once(remind_user1, 1, data=user_id)
        else:
            await context.bot.send_message(chat_id=user_id, text=f"An error occurred: {e}")

async def check_membership2(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    logger.info(f"Checking membership for user_id: {user_id} in group2: {TARGET_GROUP2_CHAT_ID}")

    try:
        group2_member = await context.bot.get_chat_member(TARGET_GROUP2_CHAT_ID, user_id)
        logger.info(f"Member status: {group2_member.status}")
        if group2_member.status in ['member', 'administrator', 'creator']:
            user = update.effective_user  # Get the user who sent the message
            first_name = user.first_name
            await context.bot.send_message(chat_id=user_id, text=f"🥳 {first_name}, welcome aboard, and thank you for joining. Updates will follow shortly.")
            await asyncio.sleep(2)
            await done_task_proceed(update, context)
        else:
            # Resend the task until the user joins
            context.job_queue.run_once(remind_user2, 1, data=user_id)

    except TelegramError as e:
        logger.error(f"Error checking membership: {e}")
        if "chat not found" in str(e).lower():
            # Resend the task until the user joins
            context.job_queue.run_once(remind_user2, 1, data=user_id)
        else:
            await context.bot.send_message(chat_id=user_id, text=f"An error occurred: {e}")

async def done_task_proceed(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    task_index = user_tasks[user_id]

    if task_index < len(TASKS) - 1:  # Check if there are more tasks
        user_tasks[user_id] += 1  # Increment the task index
        await send_task(update, context)  # Send the next task
    else:
        user_id = update.effective_chat.id
        video_url ='https://i.ibb.co/dPRbVYk/congrats.gif'
        await context.bot.send_animation(chat_id=user_id, animation= video_url,caption=" 🎉 Congratulations! 🎉\n Once your KYC is approved, you will receive $50 worth of CSM.💸 "
                 "Thank you for being a part of our community. Stay connected for more updates and future airdrops.")

async def remind_user1(context: CallbackContext):
    user_id = context.job.data  # Use 'data' to access the user_id
    keyboard = [[
        InlineKeyboardButton("Join Media Group", url=GROUP1_LINK),
        InlineKeyboardButton("Done", callback_data='done')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text="Please follow our Caesium Lab Media group.", reply_markup=reply_markup)

async def remind_user2(context: CallbackContext):
    user_id = context.job.data  # Use 'data' to access the user_id
    keyboard = [
        [InlineKeyboardButton("Join AR Group", url=GROUP2_LINK),
        InlineKeyboardButton("Done", callback_data='done')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text="Please follow our Alpha returns group.", reply_markup=reply_markup)

async def handle_more(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    if user_id not in User_tasks:
        User_tasks[user_id] = 1  # Initialize if not present

    task_index1 = User_tasks[user_id]

    if task_index1 < len(More_task_List):
        task1_text = More_task_List[task_index1]
        keyboard = [
            [InlineKeyboardButton("✅ Done", callback_data='done_more'),
             InlineKeyboardButton("❌ Cancel", callback_data='cancel_more')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=user_id, parse_mode='HTML', text=task1_text, reply_markup=reply_markup
        )
    else:
        User_tasks[user_id] = 1  # Reset for future tasks
        video_url='https://i.ibb.co/dPRbVYk/congrats.gif'
        await context.bot.send_animation(
            chat_id=user_id,
            animation =video_url,
            caption=" 🎉 Congratulations! 🎉\nOnce your KYC is approved, you’ll receive $50 worth of CSM. 💸 Plus, enjoy an extra $12.5 worth of CSM for playing Alpha Returns! 🎉 Thank you for your support—stay tuned for more updates and future airdrops. 🚀 This is just the beginning!"
        )

async def done_more_task_proceed(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    if user_id not in User_tasks:
        User_tasks[user_id] = 1  # Initialize if not present

    task_index1 = User_tasks[user_id]

    if task_index1 < len(More_task_List) - 1:  # Check if there are more tasks
        User_tasks[user_id] += 1  # Increment the task index
        await handle_more(update, context)  # Send the next task
    else:
        video_url='https://i.ibb.co/dPRbVYk/congrats.gif'
        await context.bot.send_animation(
            chat_id=user_id,
            animation =video_url,
            caption=" 🎉 Congratulations! 🎉\nOnce your KYC is approved, you’ll receive $50 worth of CSM. 💸 Plus, enjoy an extra $12.5 worth of CSM by playing Alpha Returns. 🎉 Thank you for your support—stay tuned for more updates and future airdrops. 🚀 This is just the beginning!"
        )

async def done_more_task(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    if user_id not in User_tasks:
        User_tasks[user_id] = 1  # Initialize if not present
    await done_more_task_proceed(update, context)

async def cancel_task(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    user_tasks[user_id] = 0  # Reset to the first task
    await send_task(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Token value", callback_data='tokenvalue')],
        [InlineKeyboardButton("About", url='https://caesiumlab.com/blogs/unveils-a-visionary-2024-after-a-pivotal-caesium-crypto-stories-shaped-2023')],
        [InlineKeyboardButton("Raise Ticket", url='https://docs.google.com/forms/d/e/1FAIpQLSeV8nzqi0VEPXQVxT7EfjqUSMGAp_3Rj0LRgpiW6MgBPON0cg/viewform?usp=header')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='I am Alpha! How can I help you?', reply_markup=reply_markup)

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'how are you' in processed:
        return 'I am good!'
    return 'I do not understand what you wrote..'

async def send_data_to_apps_script(data):
    try:
        response = requests.post(apps_script_url, json=data)
        if response.status_code == 200:
            logger.info("Data sent successfully to Apps Script.")
        else:
            logger.error(f"Failed to send data to Apps Script: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Error sending data to Apps Script: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        channel_post = update.channel_post
        chat_id = channel_post.chat.id
        username = update.effective_user.username
        text = channel_post.text
        print(f'Channel Post from {channel_post.chat.title}: "{text}"')  # Debugging output

        if 'hello' in text.lower():
            print("returning to start command")
            video_url = 'https://i.ibb.co/m6Z7YZ1/welcome.gif'
            caption = ("Hey Welcome to the airdrop! 🎉\n"
               "\n⬇️ Complete the tasks below to earn <b>$50 worth of $CSM</b> tokens.\n"
               "\nℹ️ <b>About Caesium ($CSM):</b>\n"
               "Caesium ($CSM) is a fast, secure cryptocurrency enabling <b>decentralised finance (DeFi)</b> and a seamless wallet experience.\n"
               "\nℹ️ <b>About Alpha Returns:</b>\n"
               "\n<b>Alpha Returns</b>is the Play-to-Earn PvP game where players engage in exciting solo, duo, and squad modes. <b>You can convert the gold coins earned while playing into $CSM tokens.</b>\n"
               "\nThe airdrop ends on <b>31 Jan 2025</b>, and valid participants will be rewarded.\n\n"
               "🗒 <b>Airdrop Rules:</b>\n"
               "🔘 Follow our Telegram Channel\n"
               "🔘 Follow us on Twitter\n"
               "🔘 Download the Caesium Wallet and complete the KYC\n"
               "🔘 Submit your wallet address and sponsor code\n"
               "🔘 Refer friends to earn more\n"
               "\nClick the <b>Join Airdrop</b> button to submit your details and verify tasks."
    )

        keyboard = [[InlineKeyboardButton("Join AirDrop", callback_data='join_airdrop')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_animation(chat_id, animation=video_url, caption=caption, parse_mode='HTML', reply_markup=reply_markup)
        # Handle commands or messages in the channel
        if Bot_Username in text:
            user_id = update.effective_chat.id
            new_text = text.replace(Bot_Username, '').strip()
            response = handle_response(new_text)
            data = {'user_id': user_id,
                    'task_completed': True,
                     'message': text,
                     'type': 'channel',
                     'timestamp': str(datetime.datetime.now())
                }
            await context.bot.send_message(chat_id=chat_id, text=response)
            await send_data_to_apps_script(data)
            print(f"Received message1 from {user_id}: {text}")  # Debugging output
            taskName="Tasklist"
            return  # Exit after handling the channel post



    user_id = update.effective_chat.id
    username = update.effective_user.username
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')  # Debugging on get user id who sending message this text indicate what kind of text they were sending

       # Check if the message is from a group
    if message_type == 'supergroup':
        # Check if the bot's username is mentioned
        if Bot_Username in text:
            # Remove the bot's username from the text
            new_text: str = text.replace(Bot_Username, '').strip()  # Use strip() to remove leading/trailing spaces
             # Check if the new text contains 'hello'
            if user_id in user_tasks:
             task_index = user_tasks[user_id]  # Get the current task index for the user
             taskName = TASKS[task_index]  # Get the task name
            else:
             taskName = "No current task"  # Default message if user is not found
            if 'hello' in new_text.lower():
                print("Returning to start command")
                await start_command(update, context)  # Call the start command
                return
            print(f"Received message1 from {user_id}: {text}")  # Debugging output
            await log_user_message(user_id, username,text,taskName)
            response: str = handle_response(new_text)  # Generate a response based on the new text
            await update.message.reply_text(response)  # Send the response back to the group
            return  # Exit the function after processing the message
        else:
            return  # Do nothing if the bot's username is not mentioned


    if 'hello' in text.lower():
        print("returning to start command")
        await start_command(update, context)
        return

    elif user_id in user_tasks:
        task_index = user_tasks[user_id]

        if task_index == 3:  # Twitter username submission
            if text.startswith("@"):
             user_tasks[user_id] += 1  # Move to the next task
             await context.bot.send_message(chat_id=user_id, text=f"Twitter username '{text}' received. Now, proceed to the next task.")
             data = {'user_id': user_id,
                    'task_completed': True,
                     'message': text,
                     'type':message_type,
                     'timestamp': str(datetime.datetime.now())
                }
             await send_data_to_apps_script(data)
             print("data had send to send_data from index2")
             print(f"Received message1 from {user_id}: {text}")  # Debugging output
             taskName="Twitter ID"
             await log_user_message(user_id, username, text, taskName)
             await send_task(update, context)
            else:
                # Send an error message if the wallet address is invalid
                await context.bot.send_message(chat_id=user_id, text="❌ Invalid Twitter ID. Please ensure you are providing the valid ID.")
                await context.bot.send_message(chat_id=user_id, text="Please submit your Twitter ID:")
            return


        if task_index == 4:  # Task 2: Wallet address submission
            # Validate the wallet address
            if text.startswith("0x") and len(text) == 42 and " " not in text:
                user_tasks[user_id] += 1  # Move to the next task
                await context.bot.send_message(chat_id=user_id, text=f"Wallet address '{text}' received. Now, proceed to the next task.")
                data = {'user_id': user_id,
                    'task_completed': True,
                     'message': text,
                     'type':message_type,
                     'timestamp': str(datetime.datetime.now())
                    }
                await send_data_to_apps_script(data)
                print("data had send to send_data from index2")
                await send_task(update, context)
                print(f"Received message1 from {user_id}: {text}")  # Debugging output
                taskName="Wallet Adddress"
                await log_user_message(user_id, username, text, taskName)
            else:
                # Send an error message if the wallet address is invalid
                await context.bot.send_message(chat_id=user_id, text="❌ Invalid wallet address. Please ensure you are providing the valid Address.")
                await context.bot.send_message(chat_id=user_id, text="Please submit your Caesium Wallet Address:")
            return

        if task_index == 5:
                return

    if user_id not in User_tasks:
        User_tasks[user_id] = 1

    task_index1 = User_tasks[user_id]
    print(f"User  ID: {user_id}, Current Task Index: {task_index1}, Submitted Text: {text}")

# Handle the next task if the task index is 1 or higher
    if task_index1 == 1:
    # Logic for the next task goes here
        User_tasks[user_id] += 1  # Move to the next task
        await handle_more(update, context)
        await send_data_to_apps_script(data)
        print("data had send to send_data from index1: User_tasks")

    response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)

async def handle_kyc_confirmation(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    query = update.callback_query
    await query.answer()

    if query.data == 'kyc_done':
        # Proceed to the next step
        await complete_tasks(update, context)
    elif query.data == 'kyc_not_done':
        # Inform the user to complete KYC and provide a continue button
        keyboard = [
            [InlineKeyboardButton("Continue", callback_data='continue_kyc')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=user_id, text="Complete your KYC to proceed. Once done, click the continue button below.", reply_markup=reply_markup)

async def continue_kyc(update: Update, context: CallbackContext):
    await complete_tasks(update, context)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    # Prepare the new message based on the button clicked
    if query.data == 'tokenvalue':
        new_message = "The present Caesium token value is 11$"
        await context.bot.send_message(chat_id=query.message.chat.id, text=new_message)
    elif query.data == 'join_airdrop':
        await join_airdrop(update, context)
    elif query.data == 'done':
        await done_task(update, context)
    elif query.data == 'more':
        await handle_more(update, context)
    elif query.data == 'done_more':
        await done_more_task(update, context)
    elif query.data == 'cancel_more':
        await cancel_task(update, context)
    elif query.data == 'cancel':
        await cancel_task(update, context)
    elif query.data == 'kyc_done':
        await handle_kyc_confirmation(update, context)  # Ensure this is called correctly
    elif query.data == 'kyc_not_done':
        await handle_kyc_confirmation(update, context)
    elif query.data == 'continue_kyc':
        await continue_kyc(update, context)



if __name__ == '__main__':
    print('Starting')
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Handle only non-command text messages
    app.add_handler(CallbackQueryHandler(handle_kyc_confirmation))
    app.add_error_handler(error)
    print('Polling')

    # Run the application
    asyncio.run(app.run_polling())

