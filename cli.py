import sqlite3
import db
import utils

class CLI:
    def __init__(self):
        self.conn = db.get_db_connection()

    def menu(self):
        while True:
            print("\nLibrary Manager")
            print("1. Add Member")
            print("2. Delete Member")
            print("3. Add Book")
            print("4. Delete Book")
            print("5. Borrow Book")
            print("6. Return Book")
            print("7. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_member()
            elif choice == '2':
                self.delete_member()
            elif choice == '3':
                self.add_book()
            elif choice == '4':
                self.delete_book()
            elif choice == '5':
                self.borrow_book()
            elif choice == '6':
                self.return_book()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_member(self, name=None, email=None):
        if not name:
            name = input("Enter member name: ")
        if not email:
            email = input("Enter member email: ")
        with self.conn:
            self.conn.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
        print(f"Member '{name}' added.")

    def delete_member(self, member_id=None):
        if not member_id:
            member_id = utils.get_input("Enter member ID: ", int)
        with self.conn:
            self.conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
        print(f"Member with ID '{member_id}' deleted.")

    def add_book(self, title=None, author=None):
        if not title:
            title = input("Enter book title: ")
        if not author:
            author = input("Enter book author: ")
        with self.conn:
            self.conn.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        print(f"Book '{title}' added.")

    def delete_book(self, book_id=None):
        if not book_id:
            book_id = utils.get_input("Enter book ID: ", int)
        with self.conn:
            self.conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        print(f"Book with ID '{book_id}' deleted.")

    def borrow_book(self, member_id=None, book_id=None):
        if not member_id:
            member_id = utils.get_input("Enter member ID: ", int)
        if not book_id:
            book_id = utils.get_input("Enter book ID: ", int)
        with self.conn:
            self.conn.execute("INSERT INTO borrows (member_id, book_id) VALUES (?, ?)", (member_id, book_id))
        print(f"Book with ID '{book_id}' borrowed by member with ID '{member_id}'.")

    def return_book(self, borrow_id=None):
        if not borrow_id:
            borrow_id = utils.get_input("Enter borrow ID: ", int)
        with self.conn:
            self.conn.execute("DELETE FROM borrows WHERE id = ?", (borrow_id,))
        print(f"Borrow record with ID '{borrow_id}' deleted.")
