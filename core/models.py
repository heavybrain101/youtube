from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Employe(models.Model):
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    name = models.CharField(max_length=200,verbose_name="Имя")

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Имя")
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name="картинка")
    phone = models.CharField(max_length=200, verbose_name="телефон")
    office = models.CharField(max_length=200, verbose_name="работа")

    def __str__(self):
        return f'{self.name}'


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if 'password' in self.__dict__ and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)


class News(models.Model):
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    text = models.CharField(max_length=200,verbose_name="текст")
    title = models.CharField(max_length=200,verbose_name="название")
    image = models.ImageField(upload_to='news_images/',verbose_name="картинка")

    def __str__(self):
        return f'{self.title}'





class Wallet(models.Model):
    class Meta:
        verbose_name = "Бонус"
        verbose_name_plural = "Бонусы"
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, unique=True)
    wallet = models.IntegerField(default=4000,verbose_name="бонусы")

    def __str__(self):
        return f'{self.profile.name}'


class ShopCategory(models.Model):
    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"
    name = models.CharField(max_length=200,verbose_name="Имя")

    def __str__(self):
        return f'{self.name}'


class ShopItems(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    shop = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200,verbose_name="Имя")
    coast = models.IntegerField(verbose_name="стоимость")

    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(ShopItems)


@receiver(post_save, sender=Profile)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(profile=instance)
