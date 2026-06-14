from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)

class CustomUser(AbstractBaseUser):
    """
    This class represents a basic user.
    """
    first_name = models.CharField(max_length=20, default=None, null=True, blank=True)
    last_name = models.CharField(max_length=20, default=None, null=True, blank=True)
    middle_name = models.CharField(max_length=20, default=None, null=True, blank=True)
    email = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"'id': {self.id}, 'first_name': '{self.first_name}', 'middle_name': '{self.middle_name}', " \
               f"'last_name': '{self.last_name}', 'email': '{self.email}', 'created_at': {int(self.created_at.timestamp())}, " \
               f"'updated_at': {int(self.updated_at.timestamp())}, 'role': {self.role}, 'is_active': {self.is_active}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        # Валідація довжини рядків для уникнення DataError у PostgreSQL
        if (first_name and len(first_name) > 20) or \
           (middle_name and len(middle_name) > 20) or \
           (last_name and len(last_name) > 20) or \
           (email and len(email) > 100):
            return None

        # Перевірка базової валідності email, як очікують тести
        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            return None

        # Запобігання падінню при дублюванні email
        if CustomUser.objects.filter(email=email).exists():
            return None

        try:
            user = CustomUser(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name
            )
            user.save()
            return user
        except Exception:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'role': self.role,
            'is_active': self.is_active
        }

    def update(self, first_name=None, last_name=None, middle_name=None, password=None, role=None, is_active=None):
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if middle_name is not None:
            self.middle_name = middle_name
        if password is not None:
            self.password = password
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        self.save()

    @staticmethod
    def get_all():
        return list(CustomUser.objects.all())

    def get_role_name(self):
        return dict(ROLE_CHOICES).get(self.role)