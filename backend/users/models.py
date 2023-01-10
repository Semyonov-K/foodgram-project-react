from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    USER_ROLES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
    ]
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=USER_ROLES,
                            default='user')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('username',)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.get_full_name()


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name="unique followers"),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='do not selffollow'),
        ]
