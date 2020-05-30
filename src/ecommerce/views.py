from django.contrib.auth import authenticate, login, get_user_model

from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import ContactForm,LoginForm,RegisterForm


def home_page(request):
    #return HttpResponse("Hello World")
    context = {
        "title":"Hello World!",     #This will get showed in home_page.html title variable
        "content":"Welcome to home page",    #This will get showed in home_page.html content variable
        #"premium_content":"Yeahhhhhhh"
    }
    #return render(request,"home_page.html",{})
    if request.user.is_authenticated:
        context["premium_content"]="YEAHHHHHHHHH"
    return render(request,"home_page.html",context)


def about_page(request):
    context = {
        "title":"About Page",
        "content":"Welcome to about page"
    }
    return render(request,"home_page.html",context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact",
        "content":"Welcome to contact page",
        "form":contact_form,
        "brand": "new Brand Name"
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    '''
    if request.method == 'POST':
        print(request.POST)

        <QueryDict: {'csrfmiddlewaretoken': ['Bf8pMnK13KZGrBZx6z9xnq7QbSoCHNH6s2JJpOQSuKH3GHNcLxm6mcNRRy49vZ2F'], 'fullname': ['abc']}>
        
        print(request.POST.get('fullname'))
        print(request.POST.get('email'))
        print(request.POST.get('content'))
    '''
    return render(request,"contact/view.html",context)
def login_page(request):
    form = LoginForm(request.POST or None)
    context={
        "form":form #LoginForm class object
    }
    print("User Logged in ",request.user.is_authenticated)  # Built in Django function. In 3.0 no need to () for this function
    if form.is_valid(): 
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print("Logged in user:",user)
        print(request.user.is_authenticated)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            # Redirect to a success page.
            #context['form']=LoginForm() 
            #if you put : in this it will not clear the session context['form']:LoginForm()
            return redirect('/login')
        else:
            # Return an 'invalid login' error message.
            print("Error")
    return render(request,'auth/login.html',context)


User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username,email,password)
        print(new_user)
    return render(request,'auth/register.html',context) #if you have not given context page will be empty. form wont be visible.