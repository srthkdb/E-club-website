from .models import Box, Issued
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, Issued
import datetime

# Create your views here.

#home page
def index(request):
    #if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'items/login.html')
    # enter the webpage only if the user is a registered user
    else:
        return render(request, 'items/index.html', {})

#list of boxes with location and items left in each box
def boxes_list(request, box_id):
    if not request.user.is_authenticated:
        return render(request, 'index/login.html')
    else:
        boxes = Box.objects.all()
        return render(request, 'index/box_list.html', {'boxes': boxes})

#list showing issues of a user
def myIssues(request):
    # if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'index/login.html')
    else:
        user = request.user
        issues = Issued.objects.filter(user=request.user)
        return render(request, 'index/myIssues.html', {'user': user, 'issues': issues})

#list showing issues in a box (for admin)
def issues_by_box(request, box_id):
    if not request.user.is_authenticated:
        return render(request, 'index/login.html')
    else:
        user = request.user
        box = get_object_or_404(Box, pk=box_id)
        issues = Issued.objects.filter(box=box)
        return render(request, 'index/issues_by_box.html', {'user': user, 'issues': issues, 'box': box})

def create_issue(request):
    #use DiscussionFormIndex class from forms.py
    if not request.user.is_authenticated:
        return render(request, 'index/login.html')
    else:
        form = Issued(request.POST or None, request.FILES or None)
        if form.is_valid():
            #do not save to database now
            issue = form.save(commit=False)
            issue.user = request.user
            issue.issue_date = datetime.date.now()
            if issue.quantity_issued > issue.box.quantity_left: #if a picture is uploaded
                return render(request, 'items/issue_form.html', {'form': form, 'error_message': 'Quantity asked is more than the quantity of item available'})
            #save to database
            issue.save()
            return render(request, 'home/index.html', {})
        return render(request, 'home/issue_form.html', {'form': form})

def create_return(request, issue_id):
    #use DiscussionFormIndex class from forms.py
    if not request.user.is_authenticated:
        return render(request, 'index/login.html')
    else:
        form = Issued(request.POST or None, request.FILES or None)
        issued = get_object_or_404(Issued, pk=issue_id)
        if form.is_valid():
            #do not save to database now
            issue = form.save(commit=False)
            if issue.return_number != issued.box.number: #if a picture is uploaded
                return render(request, 'items/return_form.html', {'form': form, 'error_message': 'Box number mismatch. Please put the item in the correct box.'})
            #save to database
            issued.return_date = datetime.date.now()
            issued.returned = True
            issued.return_number = issue.return_number
            issued.save()
            return render(request, 'home/index.html', {})
        return render(request, 'home/issue_form.html', {'form': form})



def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'home/login.html', {"form": form})

#logging in a user
def login_user(request):
    #if user is already logged in, return them to homepage
    if request.user.is_authenticated:
        return render(request, 'items/index.html', {'error_message': 'You are already logged in! Click on the Oraculi button on the top left corner of screen'})
    #process form data
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        #if user exists
        if user is not None:
            #if user is not suspended
            if user.is_active:
                #login funtion is already in request
                login(request, user)
                return render(request, 'items/index.html', {})
            else:
                return render(request, 'items/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'items/login.html', {'error_message': 'Invalid login'})
    return render(request, 'items/login.html')


















