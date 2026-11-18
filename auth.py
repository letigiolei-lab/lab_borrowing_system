"""User authentication, hashing, and password management."""

import hashlib
from database import Database

class AuthManager:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @classmethod
    def authenticate(cls, username, password):
        hashed = cls.hash_password(password)
        query = "SELECT id, username, full_name, role FROM users WHERE username = %s AND password_hash = %s"
        return Database.execute_single(query, (username, hashed))

    @classmethod
    def update_password(cls, user_id, old_pass, new_pass):
        user = Database.execute_single("SELECT password_hash FROM users WHERE id = %s", (user_id,))
        if not user:
            return False, "User not found."
        
        if user["password_hash"] != cls.hash_password(old_pass):
            return False, "Current password does not match."
        
        new_hashed = cls.hash_password(new_pass)
        success = Database.execute_query(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (new_hashed, user_id),
            commit=True
        )
        if success:
            return True, "Password successfully updated."
        return False, "Failed to update password."
