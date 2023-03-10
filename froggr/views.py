from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.text import slugify
from froggr_website.settings import MEDIA_URL
from froggr.forms import UserForm, UserProfileForm
from froggr.models import BlogPost, User, UserProfile
from froggr import forms
from datetime import datetime
from django.db.models import Q

# Create your views here.

def posts(request):
    return HttpResponse("Posts!")

def test(request):
    return render(request, 'test_template.html')

def test2(request):
    return render(request, 'test_template_2.html')

def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, 'Account created for: ' + username)
            return redirect('froggr:frog-in')
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def my_frogs(request):
    return render(request, 'my_frogs.html')

def get_user_profile_or_none(user):
    profile = None
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    return profile

def profile(request, profile_slug = None):
    user = None
    is_logged_in = False
    if request.path == reverse('froggr:profile'):
        user = request.user
    else:
        try:
            user = UserProfile.objects.get(profile_slug=profile_slug)
            user = user.user
        except UserProfile.DoesNotExist:
            user = None
    if user == None:
        return render(request, '404.html')

    if user == request.user:
        is_logged_in = True

    profile = get_user_profile_or_none(user)
    context_dict = {}
    context_dict["username"] = user.username
    context_dict["is_logged_in_profile"] = is_logged_in
    context_dict["profile_slug"] = "";
    if profile != None:
        context_dict["profile_img"] = profile.image
        context_dict["profile_text"] = profile.text
        context_dict["profile_slug"] = profile.profile_slug
    return render(request, 'profile.html', context_dict)

# returns the results of form.save() with image and user filled in
def handle_text_image_form(form, request):
    if form.is_valid():
        form.instance.user = request.user
        if 'image' in request.FILES:
            form.instance.image = request.FILES['image']
    else:
        print(form.errors)
                
@login_required
def create_profile(request):
    form = None
    profile = get_user_profile_or_none(request.user)
    if profile != None:
        form = forms.UserProfileForm(
            initial={'text':profile.text,'image':profile.image},
            instance=profile)
    else:
        form = forms.UserProfileForm()
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, instance=profile)
        handle_text_image_form(form, request)
        form.save()
        return redirect('froggr:profile')
        
    return render(request, "create_profile.html", {'profile_form': form})

@login_required
def create_frogg(request, post_slug=None):
    form = None
    post = None

    try:
        post = BlogPost.objects.get(post_slug=post_slug)
    except BlogPost.DoesNotExist:
        post = None
        
    if post != None:
        form = forms.BlogPostForm(
            initial={'title':post.title, 'image':post.image, 'text':post.text},
            instance=post)
    else:
        form = forms.BlogPostForm()
    error_message = None
    if request.method == 'POST':
        form = forms.BlogPostForm(request.POST, instance=post)
        handle_text_image_form(form, request)
        if form != None:
            form.instance.date = datetime.now().date()
            try:
                form.save()
                return redirect('froggr:posts', form.instance.post_slug)
            except IntegrityError:
                # this post already exists, save the inputted info and return form again
                form = forms.BlogPostForm(
                    initial={
                        'title':form.instance.title,
                        'image':form.instance.image,
                        'text':form.instance.text})
                error_message = "You already have a post with this title!"
    
    return render(request, 'create_frogg.html',
                  {'blog_form': form, 'post_slug' : post_slug, 'error_message': error_message})

def frogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('froggr:home')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    context = {}
    return render(request, 'frog_in.html', context)


def frogout(request):
    logout(request)
    return redirect(reverse('froggr:home'))


def posts(request, post_slug):
    try:
        post = BlogPost.objects.get(post_slug=post_slug)
    except BlogPost.DoesNotExist:
        return render(request, '404.html')
    context_dict = {}
    context_dict['blog_title'] = post.title
    context_dict['blog_img'] = post.image
    context_dict['blog_text'] = post.text
    context_dict['blog_author'] = post.user.username
    context_dict['author_url'] = UserProfile.objects.get(user=post.user).profile_slug
    if post.user == request.user:
        context_dict['user_owns_post'] = True
    context_dict['post_url'] = post_slug
    return render(request, 'frogg.html', context_dict)

# ---- views that return lists of posts    

INITIAL_LOAD = 21
PAGES_PER_LOAD = 6

def render_posts_for_ajax(query, count):
    load_size = PAGES_PER_LOAD
    if count == 0:
        load_size = INITIAL_LOAD
    posts = query.all()[count:(count + load_size)];
    post_data = ""
    for p in posts:
        post_data += render_to_string("post_box.html", { 'post' : p, 'MEDIA_URL' : MEDIA_URL})
    return post_data

def posts_page(request, query, base_page, base_context):
    count = 0
    first_load = False
    try:
        count = int(request.GET['post_count'])
    except KeyError:
        first_load = True

    if first_load:
        return render(request, base_page, base_context)
    else:
        return HttpResponse(render_posts_for_ajax(query, count))

def top_frogs(request):
    return posts_page(request, BlogPost.objects.order_by("-score"),
                      'home.html', {'post_view_title': 'Top Posts'})

def home(request):
    return posts_page(request, BlogPost.objects,
                      'home.html', {})

def list_user_posts(request, profile_slug):
    user = None
    try:
        user = UserProfile.objects.get(profile_slug=profile_slug).user
    except UserProfile.DoesNotExist:
        return render(request, "404.html")

    posts = BlogPost.objects.filter(user=user);

    return posts_page(request, BlogPost.objects.filter(user=user),
                      'home.html', {'post_view_title': "Posts by " + user.username })

def search_results(request, search_query=None):
    if request.method == "POST":
        searched = request.POST['searched']
        return redirect(reverse('froggr:search-results') + slugify(searched))
    if search_query == None:
        return redirect(reverse('froggr:no-results'))
    search_query = search_query.replace("-", " ")
    return posts_page(request,
                      BlogPost.objects.filter(
                          Q(text__icontains=search_query) | Q(title__icontains=search_query) |
                      Q(user__username__icontains=search_query)),
                      'search_results.html', {'searched':search_query})

def no_results(request):
    return render(request, "no_results.html")
