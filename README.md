# 📚 Library Management System (Python Project)

A simple, console-based **Library Management System** built using **Python** and **Object-Oriented Programming (OOP)** principles. This beginner-level project simulates basic operations in a digital library, such as managing books and users, issuing and returning books, and saving data using JSON.


## 🚀 Features

- ➕ Add & Remove Books
- 👤 Register & Remove Users
- 📖 Borrow & Return Books
- 🔍 Search Books by Title, Author, or ISBN
- 💾 Persistent storage using JSON files
- 🖥️ Menu-driven interface using terminal/console


## 🧱 Tech Stack

- **Language**: Python 3  
- **Concepts**: OOP, File Handling, JSON  
- **Interface**: Text-based menu (CLI)


## 📂 Project Structure

- `Book` class: Manages book data and borrowing status  
- `User` class: Handles user details and borrowed books  
- `Library` class: Manages all logic and data persistence  
- `books.json` and `users.json`: Store system state  
- `main()` function: Interactive menu to control actions


## 🗓️ Development Timeline

| Day | Task                            | Output                             |
|-----|----------------------------------|-------------------------------------|
| 1   | Plan class structure            | Defined attributes & relationships |
| 2   | Implement core logic            | Created `Book`, `User`, `Library`  |
| 3   | Add JSON file storage           | Enabled `_save_data()` & `_load_data()` |
| 4   | Build interactive menu          | Console-based UI                   |
| 5   | Final testing & documentation   | Debugged and documented            |


## ✅ Sample Functionalities

```bash
1. Add Book
2. Register User
3. Borrow Book
4. Return Book
5. Search Book
6. Show All Books
7. Show All Users
8. Show User's Borrowed Books
9. Exit
