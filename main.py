from getpass import getpass

from app.auth import Auth
from app.dashboard import Dashboard
from app.database import Database
from app.ui import UI


def login_screen(auth, ui):
    ui.clear()
    ui.banner("COMPUTER LAB EQUIPMENT BORROWING SYSTEM", "Please log in")
    attempts = 0
    while attempts < 3:
        username = input("Username: ").strip()
        password = getpass("Password: ")
        if auth.login(username, password):
            return True
        attempts += 1
        ui.error(f"Wrong username or password. Attempts left: {3 - attempts}")
    return False


def main():
    db = Database()
    db.connect()
    db.setup()
    db.seed()

    auth = Auth(db)
    auth.create_default_users()
    ui = UI()

    if login_screen(auth, ui):
        ui.set_theme(auth.current_user["theme"])
        Dashboard(db, auth, ui).run()
        auth.logout()
        ui.message("You have been logged out. Goodbye!")
    else:
        ui.error("Too many failed attempts. Exiting.")

    db.close()


if __name__ == "__main__":
    main()