from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator

# Create your models here.
class UserManager(BaseUserManager):
    def create_superuser(self, first_name, last_name, username, phone, country_code, password):
        user = self.model(
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone=phone,
                country_code=country_code,
                password=password
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    country_code = models.IntegerField(default=91)
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(validators=[MinLengthValidator(10)], max_length=10, blank=False, null=False, unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'country_code']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        s = self.name + '(' + self.city.name + ')'
        return s

class Venue(models.Model):
    name = models.CharField(max_length=100)
    matches = models.IntegerField(default=0)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        s = self.name + '(' + self.city.name + ')'
        return s

class Team(models.Model):
    name = models.CharField(max_length=100)
    captain = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    xp = models.IntegerField(default=0)

    def __str__(self):
        s = self.name + '(' + self.school.name + ')'
        return s

class Match(models.Model):
    date = models.DateTimeField(verbose_name='match_date')
    upcoming = models.BooleanField(default=True)
    past = models.BooleanField(default=False)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='player1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='player2')
    refree = models.CharField(max_length=100, null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    tie = models.BooleanField(default=False)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        s = self.team1.name + ' vs ' + self.team.name
        return s

#class Bet(models.Model)
