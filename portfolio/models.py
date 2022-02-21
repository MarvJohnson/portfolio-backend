from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
  def create_user(self, username, email, password=None):
    if not email:
      raise ValueError('Users must have an email address')

    user = self.model(
      username=username,
      email=self.normalize_email(email),
    )
    user.set_password(password)
    user.is_active = True
    user.save(using=self._db)
    return user

  def create_superuser(self, username, email, password=None):
    user = self.create_user(
      username,
      email,
      password=password,
    )
    user.is_superuser = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser):
  username = models.CharField(max_length=500, unique=True)
  password = models.CharField(max_length=500)
  email = models.EmailField()
  is_active = models.BooleanField()
  is_superuser = models.BooleanField(default=False)
  last_login = models.DateTimeField(null=True)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  EMAIL_FIELD = 'email'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
    return self.username

  def has_perm(self,  perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True

  @property
  def is_staff(self):
    return self.is_superuser

class Post(models.Model):
  title = models.CharField(max_length=100)
  topic = models.CharField(max_length=100)

  def __str__(self):
    return self.title

class PostSection(models.Model):
  title = models.CharField(max_length=100)
  post = models.ForeignKey(
    Post,
    related_name='sections',
    on_delete=models.CASCADE
  )
  
  def __str__(self):
    return f'{self.post.title} | {self.id}'

class PostSectionContent(models.Model):
  post_section = models.ForeignKey(
    PostSection,
    related_name='contents',
    on_delete=models.CASCADE
  )
  ContentType = models.TextChoices('ContentType', 'PARAGRAPH IMAGE')
  type = models.CharField(choices=ContentType.choices, max_length=10)
  content = models.TextField(max_length=2000)

  def __str__(self):
    return f'{self.post_section.id} | {self.content[0:10]}'

class Comment(models.Model):
  author = models.ForeignKey(
    User,
    related_name='comments',
    on_delete=models.CASCADE
  )
  post = models.ForeignKey(
    Post,
    related_name='comments',
    on_delete=models.CASCADE
  )
  replies = models.ForeignKey(
    'self',
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )
  text = models.TextField(max_length=2000)

  def __str__(self):
    return f'{self.author.username} | {self.text[0:100]}'

class UserCommentVote(models.Model):
  user = models.ForeignKey(
    User,
    related_name='votes',
    on_delete=models.CASCADE
  )
  comment = models.ForeignKey(
    Comment,
    related_name='votes',
    on_delete=models.CASCADE
  )
  vote = models.IntegerField()

  def __str__(self):
    return f'{self.user.username} | {self.vote}'