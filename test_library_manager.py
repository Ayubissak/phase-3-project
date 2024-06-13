import pytest
import sqlite3
import os
from library_manager import database
from library_manager.cli import CLI

DATABASE = 'test_library.db'

@pytest.fixture(scope='module')
def db():
    # Setup
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    database.DATABASE = DATABASE  # Use test database
    database.init_db()
    yield conn  # this is where the testing happens
    conn.close()
    # Teardown
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

@pytest.fixture(scope='module')
def cli(db):
    cli = CLI()
    cli.conn = db
    return cli

def test_add_member(cli):
    cli.add_member("John Doe", "john.doe@example.com")
    cur = cli.conn.cursor()
    cur.execute("SELECT * FROM members WHERE email = ?", ("john.doe@example.com",))
    member = cur.fetchone()
    assert member is not None
    assert member["name"] == "John Doe"
    assert member["email"] == "john.doe@example.com"

def test_delete_member(cli):
    cli.add_member("Jane Doe", "jane.doe@example.com")
    cur = cli.conn.cursor()
    cur.execute("SELECT * FROM members WHERE email = ?", ("jane.doe@example.com",))
    member = cur.fetchone()
    assert member is not None
    member_id = member["id"]
    cli.delete_member(member_id)
    cur.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    member = cur.fetchone()
    assert member is None

def test_add_book(cli):
    cli.add_book("The Great Gatsby", "F. Scott Fitzgerald")
    cur = cli.conn.cursor()
    cur.execute("SELECT * FROM books WHERE title = ?", ("The Great Gatsby",))
    book = cur.fetchone()
    assert book is not None
    assert book["title"] == "The Great Gatsby"
    assert book["author"] == "F. Scott Fitzgerald"

def test_delete_book(cli):
    cli.add_book("1984", "George Orwell")
    cur = cli.conn.cursor()
    cur.execute("SELECT * FROM books WHERE title = ?", ("1984",))
    book = cur.fetchone()
    assert book is not None
    book_id = book["id"]
    cli.delete_book(book_id)
    cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cur.fetchone()
    assert book is None

def test_borrow_book(cli):
    cli.add_member("Alice Smith", "alice.smith@example.com")
    cli.add_book("To Kill a Mockingbird", "Harper Lee")
    cur = cli.conn.cursor()
    cur.execute("SELECT * FROM members WHERE email = ?", ("alice.smith@example.com",))
    member = cur.fetchone()
    assert member is not None
    member_id = member["id"]
    cur.execute("SELECT * FROM books WHERE title = ?", ("To Kill a Mockingbird",))
    book = cur.fetchone()
    assert book is not None
    book_id = book["id"]
    cli.borrow_book(member_id, book_id)
    cur.execute("SELECT * FROM borrows WHERE member_id = ? AND book_id = ?", (member_id, book_id))
    borrow = cur.fetchone()
    assert borrow is not None
    assert borrow["member_id"] == member_id
    assert borrow["book_id"] == book_id

def test_return_book(cli):
    cur = cli.conn.cursor()
    cur.execute("SELECT * FROM members WHERE email = ?", ("alice.smith@example.com",))
    member = cur.fetchone()
    assert member is not None
    member_id = member["id"]
    cur.execute("SELECT * FROM books WHERE title = ?", ("To Kill a Mockingbird",))
    book = cur.fetchone()
    assert book is not None
    book_id = book["id"]
    cur.execute("SELECT * FROM borrows WHERE member_id = ? AND book_id = ?", (member_id, book_id))
    borrow = cur.fetchone()
    assert borrow is not None
    borrow_id = borrow["id"]
    cli.return_book(borrow_id)
    cur.execute("SELECT * FROM borrows WHERE id = ?"),
