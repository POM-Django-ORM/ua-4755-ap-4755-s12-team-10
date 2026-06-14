from django.db import models
from author.models import Author

class Book(models.Model):
    """
    This class represents a Book.
    """
    name = models.CharField(max_length=128)
    description = models.TextField()
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        authors_list = [author.id for author in self.authors.all()]
        return f"'id': {self.id}, 'name': '{self.name}', 'description': '{self.description}', 'count': {self.count}, 'authors': {authors_list}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return True
        except Book.DoesNotExist:
            return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        # Перевірка на обмеження довжини імені (max_length=128)
        if name is not None and len(name) > 128:
            return None
        try:
            book = Book.objects.create(name=name, description=description, count=count)
            if authors:
                book.authors.set(authors)
            return book
        except Exception:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.id for author in self.authors.all()]
        }

    def update(self, name=None, description=None, count=None):
        if name is not None:
            if len(name) > 128:
                return
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        if authors:
            self.authors.add(*authors)

    def remove_authors(self, authors):
        if authors:
            self.authors.remove(*authors)

    @staticmethod
    def get_all():
        return list(Book.objects.all())