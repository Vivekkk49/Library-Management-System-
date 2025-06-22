import json

class Book:
    def __init__(self, title, author, isbn):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_borrowed = False

    @property
    def title(self): return self._title

    @property
    def author(self): return self._author

    @property
    def isbn(self): return self._isbn

    @property
    def is_borrowed(self): return self._is_borrowed

    @is_borrowed.setter
    def is_borrowed(self, value):
        if isinstance(value, bool):
            self._is_borrowed = value

    def borrow(self):
        if not self._is_borrowed:
            self._is_borrowed = True
            return True
        return False

    def return_book(self):
        if self._is_borrowed:
            self._is_borrowed = False
            return True
        return False

    def __str__(self):
        status = "Borrowed" if self._is_borrowed else "Available"
        return f"Title: {self._title}, Author: {self._author}, ISBN: {self._isbn}, Status: {status}"

    def to_dict(self):
        return {
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "borrowed": self._is_borrowed
        }

class User:
    def __init__(self, name, user_id):
        self._name = name
        self._user_id = user_id
        self._borrowed_books_isbns = []

    @property
    def name(self): return self._name

    @property
    def user_id(self): return self._user_id

    @property
    def borrowed_books_isbns(self): return self._borrowed_books_isbns.copy()

    def add_borrowed_book_isbn(self, isbn):
        if isbn not in self._borrowed_books_isbns:
            self._borrowed_books_isbns.append(isbn)

    def remove_borrowed_book_isbn(self, isbn):
        if isbn in self._borrowed_books_isbns:
            self._borrowed_books_isbns.remove(isbn)

    def __str__(self):
        return f"User: {self._name} (ID: {self._user_id}), Borrowed Books: {len(self._borrowed_books_isbns)}"

    def to_dict(self):
        return {
            "name": self._name,
            "user_id": self._user_id,
            "borrowed": self._borrowed_books_isbns
        }

class Library:
    def __init__(self, book_file='books.json', user_file='users.json'):
        self._books = {}
        self._users = {}
        self._data_file_books = book_file
        self._data_file_users = user_file
        self._load_data()

    def _load_data(self):
        try:
            with open(self._data_file_books, 'r') as f:
                for d in json.load(f):
                    book = Book(d['title'], d['author'], d['isbn'])
                    book.is_borrowed = d['borrowed']
                    self._books[book.isbn] = book
        except FileNotFoundError:
            pass

        try:
            with open(self._data_file_users, 'r') as f:
                for d in json.load(f):
                    user = User(d['name'], d['user_id'])
                    for isbn in d['borrowed']:
                        user.add_borrowed_book_isbn(isbn)
                    self._users[user.user_id] = user
        except FileNotFoundError:
            pass

    def _save_data(self):
        with open(self._data_file_books, 'w') as f:
            json.dump([b.to_dict() for b in self._books.values()], f, indent=2)
        with open(self._data_file_users, 'w') as f:
            json.dump([u.to_dict() for u in self._users.values()], f, indent=2)

    def add_book(self, book):
        if book.isbn in self._books:
            return False
        self._books[book.isbn] = book
        self._save_data()
        return True

    def remove_book(self, isbn):
        book = self._books.get(isbn)
        if book and not book.is_borrowed:
            del self._books[isbn]
            self._save_data()
            return True
        return False

    def register_user(self, user):
        if user.user_id in self._users:
            return False
        self._users[user.user_id] = user
        self._save_data()
        return True

    def remove_user(self, user_id):
        user = self._users.get(user_id)
        if user and not user.borrowed_books_isbns:
            del self._users[user_id]
            self._save_data()
            return True
        return False

    def borrow_book(self, isbn, user_id):
        book = self._books.get(isbn)
        user = self._users.get(user_id)
        if book and user and not book.is_borrowed:
            if book.borrow():
                user.add_borrowed_book_isbn(isbn)
                self._save_data()
                return True
        return False

    def return_book(self, isbn, user_id):
        book = self._books.get(isbn)
        user = self._users.get(user_id)
        if book and user and isbn in user.borrowed_books_isbns:
            if book.return_book():
                user.remove_borrowed_book_isbn(isbn)
                self._save_data()
                return True
        return False

    def search_book(self, query):
        result = []
        query = query.lower()
        for book in self._books.values():
            if query in book.title.lower() or query in book.author.lower() or query in book.isbn:
                result.append(book)
        return result

    def display_all_books(self, show_available_only=False):
        for book in self._books.values():
            if not show_available_only or not book.is_borrowed:
                print(book)

    def display_all_users(self):
        for user in self._users.values():
            print(user)

    def display_user_borrowed_books(self, user_id):
        user = self._users.get(user_id)
        if user:
            for isbn in user.borrowed_books_isbns:
                print(self._books.get(isbn))
        else:
            print("User not found.")

def main():
    library = Library()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Register User")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Book")
        print("6. Show All Books")
        print("7. Show All Users")
        print("8. Show User's Borrowed Books")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            t = input("Enter book title: ")
            a = input("Enter author name: ")
            i = input("Enter ISBN: ")
            library.add_book(Book(t, a, i))

        elif choice == '2':
            n = input("Enter user name: ")
            uid = input("Enter user ID: ")
            library.register_user(User(n, uid))

        elif choice == '3':
            uid = input("Enter user ID: ")
            i = input("Enter ISBN to borrow: ")
            if not library.borrow_book(i, uid):
                print("Borrow failed.")

        elif choice == '4':
            uid = input("Enter user ID: ")
            i = input("Enter ISBN to return: ")
            if not library.return_book(i, uid):
                print("Return failed.")

        elif choice == '5':
            q = input("Search title/author/ISBN: ")
            books = library.search_book(q)
            for book in books:
                print(book)

        elif choice == '6':
            library.display_all_books()

        elif choice == '7':
            library.display_all_users()

        elif choice == '8':
            uid = input("Enter user ID: ")
            library.display_user_borrowed_books(uid)

        elif choice == '9':
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
