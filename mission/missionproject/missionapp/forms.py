from django import forms
from missionapp.models import Post,Comment,UserProfile
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from tinymce.models import TinyMCE

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields=['username','first_name','last_name','email','password']

class UserProfileForm(forms.ModelForm):
    class Meta():
        model=UserProfile
        fields=['profile_pic','portfolio_site']


########

class EditProfileForm(UserChangeForm):
    template_name='/something/else'


    class Meta:
        model = User

        fields = [
            'email',
            'first_name',
            'last_name',
            'password',

        ]

class PostForm(forms.ModelForm):

    user=User.username

    class Meta():
        model=Post

        fields=['category','title','content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }



class CommentForm(forms.ModelForm):

    class Meta():
        model=Comment
        fields=['content']

        widgets = {

            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


        #widgets={
        #'author':forms.TextInput(attrs={'class':'textinputclass'}),
        #'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent' })
        #}


class PostEditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=[

        'category',
        'title',
        'content',
        ]

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
