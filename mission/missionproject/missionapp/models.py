from django.db import models

# Create your models here.
from tinymce.models  import HTMLField
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
#from final_project.settings import TINYMCE_PROFILE
from django.db.models.signals import post_save
#from updown.fields import RatingField
#from tinymce import HTMLField
from django.conf import settings
# Create your models here.

class UserProfile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE,unique=True)

    portfolio_site=models.URLField(blank=True)
    profile_pic=models.ImageField(upload_to='profile_pic',blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    cat_name=models.CharField(max_length=256)
    parent=models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)


    def __str__(self):
        full_path=[self.cat_name]
        k= self.parent
        while k is not None:
            full_path.append(k.cat_name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('post_by_category',args=[self.cat_name])

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    title=models.CharField(max_length=300)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    #description = tinymce_models.HTMLField()
    #rating=RatingField(can_change_vote=True)
    content=models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(default=datetime.now)
    post_img=models.ImageField(upload_to='profile_pic',blank=True)
    #published_date = models.DateTimeField(blank=True, null=True)

    #def publish(self):
    #    self.published_date = datetime.now()
    #    self.save()

    def comment_count(self):
        return self.comments

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})


    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(max_length=200)
    #rating=RatingField(can_change_vote=True)
    created_date = models.DateTimeField(default=datetime.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.content
