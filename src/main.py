import os.path

from database.db_setup import init_db


def main():
    # Set the path for the database
    db_path = os.path.join('database', 'coffee_manager.db')


    # Check if the database file exists, if not, initialize it
    if not os.path.exists(db_path):
        init_db(db_path)

if __name__ == "__main__":
    main() 