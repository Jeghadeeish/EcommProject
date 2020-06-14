from django.contrib.auth import authenticate, login, get_user_model

from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm, GuestForm
from .models import GuestEmail

from django.utils.http import is_safe_url
# Create your views here.

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context={
        "form":form #LoginForm class object
    }
    print("User Logged in ",request.user.is_authenticated)  # Built in Django function. In 3.0 no need to () for this function
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid(): 
        print(form.cleaned_data)
        email    = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')
    return redirect('/register/')


def login_page(request):
    form = LoginForm(request.POST or None)
    context={
        "form":form #LoginForm class object
    }
    print("User Logged in ",request.user.is_authenticated)  # Built in Django function. In 3.0 no need to () for this function
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
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
            try:
                del request.session['guest_email_id']
            except:
                pass
            # Redirect to a success page.
            #context['form']=LoginForm() 
            #if you put : in this it will not clear the session context['form']:LoginForm()
            # return redirect('/login')

            # --------- Redirect to correct page after login
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            # Return an 'invalid login' error message.
            print("Error")
    return render(request,'accounts/login.html',context)


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
    return render(request,'accounts/register.html',context) #if you have not given context page will be empty. form wont be visible.