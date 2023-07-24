import sys
import mysql.connector
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class StartWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Start")
        self.setGeometry(100, 100, 700, 600)

        image_label = QLabel(self)
        pixmap = QPixmap("img/books.png")
        scaled_pixmap = pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("background-color: transparent;")

        self.start_button = QPushButton("Get started")
        self.start_button.setStyleSheet("font-size: 20px; background-color: #947d73; color: black")
        self.start_button.setFixedSize(700, 40)

        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(self.start_button)
        self.setLayout(layout)


class DatabaseWindow(QMainWindow):

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("all")
        self.setGeometry(820, 100, 450, 400)
        self.setStyleSheet("background-color: #e9d5ca;")
        self.setWindowIcon(QIcon("img/book_s.png"))

        self.list_widget = QListWidget()
        self.list_widget.addItems(data)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Search")
        self.setGeometry(100, 100, 700, 600)

        self.search_label = QLabel("Search by Title or Author:")
        self.search_label.setFont(QFont("Times New Roman", 16))

        self.search_box = QLineEdit()
        self.search_box.setFixedSize(700, 40)
        self.search_box.setFont(QFont("Times New Roman", 16))

        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("font-size: 20px; background-color: #947d73; color: black")
        self.search_button.setFixedSize(700, 40)

        self.results_label = QLabel("Search Results:")
        self.results_label.setFont(QFont("Times New Roman", 16))

        self.results_box = QLineEdit()
        self.results_box.setFixedSize(700, 110)
        self.results_box.setFont(QFont("Times New Roman", 16))
        self.results_box.setReadOnly(True)

        self.results_list = QListWidget()
        self.results_list.setFixedSize(700, 140)
        self.results_list.setFont(QFont("Times New Roman", 16))

        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet("font-size: 20px; background-color: #947d73; color: black")
        self.add_button.setFixedSize(700, 40)

        self.delete_label = QLabel("Delete by Title:")
        self.delete_label.setFont(QFont("Times New Roman", 16))

        self.delete_box = QLineEdit()
        self.delete_box.setFixedSize(700, 60)
        self.delete_box.setFont(QFont("Times New Roman", 16))

        self.delete_button = QPushButton("Delete")
        self.delete_button.setStyleSheet("font-size: 20px; background-color: #947d73; color: black")
        self.delete_button.setFixedSize(700, 40)

        layout = QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_box)
        layout.addWidget(self.search_button)

        layout.addWidget(self.results_label)
        layout.addWidget(self.results_list)

        layout.addWidget(self.delete_label)
        layout.addWidget(self.delete_box)
        layout.addWidget(self.delete_button)

        layout.addWidget(self.add_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.search_button.clicked.connect(self.search_books)
        self.add_button.clicked.connect(self.show_add_window)
        self.delete_button.clicked.connect(self.delete_book)

        self.create_button()

    def create_button(self):
        action = QAction("Database", self)
        action.setFont(QFont("Times New Roman", 16))
        action.triggered.connect(self.go_to_database)

        self.menuBar().addAction(action)

    def go_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="azzza666",
                database="book_store"
            )
            cursor = connection.cursor()
            query = "SELECT title, author FROM books"
            cursor.execute(query)
            results = cursor.fetchall()

            books = ['{} - {}'.format(book[0], book[1]) for book in results]

            self.database_window = DatabaseWindow(books)
            self.database_window.show()

            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print("Failed to fetch data from database: {}".format(error))

    def search_books(self):
        search_input = self.search_box.text()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="azzza666",
                database="book_store"
            )
            cursor = connection.cursor()

            query = "SELECT title, author FROM books WHERE title LIKE '%{}%' OR author LIKE '%{}%'".format(
                search_input, search_input)

            cursor.execute(query)
            results = cursor.fetchall()

            # Очищаем QListWidget перед добавлением новых результатов
            self.results_list.clear()

            for book in results:
                # Отображаем результаты в столбике с помощью QListWidget
                item_text = '{} - {}'.format(book[0], book[1])
                self.results_list.addItem(item_text)

            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print("Failed to search books from database: {}".format(error))

    def delete_book(self):
        delete_input = self.delete_box.text()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="azzza666",
                database="book_store"
            )
            cursor = connection.cursor()

            query = "DELETE FROM books WHERE title = '{}'".format(delete_input)

            cursor.execute(query)
            connection.commit()

            self.delete_box.setText("")

            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print("Failed to delete book from database: {}".format(error))

    def show_add_window(self):
        self.add_window = AddWindow(self)
        self.add_window.show()


class AddWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Book")
        self.setGeometry(820, 100, 450, 400)

        self.title_label = QLabel("Title:")
        self.title_label.setFont(QFont("Times New Roman", 16))

        self.title_box = QLineEdit()
        self.title_box = QLineEdit(self)
        self.title_box.setFont(QFont("Times New Roman", 16))
        self.title_box.setFixedSize(450, 40)

        self.author_label = QLabel("Author:")
        self.author_label.setFont(QFont("Times New Roman", 16))

        self.author_box = QLineEdit()
        self.author_box = QLineEdit(self)
        self.author_box.setFont(QFont("Times New Roman", 16))
        self.author_box.setFixedSize(450, 40)

        self.price_label = QLabel("Price:")
        self.price_label.setFont(QFont("Times New Roman", 16))

        self.price_box = QLineEdit()
        self.price_box = QLineEdit(self)
        self.price_box.setFont(QFont("Times New Roman", 16))
        self.price_box.setFixedSize(450, 40)

        self.language_label = QLabel("Language:")
        self.language_label.setFont(QFont("Times New Roman", 16))

        self.language_box = QLineEdit()
        self.language_box = QLineEdit(self)
        self.language_box.setFont(QFont("Times New Roman", 16))
        self.language_box.setFixedSize(450, 40)

        self.add_button = QPushButton("Add", self)
        self.add_button.setStyleSheet("font-size: 20px; background-color: #947d73; color: black")
        self.add_button.setFixedSize(450, 40)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_box)

        layout.addWidget(self.author_label)
        layout.addWidget(self.author_box)

        layout.addWidget(self.price_label)
        layout.addWidget(self.price_box)

        layout.addWidget(self.language_label)
        layout.addWidget(self.language_box)

        layout.addWidget(self.add_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.add_button.clicked.connect(self.add_book)

    def add_book(self):
        title = self.title_box.text()
        author = self.author_box.text()
        price = self.price_box.text()
        language = self.language_box.text()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="azzza666",
                database="book_store"
            )
            cursor = connection.cursor()

            query = "INSERT INTO books (title, author, price, language) VALUES (%s, %s, %s, %s)"
            values = (title, author, price, language)

            cursor.execute(query, values)
            connection.commit()

            self.title_box.setText("")
            self.author_box.setText("")
            self.price_box.setText("")
            self.year_box.setText("")

            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print("Failed to add book to database: {}".format(error))


class CombinedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database search engine")
        self.setGeometry(100, 100, 700, 600)

        self.setStyleSheet("background-color: #e9d5ca;")
        self.setWindowIcon(QIcon("img/book_s.png"))

        self.login_widget = StartWindow(self)
        self.setCentralWidget(self.login_widget)
        self.login_widget.start_button.clicked.connect(self.show_search_window)

    def show_search_window(self):
        self.search_window = MainWindow()
        self.setCentralWidget(self.search_window)

    def show_add_window(self):
        self.add_window = AddWindow()
        self.setWindowTitle(self.add_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CombinedWindow()
    window.show()
    sys.exit(app.exec())
