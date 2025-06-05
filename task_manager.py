import os
import sqlite3
import openai
from datetime import datetime

DB_PATH = 'tasks.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            effort_estimate TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_task(description, effort):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO tasks (description, effort_estimate, created_at) VALUES (?,?,?)',
        (description, effort, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def find_similar(description):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT description FROM tasks WHERE description LIKE ?', ('%'+description+'%',))
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results

def query_openai(task_text):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY not set')
    openai.api_key = api_key
    prompt = f"Schätze den Aufwand für folgende Aufgabe: '{task_text}'"
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}]
    )
    answer = response.choices[0].message.content.strip()
    return answer

def main():
    init_db()
    print('Beschreibe deine Aufgabe:')
    description = input().strip()
    if not description:
        print('Keine Aufgabe eingegeben.')
        return
    print('Sende Aufgabe an OpenAI...')
    effort = query_openai(description)
    similar = find_similar(description)
    save_task(description, effort)
    print('\nGeschätzter Aufwand:')
    print(effort)
    if similar:
        print('\nÄhnliche Aufgaben in der Datenbank:')
        for s in similar:
            print('-', s)
    else:
        print('\nKeine ähnlichen Aufgaben gefunden.')
    print('\nAufgabe wurde gespeichert.')

if __name__ == '__main__':
    main()
