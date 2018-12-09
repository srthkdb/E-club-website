from .models import Box, Issued
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, IssuedForm, ReturnIssue, LocationForm
from django.views.generic import View


# Create your views here.

#list of boxes with location and items left in each box
def boxes_list(request):
    if not request.user.is_authenticated:
        return render(request, 'items/login.html')
    else:
        boxes = Box.objects.all()
        return render(request, 'items/box_list.html', {'boxes': boxes})

#list showing issues of a user
def myIssues(request):
    # if user is not a registered user, redirect them to login page
    if not request.user.is_authenticated:
        return render(request, 'items/login.html')
    else:
        user = request.user
        issues = Issued.objects.filter(user=request.user)
        return render(request, 'items/myIssues.html', {'user': user, 'issues': issues})

#list showing issues in a box (for admin)
def issues_by_box(request, box_id):
    if not request.user.is_authenticated:
        return render(request, 'items/login.html')
    else:
        user = request.user
        box = get_object_or_404(Box, pk=box_id)
        issues = Issued.objects.filter(box=box)
        return render(request, 'items/issues_by_box.html', {'user': user, 'issues': issues, 'box': box})

def create_issue(request):
    #use DiscussionFormIndex class from forms.py
    if not request.user.is_authenticated:
        return render(request, 'items/login.html')
    else:
        form = IssuedForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            #do not save to database now
            issue = form.save(commit=False)
            issue.user = request.user
            if issue.quantity_issued > issue.box.quantity_left: #if a picture is uploaded
                return render(request, 'items/issue_form.html', {'form': form, 'error_message': 'Quantity asked is more than the quantity of item available'})
            #save to database
            issue.box.quantity_left = issue.box.quantity_left - issue.quantity_issued
            issue.save()
            issue.box.save()

            return render(request, 'items/index.html', {})
        return render(request, 'items/issue_form.html', {'form': form})

def change_location(request):
    #use DiscussionFormIndex class from forms.py
    if not request.user.is_authenticated:
        return render(request, 'items/login.html')
    else:
        form = LocationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            #do not save to database now
            issue = form.save(commit=False)
            box = get_object_or_404(Box, number=issue.number)
            box.location = issue.location
            box.save()

            return render(request, 'items/index.html', {})
        return render(request, 'items/issue_form.html', {'form': form})

def create_return(request, issue_id):
    #use DiscussionFormIndex class from forms.py
    if not request.user.is_authenticated:
        return render(request, 'items/login.html')
    else:
        form = ReturnIssue(request.POST or None, request.FILES or None)
        issued = get_object_or_404(Issued, pk=issue_id)
        if form.is_valid():
            #do not save to database now
            issue = form.save(commit=False)
            if issue.return_number != issued.box.number: #if a picture is uploaded
                return render(request, 'items/return_form.html', {'form': form, 'error_message': 'Box number mismatch. Please put the item in the correct box.'})
            #save to database
            issued.returned = True
            issued.box.quantity_left = issued.box.quantity_left + issued.quantity_issued
            issued.return_number = issue.return_number
            issued.save()
            issued.box.save()

            return render(request, 'items/index.html', {})
        return render(request, 'items/issue_form.html', {'form': form})



def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'items/login.html', {"form": form})

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

class UserFormView(View):
    #Credits: code structure for this class is adapted from newboston django video tutorials.
    form_class = UserForm
    template_name = 'items/registration_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            #cleaned(normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            #add user to the database
            user.save()

            #returns user objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                #django gives admin power to suspend users. This option checks if the user is not suspended.
                if user.is_active:
                    login(request, user)
                    user = request.user
                    issues = Issued.objects.filter(user=request.user)
                    return render(request, 'items/myIssues.html', {'user': user, 'issues': issues})
        return render(request, self.template_name, {'form': form})


















