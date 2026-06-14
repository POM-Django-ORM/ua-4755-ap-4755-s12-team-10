from django.db import models
from django.utils import timezone
import datetime
from book.models import Book

class Order(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField()

    def __str__(self):
        end_at_str = f"'{self.end_at}'" if self.end_at else "None"
        return f"'id': {self.id}, 'user': CustomUser(id={self.user.id}), 'book': Book(id={self.book.id}), " \
               f"'created_at': '{self.created_at}', 'end_at': {end_at_str}, 'plated_end_at': '{self.plated_end_at}'"

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        return {
            'id': self.id,
            'book': self.book.id if self.book else None,
            'user': self.user.id if self.user else None,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
            'plated_end_at': int(self.plated_end_at.timestamp()) if self.plated_end_at else None,
        }

    @staticmethod
    def create(user, book, plated_end_at):
        # 1. Базова перевірка на наявність об'єктів
        if not user or not user.id or not book:
            return None

        # 2. Оновлюємо стан книги з бази (про всяк випадок)
        if hasattr(book, 'id') and book.id:
            try:
                book.refresh_from_db()
            except Exception:
                pass

        # 3. Рахуємо, скільки вже є АКТИВНИХ замовлень на цю книгу (де end_at ще не заповнено)
        # Якщо книга вже видана стільки ж разів, скільки її є в наявності — повертаємо None
        if hasattr(book, 'id') and book.id:
            active_orders_count = Order.objects.filter(book=book, end_at__isnull=True).count()
            if active_orders_count >= book.count:
                return None
        else:
            # Якщо у книги взагалі count <= 0 (для об'єктів не з бази)
            if hasattr(book, 'count') and book.count <= 0:
                return None

        # 4. Конвертація timestamp у datetime
        if isinstance(plated_end_at, int):
            plated_end_at = datetime.datetime.fromtimestamp(plated_end_at, tz=datetime.timezone.utc)

        try:
            order = Order.objects.create(
                user=user,
                book=book,
                plated_end_at=plated_end_at
            )
            return order
        except Exception:
            return None

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            if isinstance(plated_end_at, int):
                self.plated_end_at = datetime.datetime.fromtimestamp(plated_end_at, tz=datetime.timezone.utc)
            else:
                self.plated_end_at = plated_end_at
                
        if end_at is not None:
            if isinstance(end_at, int):
                self.end_at = datetime.datetime.fromtimestamp(end_at, tz=datetime.timezone.utc)
            else:
                self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at__isnull=True))

    @staticmethod
    def delete_by_id(order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False