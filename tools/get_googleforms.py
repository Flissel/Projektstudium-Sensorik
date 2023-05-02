import os
import psycopg2
from google.oauth2 import service_account
from googleapiclient import discovery

# Set up Google API client
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'path/to/file.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
sheets_service = discovery.build('sheets', 'v4', credentials=creds)

# Replace 'SHEET_ID' with your Google Sheet ID
SHEET_ID = '1dx2s1FcvATbaxgnFv-iY6UKELXOr1w2gk66rqvmORAg'

# Get questions and options from the response sheet
sheet_data = sheets_service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range='A2:C').execute()
questions = sheet_data['values']

def split_options(options_str):
    if not options_str:
        return []
    elif ';' in options_str:
        return [option.strip() for option in options_str.split(';')]
    elif ',' in options_str:
        return [option.strip() for option in options_str.split(',')]




def categorize_questions(questions):
    mc_questions = []
    text_questions = []
    list_questions = []
    grid_questions = []
    checkbox_grid_questions = []
    checkbox_questions = []

    for q in questions:
        if q[1] == 'MULTIPLE_CHOICE':
            mc_questions.append((q[0], split_options(q[2])))
        elif q[1] == 'TEXT':
            text_questions.append(q[0])
        elif q[1] == 'LIST':
            list_questions.append((q[0], split_options(q[2])))
        elif q[1] == 'GRID':
            grid_questions.append((q[0], split_options(q[2])))
        elif q[1] == 'CHECKBOX_GRID':
            checkbox_grid_questions.append((q[0], split_options(q[2])))
        elif q[1] == 'CHECKBOX':
            checkbox_questions.append((q[0], split_options(q[2])))

    return mc_questions, text_questions, list_questions, grid_questions, checkbox_grid_questions, checkbox_questions


def combine_all_questions(mc_questions, text_questions, list_questions, grid_questions, checkbox_grid_questions, checkbox_questions):
    return (
        [{'type': 'multiple_choice', 'question': q, 'options': o} for q, o in mc_questions] + 
        [{'type': 'text', 'question': q} for q in text_questions] + 
        [{'type': 'list', 'question': q, 'options': o} for q, o in list_questions] + 
        [{'type': 'grid', 'question': q, 'options': o} for q, o in grid_questions if q] +  # skip empty question
        [{'type': 'checkbox_grid', 'question': q, 'options': o} for q, o in checkbox_grid_questions] + 
        [{'type': 'checkbox', 'question': q, 'options': o} for q, o in checkbox_questions]
    )

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS multiple_choice_questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            option_1 TEXT,
            option_2 TEXT,
            option_3 TEXT,
            option_4 TEXT,
            option_5 TEXT,
            option_6 TEXT,
            option_7 TEXT,
            option_8 TEXT,
            option_9 TEXT,
            option_10 TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkbox_questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            option_1 TEXT,
            option_2 TEXT,
            option_3 TEXT,
            option_4 TEXT,
            option_5 TEXT,
            option_6 TEXT,
            option_7 TEXT,
            option_8 TEXT,
            option_9 TEXT,
            option_10 TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS list_questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            option_1 TEXT,
            option_2 TEXT,
            option_3 TEXT,
            option_4 TEXT,
            option_5 TEXT,
            option_6 TEXT,
            option_7 TEXT,
            option_8 TEXT,
            option_9 TEXT,
            option_10 TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grid_questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            rows TEXT,
            columns TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkbox_grid_questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            rows TEXT,
            columns TEXT
        );
    ''')
    conn.commit()




def save_questions(conn, questions):
    cursor = conn.cursor()
    for question in questions:
        title = question["question"]
        question_type = question["type"]
        options = question["options"]
        if question_type == 'multiple_choice':
            options = options + [None] * (10 - len(options))
            cursor.execute('''
                INSERT INTO multiple_choice_questions (
                    question, option_1, option_2, option_3, option_4,
                    option_5, option_6, option_7, option_8, option_9, option_10
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (title, *options))
        elif question_type == 'text':
            cursor.execute('INSERT INTO text_questions (question) VALUES (%s)', (title,))
        elif question_type == 'checkbox':
            options = options + [None] * (10 - len(options))
            cursor.execute('''
                INSERT INTO checkbox_questions (
                    question, option_1, option_2, option_3, option_4,
                    option_5, option_6, option_7, option_8, option_9, option_10
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (title, *options))
        elif question_type == 'list':
            options = options + [None] * (10 - len(options))
            cursor.execute('''
                INSERT INTO list_questions (
                question, option_1, option_2, option_3, option_4,
                option_5, option_6, option_7, option_8, option_9, option_10
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (title, *options))
        elif question_type == 'grid':
            if options:
                rows_str, columns_str = options
            else:
                rows_str, columns_str = None, None
            cursor.execute('''
                INSERT INTO grid_questions (
                question, rows, columns
                ) VALUES (%s, %s, %s)
                ''', (title, rows_str, columns_str))
        elif question_type == 'checkbox_grid':
            if options:
                rows_str, columns_str = options
            else:
                rows_str, columns_str = None, None
            cursor.execute('''
            INSERT INTO checkbox_grid_questions (
            question, rows, columns
            ) VALUES (%s, %s, %s)
            ''', (title, rows_str, columns_str))

    conn.commit()





# Set up PostgreSQL connection
conn = psycopg2.connect(
    host='localhost',
    database='praktikum_db',
    user='postgres',
    password='123'
)

# Categorize questions and extract options
mc_questions, text_questions, list_questions, grid_questions, checkbox_grid_questions, checkbox_questions = categorize_questions(questions)

print('Multiple choice questions:', mc_questions)
print('Text questions:', text_questions)
print('List questions:', list_questions)
print('Grid questions:', grid_questions)
print('Checkbox grid questions:', checkbox_grid_questions)
print('Checkbox questions:', checkbox_questions)

# Combine all question types into a single list
all_questions = combine_all_questions(mc_questions, text_questions, list_questions, grid_questions, checkbox_grid_questions, checkbox_questions)

# Create tables and save questions to the database
create_tables(conn)
save_questions(conn, all_questions)