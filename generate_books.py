import random
import json

# Sample data
titles = ["The Great Adventure", "Mystery of the Lost Island", "Python Programming 101", 
          "Learning AI", "The Secrets of the Universe", "Diving into Deep Learning", 
          "The Art of War", "1984", "Pride and Prejudice", "Moby Dick", "The Burning Blade", "The Return of Flameheart", "How to Solve Riddle Guide", "How not to die in Valorant"]
authors = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", 
           "Chris Lee", "Emma Wilson", "Noah Davis", "Sophia Garcia", "Jane Doe", " Vivien Therese Basco Villalobos", "Pongpisut Somsagun"]
genres = ["Fiction", "Non-Fiction", "Science", "Fantasy", "Mystery", "Biography"]

def generate_books(num_books):
    books = []
    for _ in range(num_books):
        book = {
            "title": random.choice(titles),
            "author": random.choice(authors),
            "genre": random.choice(genres),
            "published_year": random.randint(1900, 2023),
            "isbn": f"{random.randint(1000000000, 9999999999)}"
        }
        books.append(book)
    return books

# Generate 50 random books
book_data = generate_books(50)

# Save to JSON file
with open('books.json', 'w') as f:
    json.dump(book_data, f, indent=4)

print("Generated random book data.")