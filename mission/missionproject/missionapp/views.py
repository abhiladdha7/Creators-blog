from django.shortcuts import render
from django.shortcuts import render,get_object_or_404, redirect
from missionapp.models import Post,Comment,Category,UserProfile
from missionapp.forms import UserForm,UserProfileForm,PostForm,CommentForm,EditProfileForm,PostEditForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from datetime import datetime
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

class BlogStart(TemplateView):
    template_name='missionapp/blog_start.html'


def categoryList(request):
    categorys=Category.objects.all()
    posts=Post.objects.all()
    postlist=posts.filter(created_date__lte=datetime.now()).order_by('-created_date')[0:5]
    postviewlist=posts.filter(view_count__lte=1000000).order_by('-view_count')[0:5]
    if 'search' in request.GET:
        search_term=request.GET['search']
        posts=posts.filter(title__icontains=search_term)
        return render(request,'missionapp/post_list.html',context={'posts':posts,})
    else:
        return render(request,'missionapp/blog_start.html',context={'categorys':categorys,'posts':posts,'postlist':postlist,'postviewlist':postviewlist})


#class PostCategory(ListView):
#    model=Post
#    template_name='final_app/post_category.html'

#    def get_queryset(self):
#        self.category=get_object_or_404(Category,pk=self.kwargs['pk'])
#        return Post.objects.filter(category=self.category)


#    def get_context_data(self,**kwargs):
#        context=super(PostCategory,self).get_context_data(**kwargs)
#        context['category']=self.category
#        return context

def PostCategory(request,pk):
    category=get_object_or_404(Category,pk=pk)
    post=Post.objects.filter(category=category)
    recentpost=post.filter(created_date__lte=datetime.now()).order_by('-created_date')[0:5]
    if 'search' in request.GET:
        search_term=request.GET['search']
        post=post.filter(title__icontains=search_term).order_by('-created_date')

    context={
    'category':category,
    'post':post,
    'recentpost':recentpost,
    }
    return render(request,'missionapp/post_category.html',context)


def register(response):

    registered=False

    if response.method=='POST':
        user_form=UserForm(data=response.POST)
        profile_form=UserProfileForm(data=response.POST)

        if user_form.is_valid() and  profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in response.FILES:
                profile.profile_pic=response.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileForm()

    if registered:
        return redirect('user_login')

    return render(response,'missionapp/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(response):

    if response.method=='POST':
        username=response.POST.get('username')
        password=response.POST.get('password')

        user=authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(response,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(response,'missionapp/login.html',{})
        else:
            messages.error(response,'username or password incorrect!')
            return redirect('user_login')
    else:
        return render(response,'missionapp/login.html',{})


@login_required
def user_logout(response):
    logout(response)
    return(HttpResponseRedirect(reverse('index')))

class IndexView(TemplateView):
    template_name='missionapp/index.html'

class AboutView(TemplateView):
    template_name='missionapp/about.html'

def post_list(request):

    posts=Post.objects.all()
    recentpost=posts.filter(created_date__lte=datetime.now()).order_by('-created_date')[0:5]
    if 'search' in request.GET:
        search_term=request.GET['search']
        posts=posts.filter(title__icontains=search_term).order_by('-created_date')


    return render(request,"missionapp/post_list.html",{'posts':posts,'recentpost':recentpost})


class PostDetailView(DetailView):
    model=Post
    def get_object(self):
        object=super(PostDetailView,self).get_object()
        object.view_count+=1
        object.save()
        return object

#class PostCreateView(LoginRequiredMixin,CreateView):
#    login_url='/login/'
#    redirect_field_name='final_app/post_category.html'
#    form_class=PostForm
#    model=Post
#    template_name='final_app/post_form.html'
#    instance.user=request.user
#    instance.save()

@login_required
def PostCreateView(request):
    user1=[]
    #user1=get_object_or_404(UserProfileInfo)
    user1=User.objects.all()
    for user in user1:
        if user.is_active:

            form=PostForm(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                if 'post_img' in request.FILES:
                    instance.profile_pic=request.FILES['profile_pic']

                instance.save()

                return HttpResponseRedirect(instance.get_absolute_url())

    context={'form':form}
    return render(request,'missionapp/post_form.html',context)


#class PostUpdateView(LoginRequiredMixin,UpdateView):
#        login_url='/login/'
#        redirect_field_name='final_app/post_detail.html'
#        form_class=PostForm
#        model=Post
#        Post.user=user

def PostUpdateView(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=PostEditForm(request.POST or None,instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form=PostEditForm(instance=post)
    context={'form':form,'post':post}
    return render(request,'missionapp/post_edit.html',context)

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
        login_url='/login/'
        redirect_field_name='missionapp/post_list.html'
        model=Post

        def get_queryset(self):
            return Post.objects.filter(created_date__isnull=True).order_by('created_date')

@login_required
def post_publish(response,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model=Comment
    success_url=reverse_lazy('post_list')



@login_required
def add_comment_to_post(response,pk):
    post=get_object_or_404(Post,pk=pk)
    user1=[]
    user1=User.objects.all()

    for user in user1:
        if user.is_active:

                form=CommentForm(response.POST)
                if form.is_valid():
                    comment=form.save(commit=False)
                    comment.post=post
                    comment.user=response.user
                    comment.save()
                    return redirect('post_detail',pk=post.pk)
    context={'form':form}
    return render(response,'missionapp/comment_form.html',context)

@login_required
def comment_approve(reponse,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(r,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)


########

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'missionapp/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'missionapp/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('view_profile'))
        else:
            return redirect(reverse('change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'missionapp/change_password.html', args)


def UserPosts(request):
    postly=[]
    user=[]
    user=User.objects.all()
    posts=Post.objects.all()
    for user1 in user:
        if user1.is_active:
            for post in posts:
                if post.user==user1:
                    postly.add(post)
    return render(request,'missionapp/user_post_list.html',postly)


def userposts(request):
    user = request.user
    user_posts = Post.objects.filter(user=request.user).order_by('-created_date')
    template = 'missionapp/user_post_list.html'
    if 'search' in request.GET:
        search_term=request.GET['search']
        user_posts=user_posts.filter(title__icontains=search_term).order_by('-created_date')

    return render(request, template, {'user_posts':user_posts,'user': user})

##############


class privacy_policy(TemplateView):
    template_name='missionapp/privacy_policy.html'

class termsandcondition(TemplateView):
    template_name='missionapp/termsandcondition.html'

class contactus(TemplateView):
    template_name='missionapp/contactus.html'

class pressrelease(TemplateView):
    template_name='missionapp/pressrelease.html'

# Create your views here.
