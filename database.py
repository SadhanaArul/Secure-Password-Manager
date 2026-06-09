import sqlite3
from encryption import EncryptionManager

class DatabaseManager:
    def __init__(self, db_name="password_manager.db"):
        self.db_name = db_name
        self.encryption = EncryptionManager()
        self.create_table()
    
    def create_table(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f"Database creation failed: {str(e)}")
    
    def save_password(self, website, username, password):
        try:
            if self.check_duplicate(website, username):
                raise Exception("Entry already exists for this website and username")
            
            encrypted_password = self.encryption.encrypt_password(password)
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO passwords (website, username, password)
                VALUES (?, ?, ?)
            """, (website, username, encrypted_password))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise Exception(f"Failed to save password: {str(e)}")
    
    def get_all_passwords(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT id, website, username, password FROM passwords")
            records = cursor.fetchall()
            
            decrypted_records = []
            for record in records:
                decrypted_password = self.encryption.decrypt_password(record[3])
                decrypted_records.append((record[0], record[1], record[2], decrypted_password))
            conn.close()
            return decrypted_records
        except Exception as e:
            raise Exception(f"Failed to retrieve passwords: {str(e)}")
    
    def search_passwords(self, search_term):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, website, username, password 
                FROM passwords 
                WHERE website LIKE ? OR username LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%"))
            records = cursor.fetchall()
            
            decrypted_records = []
            for record in records:
                decrypted_password = self.encryption.decrypt_password(record[3])
                decrypted_records.append((record[0], record[1], record[2], decrypted_password))
            conn.close()
            return decrypted_records
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")
    
    def delete_password(self, password_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            return deleted
        except Exception as e:
            raise Exception(f"Deletion failed: {str(e)}")
    
    def check_duplicate(self, website, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM passwords 
            WHERE website = ? AND username = ?
        """, (website, username))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists