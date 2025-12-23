# main.py

import os
from dotenv import load_dotenv
load_dotenv()

import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ---------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Load bot token from environment
# ---------------------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Please define it in your .env file.")

# ---------------------------------------------------------------------
# Message content
# ---------------------------------------------------------------------
jokes = [
    "I told my computer I needed a break, and it said no problem—it froze.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "I’m reading a book about anti-gravity—it’s impossible to put down.",
    "Why did the math book look sad? It had too many problems.",
    "I asked my dog what’s two minus two—he said nothing.",
    "Why don’t eggs tell jokes? They might crack up.",
    "I used to play piano by ear, but now I use my hands.",
    "Why did the scarecrow get promoted? He was outstanding in his field.",
    "I tried to catch fog yesterday—mist.",
    "Why did the bicycle fall over? It was two-tired.",
    "I don’t trust stairs—they’re always up to something.",
    "Why did the coffee file a police report? It got mugged.",
    "I told my calendar a joke—it had a few dates.",
    "Why don’t scientists trust atoms? They make up everything.",
    "I used to hate facial hair, but then it grew on me.",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "I’m on a seafood diet—I see food and I eat it.",
    "Why was the math lecture so long? The professor kept going off on tangents.",
    "I gave up on learning how to juggle—I just couldn’t keep it up.",
    "Why did the tomato blush? It saw the salad dressing.",
    "I tried to be a baker, but I couldn’t make enough dough.",
    "Why don’t programmers like nature? Too many bugs.",
    "I once had a job at a calendar factory, but I got fired for taking a day off.",
    "Why did the picture go to jail? It was framed.",
    "I told a joke about construction, but I’m still working on it.",
    "Why did the computer go to the doctor? It caught a virus.",
    "I asked the librarian if the library had books on paranoia—she whispered, ‘They’re right behind you.’",
    "Why don’t cows have hobbies? They’re always outstanding in their field.",
    "I used to be indecisive, but now I’m not so sure.",
    "Why did the music teacher need a ladder? To reach the high notes.",
    "I bought some shoes from a drug dealer—I don’t know what he laced them with, but I was tripping all day.",
    "Why did the clock get kicked out of class? It kept ticking.",
    "I tried to learn origami, but I folded under pressure.",
    "Why did the banana go to the doctor? It wasn’t peeling well.",
    "I once told a chemistry joke—there was no reaction.",
    "Why did the stadium get hot after the game? All the fans left.",
    "I started a band called 1023MB—we haven’t gotten a gig yet.",
    "Why did the cookie go to the hospital? It felt crummy.",
    "I told my boss three companies were after me, so he gave me a raise—Turns out it was the electric, water, and gas companies.",
    "Why did the pencil break up with the eraser? It felt rubbed the wrong way.",
    "I tried to write a joke about time travel, but you didn’t like it.",
    "Why did the computer sit on its glasses? To improve its website.",
    "I don’t play soccer because I enjoy it—I’m just doing it for kicks.",
    "Why did the elevator get promoted? It really rose to the occasion.",
    "I told my friend 10 jokes to make him laugh—sadly, no pun in ten did.",
    "Why did the sheep get a job? To earn a little extra baaa-money.",
    "I tried to organize a hide-and-seek tournament, but good players were hard to find.",
    "Why did the notebook apply for a job? It wanted to make a good impression.",
    "I started exercising, but I keep losing my balance—turns out I’m running out of time."
]

