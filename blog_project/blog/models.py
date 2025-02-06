# blog/models.py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField()  # RichTextField for rich content
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    contributors = models.ManyToManyField(User, related_name='contributed_posts', blank=True) 
    category = models.ManyToManyField(Category, related_name="posts")
    is_premium = models.BooleanField(default=False)  # Paywall protection
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class  UserProfile(models.Model):
    uu_id = models.UUIDField(default=uuid.uuid4,  unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="./static/images/background-class.jpeg")
    bio = models.TextField(max_length=500, default="Ente your bio")
    posts = models.ManyToManyField(Post)


    status  = models.CharField(
        max_length=20, choices=[("Regular", "Regular"), ("Premium", "Premium"),], blank=True, default="Regular")
    
    def __str__(self):
        return self.user.username
    
    




# class Comments(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Links comment to a post
#     name = models.CharField(max_length=255)
#     body = models.TextField() 
  
#     created = models.DateTimeField(auto_now_add=True)  # Timestamp when comment is created

#     class Meta:
#         ordering = ['created']  # Orders comments by creation time
#         indexes = [models.Index(fields=['created'])]  # Indexing for faster querying

#     def __str__(self):
#         return f'Comment by {self.name} on "{self.post.title}"'

    




class Comments(models.Model):
    post = models.ForeignKey(Post,  on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment by {self.user} on {self.post}'

class Invitation(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation to {self.email} for '{self.post.title}'"
    


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional: If you want to link the user to the subscription
    subscription_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Subscription by {self.email}"
