import sqlite3
import json
import os

def setup():
    module_dir = '../legal-luminary/modules/judiciary-rd-agent'
    db_path = os.path.join(module_dir, 'judiciary.sqlite')
    json_path = os.path.join(module_dir, 'judiciary_db.json')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS officials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        name TEXT,
        elected_date TEXT,
        term_end TEXT,
        re_election_year INTEGER,
        type TEXT,
        url TEXT,
        headshot_url TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS public_notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        notice_date TEXT,
        content TEXT,
        url TEXT
    )
    ''')

    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            
            for off in data.get('officials', []):
                cursor.execute('''
                INSERT INTO officials (title, name, elected_date, term_end, re_election_year, type, url, headshot_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    off.get('title'), off.get('name'), off.get('elected_date'), 
                    off.get('term_end'), off.get('re_election_year'), off.get('type'), 
                    off.get('url'), off.get('headshot_url')
                ))
        os.remove(json_path)
    
    conn.commit()
    conn.close()
    print("Database migration to SQLite complete.")

if __name__ == '__main__':
    setup()
