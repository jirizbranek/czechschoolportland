import sqlite3
import os
from datetime import datetime

# Use environment variable for database path, fallback to local for development
DB_PATH = os.environ.get('DATABASE_PATH', 'school.db')
DB = DB_PATH

def get_connection():
    return sqlite3.connect(DB)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT,
                    location TEXT,
                    time TEXT,
                    invitation_link TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS mailing_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    subscription_date TEXT DEFAULT NULL)''')
    
    # Add new columns to events table if they don't exist (for existing databases)
    try:
        c.execute("ALTER TABLE events ADD COLUMN location TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE events ADD COLUMN time TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE events ADD COLUMN invitation_link TEXT")
    except sqlite3.OperationalError:
        pass
    
    # Add subscription_date column if it doesn't exist (for existing databases)
    try:
        c.execute("ALTER TABLE mailing_list ADD COLUMN subscription_date TEXT DEFAULT NULL")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Update existing records that don't have a subscription date
    c.execute("UPDATE mailing_list SET subscription_date = ? WHERE subscription_date IS NULL", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    
    # Normalize existing emails to lowercase
    c.execute("SELECT id, email FROM mailing_list")
    emails = c.fetchall()
    for email_id, email in emails:
        normalized_email = email.lower().strip()
        if email != normalized_email:
            try:
                c.execute("UPDATE mailing_list SET email = ? WHERE id = ?", (normalized_email, email_id))
            except sqlite3.IntegrityError:
                # If normalized email already exists, delete the duplicate
                c.execute("DELETE FROM mailing_list WHERE id = ?", (email_id,))
    
    conn.commit()
    conn.close()

def get_next_event():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT title, date, description, location, time, invitation_link FROM events WHERE date >= ? ORDER BY date ASC LIMIT 1",
              (datetime.now().strftime("%Y-%m-%d"),))
    event = c.fetchone()
    conn.close()
    return event

def get_all_events():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, date, description, location, time, invitation_link FROM events ORDER BY date ASC")
    events = c.fetchall()
    conn.close()
    return events

def add_event(title, date, description, location=None, time=None, invitation_link=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO events (title, date, description, location, time, invitation_link) VALUES (?, ?, ?, ?, ?, ?)", 
              (title, date, description, location, time, invitation_link))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()

def get_event_by_id(event_id):
    """Get a single event by its ID"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, date, description, location, time, invitation_link FROM events WHERE id=?", (event_id,))
    event = c.fetchone()
    conn.close()
    return event

def update_event(event_id, title, date, description, location=None, time=None, invitation_link=None):
    """Update an existing event"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE events SET title=?, date=?, description=?, location=?, time=?, invitation_link=? WHERE id=?", 
              (title, date, description, location, time, invitation_link, event_id))
    conn.commit()
    conn.close()

def add_email(email):
    conn = get_connection()
    c = conn.cursor()
    try:
        email_lower = email.lower().strip()  # Convert to lowercase and remove whitespace
        subscription_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO mailing_list (email, subscription_date) VALUES (?, ?)", (email_lower, subscription_date))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_mailing_list():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, email, subscription_date FROM mailing_list ORDER BY subscription_date DESC, email ASC")
    emails = c.fetchall()
    conn.close()
    return emails

def delete_email(email_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM mailing_list WHERE id=?", (email_id,))
    conn.commit()
    conn.close()

def email_exists(email):
    """Check if an email exists in the mailing list"""
    conn = get_connection()
    c = conn.cursor()
    email_lower = email.lower().strip()  # Convert to lowercase and remove whitespace
    c.execute("SELECT 1 FROM mailing_list WHERE email=?", (email_lower,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def unsubscribe_email(email):
    """Remove an email from the mailing list by email address"""
    conn = get_connection()
    c = conn.cursor()
    email_lower = email.lower().strip()  # Convert to lowercase and remove whitespace
    c.execute("DELETE FROM mailing_list WHERE email=?", (email_lower,))
    affected_rows = c.rowcount
    conn.commit()
    conn.close()
    return affected_rows > 0  # Return True if email was found and removed
