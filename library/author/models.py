from django.db import models

class Author(models.Model):
    """
    This class represents an Author. 
    """
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)

    def __str__(self):
        return f"'id': {self.id}, 'name': '{self.name}', 'surname': '{self.surname}', 'patronymic': '{self.patronymic}'"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(author_id):
        try:
            return Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(author_id):
        try:
            author = Author.objects.get(id=author_id)
            author.delete()
            return True
        except Author.DoesNotExist:
            return False

    @staticmethod
    def create(name, surname, patronymic):
        # Перевірка на обмеження довжини varchar(20)
        if len(name) > 20 or len(surname) > 20 or len(patronymic) > 20:
            return None
        try:
            author = Author(name=name, surname=surname, patronymic=patronymic)
            author.save()
            return author
        except Exception:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
        }

    def update(self, name=None, surname=None, patronymic=None):
        if name is not None:
            if len(name) > 20:
                return
            self.name = name
        if surname is not None:
            if len(surname) > 20:
                return
            self.surname = surname
        if patronymic is not None:
            if len(patronymic) > 20:
                return
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        return list(Author.objects.all())