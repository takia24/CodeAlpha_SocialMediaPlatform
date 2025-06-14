from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone


from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'  # Added related_name
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='default.jpg',  # Added default image
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"  # Improved string representation

    @property
    def followers_count(self):
        """Returns number of followers"""
        return self.user.followers.count()

    @property
    def following_count(self):
        """Returns number of users being followed"""
        return self.user.following.count()

    @property
    def full_name(self):
        """Returns user's full name"""
        return f"{self.user.first_name} {self.user.last_name}".strip()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, 
        related_name='liked_posts', 
        blank=True,
        through='Like'  # Using through model to track additional like data
    )
    
    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.author.username}'s post: {self.content[:30]}..."

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

    class Meta:
        ordering = ['created_at']

class Follow(models.Model):
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following'
    )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_objects')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} likes {self.post}"
    
# models.py এর Post মডেলে যোগ করো:
@property
def like_count(self):
    return self.likes.count()

@property
def comment_count(self):
    return self.comments.count()

    
    
