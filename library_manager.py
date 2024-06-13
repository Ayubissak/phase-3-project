from db import init_db
from cli import CLI

def main():
    init_db()
    cli = CLI()
    cli.menu()

if __name__ == "__main__":
    main()