motivations = [
    "Start your day with a clear priority.",
    "Write down your top three tasks.",
    "Break large tasks into smaller steps.",
    "Eliminate obvious distractions.",
    "Set a specific start time for work.",
    "Use a simple to-do list.",
    "Focus on one task at a time.",
    "Batch similar tasks together.",
    "Set short, focused work sessions.",
    "Take regular short breaks.",
    "Plan tomorrow before ending today.",
    "Keep your workspace tidy.",
    "Turn off nonessential notifications.",
    "Work during your most energetic hours.",
    "Define what done looks like.",
    "Set realistic daily goals.",
    "Start with the hardest task first.",
    "Use a timer to stay focused.",
    "Limit meetings when possible.",
    "Prepare everything you need in advance.",
    "Review progress at the end of the day.",
    "Avoid multitasking.",
    "Create simple routines.",
    "Decide quickly on small choices.",
    "Track where your time goes.",
    "Group emails and messages into blocks.",
    "Say no to low-value tasks.",
    "Automate repetitive work when possible.",
    "Keep important information easy to find.",
    "Use checklists for repeatable tasks.",
    "Focus on outcomes, not busyness.",
    "Set deadlines, even self-imposed ones.",
    "Reduce context switching.",
    "Work in quiet or focused environments.",
    "Clarify expectations before starting.",
    "Limit social media during work hours.",
    "Do quick tasks immediately if appropriate.",
    "Review priorities weekly.",
    "End tasks completely before switching.",
    "Keep a single trusted task system.",
    "Rest enough to stay effective.",
    "Simplify processes whenever possible.",
    "Learn keyboard shortcuts for common actions.",
    "Delegate when appropriate.",
    "Keep goals visible.",
    "Start tasks even if motivation is low.",
    "Avoid perfectionism.",
    "Close unused tabs and apps.",
    "Reflect on what works and adjust.",
    "Protect uninterrupted focus time."
]

productivity_tips = [
    "Start your day with a clear priority.",
    "Write down your top three tasks.",
    "Break large tasks into smaller steps.",
    "Eliminate obvious distractions.",
    "Set a specific start time for work.",
    "Use a simple to-do list.",
    "Focus on one task at a time.",
    "Batch similar tasks together.",
    "Set short, focused work sessions.",
    "Take regular short breaks.",
    "Plan tomorrow before ending today.",
    "Keep your workspace tidy.",
    "Turn off nonessential notifications.",
    "Work during your most energetic hours.",
    "Define what done looks like.",
    "Set realistic daily goals.",
    "Start with the hardest task first.",
    "Use a timer to stay focused.",
    "Limit meetings when possible.",
    "Prepare everything you need in advance.",
    "Review progress at the end of the day.",
    "Avoid multitasking.",
    "Create simple routines.",
    "Decide quickly on small choices.",
    "Track where your time goes.",
    "Group emails and messages into blocks.",
    "Say no to low-value tasks.",
    "Automate repetitive work when possible.",
    "Keep important information easy to find.",
    "Use checklists for repeatable tasks.",
    "Focus on outcomes, not busyness.",
    "Set deadlines, even self-imposed ones.",
    "Reduce context switching.",
    "Work in quiet or focused environments.",
    "Clarify expectations before starting.",
    "Limit social media during work hours.",
    "Do quick tasks immediately if appropriate.",
    "Review priorities weekly.",
    "End tasks completely before switching.",
    "Keep a single trusted task system.",
    "Rest enough to stay effective.",
    "Simplify processes whenever possible.",
    "Learn keyboard shortcuts for common actions.",
    "Delegate when appropriate.",
    "Keep goals visible.",
    "Start tasks even if motivation is low.",
    "Avoid perfectionism.",
    "Close unused tabs and apps.",
    "Reflect on what works and adjust.",
    "Protect uninterrupted focus time."
]

# ---------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Tell me a joke"],
        ["Motivate me"],
        ["Give me a productivity tip"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    await update.message.reply_text(
        "Welcome. Choose one of the options below.",
        reply_markup=reply_markup,
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Tell me a joke":
        response = random.choice(jokes)
    elif text == "Motivate me":
        response = random.choice(motivations)
    elif text == "Give me a productivity tip":
        response = random.choice(productivity_tips)
    else:
        response = "Please use the buttons to choose an option."

    await update.message.reply_text(response)

# ---------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------
def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    logger.info("Bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
