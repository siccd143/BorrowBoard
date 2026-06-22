import sqlite3
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Initializes a table with columns for id, name, and email, offerings, needs, and 7-period schedules
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                offerings TEXT,
                needs TEXT,
                schedule_1 TEXT,
                schedule_2 TEXT,
                schedule_3 TEXT,
                schedule_4 TEXT,
                schedule_5 TEXT,
                schedule_6 TEXT,
                schedule_7 TEXT
            )
        ''')
        self.conn.commit()

    def stop(self):
        self.conn.close()

    def add_user(self, name, email, offerings, needs, schedules):
        # Adds a new user to the database with their offerings, needs, and 7-period schedules
        self.cursor.execute('''
            INSERT INTO users (name, email, offerings, needs, schedule_1, schedule_2, schedule_3, schedule_4, schedule_5, schedule_6, schedule_7)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, offerings, needs, *schedules))
        self.conn.commit()

    def get_user(self, email):
        # Retrieves a user's information from the database based on their email
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return self.cursor.fetchone()
    
    def update_user(self, email, name=None, offerings=None, needs=None, schedules=None):
        # Updates a user's information in the database based on their email
        updates = []
        params = []
        if name:
            updates.append("name = ?")
            params.append(name)
        if offerings:
            updates.append("offerings = ?")
            params.append(offerings)
        if needs:
            updates.append("needs = ?")
            params.append(needs)
        if schedules:
            for i in range(7):
                updates.append(f"schedule_{i+1} = ?")
                params.append(schedules[i])
        
        params.append(email)
        self.cursor.execute(f'''
            UPDATE users SET {', '.join(updates)} WHERE email = ?
        ''', params)
        self.conn.commit()
    
    def delete_user(self, email):
        # Deletes a user from the database based on their email
        self.cursor.execute('DELETE FROM users WHERE email = ?', (email,))
        self.conn.commit()
    
    def get_all_users(self):
        # Retrieves all users from the database
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

class User:
    def __init__(self, name, email, offerings, needs, schedules):
        self.name = name
        self.email = email
        self.offerings = offerings
        self.needs = needs
        self.schedules = schedules  # List of 7-period schedules

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "offerings": self.offerings,
            "needs": self.needs,
            "schedules": self.schedules
        }
    
    def from_dict(data):
        return User(
            name=data.get("name"),
            email=data.get("email"),
            offerings=data.get("offerings"),
            needs=data.get("needs"),
            schedules=data.get("schedules", [""] * 7)
        )
    
    def to_database(self, db):
        db.add_user(self.name, self.email, self.offerings, self.needs, self.schedules)