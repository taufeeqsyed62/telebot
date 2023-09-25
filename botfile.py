import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters

# Create or connect to the database
conn = sqlite3.connect('subjects.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        name TEXT,
        notes TEXT,
        syllabus TEXT,
        assignments TEXT,
        previous_year_questions TEXT
    )
''')
conn.commit()

subjects_data = [
    ('COMPUTER GRAPHICS', 'Link to notes for Subject 1', 'Link to syllabus for Subject 1', 'Link to assignments for Subject 1', 'Link to previous year questions for Subject 1'),
    ('FUNDAMENTAL OF DATA ', 'Link to notes for Subject 2', 'Link to syllabus for Subject 2', 'Link to assignments for Subject 2', 'Link to previous year questions for Subject 2'),
    # Add more subjects and resources
]

for subject in subjects_data:
    cursor.execute('''
        INSERT INTO subjects (name, notes, syllabus, assignments, previous_year_questions)
        VALUES (?, ?, ?, ?, ?)
    ''', subject)

conn.commit()

def get_subject_info(subject_id):
    cursor.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,))
    return cursor.fetchone()

def update_subject(subject_id, notes, syllabus, assignments, previous_year_questions):
    cursor.execute('''
        UPDATE subjects
        SET notes = ?, syllabus = ?, assignments = ?, previous_year_questions = ?
        WHERE id = ?
    ''', (notes, syllabus, assignments, previous_year_questions, subject_id))
    conn.commit()

def delete_subject(subject_id):
    cursor.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
    conn.commit()

subjects = {
    1: {
        'name': 'COMPUTER GRAPHICS',
        'notes': 'https://mega.nz/file/D2AlwYgY#0S10f17gF5TfQ8olrsuS6aciDVZzk9k9rWvMfhS_zVU',
        'syllabus': 'https://mega.nz/file/O7xWVb7A#QDjbmshicEWH5WdRlbFkqWEqglzSaVawfCIAZJw2OJA',
        'assignments': 'Link to assignments for COMPUTER GRAPHICS',
        'previous_year_questions': 'https://mega.nz/file/67hjTSwI#ua75zlzjaL2v50orFtXtHTHCPEPDfKR4YFOfp_KyC7o'
    },
    2: {
        'name': 'FUNDAMENTAL OF DATA STRUCTURE',
        'notes': 'Link to notes for FDS',
        'syllabus': 'https://mega.nz/file/O7xWVb7A#QDjbmshicEWH5WdRlbFkqWEqglzSaVawfCIAZJw2OJA',
        'assignments': 'Link to assignments for FDS',
        'previous_year_questions': 'https://mega.nz/file/C2oEHCgY#vM7Z7oPLwYfFONSb9AYbhpO3aFrFBM4GIzxRYtJz8xM'
    },
    # Add more subjects
}

# Initialize the bot
updater = Updater(token='6312810364:AAES3PXnbyxjERNzBcCY_MJhvAiDOh5Wmaw', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to the Helpdesk Bot! Please select a subject by typing /select_subject.")

def select_subject(update, context):
    # Generate keyboard with subject options
    keyboard = [
        [str(subject_id) + '. ' + subject['name'] for subject_id, subject in subjects.items()]
    ]
    reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True, 'resize_keyboard': True}

    context.bot.send_message(chat_id=update.message.chat_id, text="Please select a subject:", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('select_subject', select_subject))

def subject_selected(update, context):
    user_choice = update.message.text.split('.')[0].strip()  # Extract the subject number
    try:
        subject = subjects[int(user_choice)]
        response = f"Subject: {subject['name']}\n\n" \
                   f"Notes: {subject['notes']}\n" \
                   f"Syllabus: {subject['syllabus']}\n" \
                   f"Assignments: {subject['assignments']}\n" \
                   f"Previous Year Questions: {subject['previous_year_questions']}"
        context.bot.send_message(chat_id=update.message.chat_id, text=response)
    except KeyError:
        context.bot.send_message(chat_id=update.message.chat_id, text="Invalid subject selection. Please select a valid subject.")

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, subject_selected))
updater.start_polling()
updater.idle()

# Close the database connection when done
conn.close()
