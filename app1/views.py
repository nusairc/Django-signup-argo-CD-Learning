from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control


# Create your views here.

 
@login_required(login_url='login')    
@cache_control(no_cache=True,must_revalidate=True,no_store=True) 
def Homepage(request):
    if request.user.is_authenticated:

        return render (request,'home.html')
    return render(request,'login.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True) 
def Signuppage(request):
    if request.method =='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            messages.error(request,' passwords dont match')
            return HttpResponseRedirect('signup')
        
        if User.objects.filter(username=uname):
            messages.error(request, "Username already exist!")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, "email already exist!")
            return redirect('signup')
        
        if not uname.strip():
            messages.error(request,'username is required....')
            return redirect('signup')

        if not email.strip():
            messages.error(request,'mail id required....')
            return redirect('signup')
        
        if not pass1.strip():
            messages.error(request,'password is required....')
            return redirect('signup')
        
        if len(uname)>10:
            messages.error(request, "Username shouldnot exceed 10 characters")
            return redirect('signup')
        
        if not uname.isalnum():
            messages.error(request, "Username must be alpha numeric!")
            return redirect('signup')
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            messages.error(request, "Account Created")
            return redirect('login')
    
    if request.user.is_authenticated:
        return redirect('home')
        
    return render(request,'signup.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
def Loginpage(request):

    if request.method =='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)

        if user is not None:
            login(request,user)
            request.session['username']=username
            return redirect('home')
        else:
            messages.error(request,' invalid credentials')
            return HttpResponseRedirect('/')
    if request.user.is_authenticated:
        return redirect('home')
    return render (request,'login.html')

####
@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
def LogoutPage(request):
    logout(request)
    return redirect('login')



#admin views


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('index_admin')
    
    return render(request,'admin_login.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def is_admin(request):
    if request.method == 'POST':
        
        username=request.POST.get('username')
        pass1=request.POST.get('pass')

        user=authenticate(request,username=username, password=pass1)

        if user is not None and user.is_superuser:
            login(request,user)
            request.session['username'] =username
            messages.error(request,"login succes to admin panel....",extra_tags='login_success')
            
            return redirect('index_admin')
        else:
            messages.error(request, 'Sorry you are not admin....!',extra_tags='failed_login')
            
            return redirect('admin_view')
        
    if request.user.is_authenticated:
        
        return redirect('index_admin')
    return render(request, 'admin_login.html')


@login_required(login_url='admin_view')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_signout(request):
    logout(request)
    messages.success(request,'Admin Logged Out Successfully!...',extra_tags='logout')
    return redirect('admin_view')
        

@login_required(login_url='admin_view')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def index_admin(request):
    if request.user.is_superuser:
        users=User.objects.all()
        return render(request,'admin_panel.html',{'user':users})
    else:
        return redirect('admin_view')

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add(request):
    return render(request,'add_user.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_user(request):
    username=request.POST['username']
    email=request.POST['email'].strip()
    pass1=request.POST['pass1'].strip()


    if not username:
        messages.error(request,'Username is required ....')
        return redirect('add')
    
    if not email:
        messages.error(request,'mail address is required ....')
        return redirect('add')
    

    if User.objects.filter(username=username).exists():
        messages.error(request,'This username is already taken...')
        return redirect('add')


    if User.objects.filter(email=email).exists():
        messages.error(request,'This mail id is already taken...')
        return redirect('add')
        

    user=User.objects.create_user(username=username,email=email)
    user.save()
    user=User.objects.get(username=username)
    user.set_password(pass1)
    user.save()
    return redirect('index_admin')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update(request,id):
    # mem=Member.objects.get(id=id)
    mem=User.objects.get(id=id)
    return render(request,'update.html',{'mem':mem})


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def updatedata(request, id):
#     username = request.POST['username'].strip()
#     email = request.POST['email'].strip()


#     if not username:
#         messages.error(request, 'Username is required.')
#         return redirect('update',id)

#     if not email:
#         messages.error(request, 'Email address is required.')
#         return redirect('update',id)
    
#     if User.objects.filter(username=username).exists():
#         messages.error(request,'This username exists')
#         return redirect('update',id)


#     if User.objects.filter(email=email).exists():
#         messages.error(request,'This mail id exists')
#         return redirect('update',id)

#     mem = User.objects.get(id=id)
#     mem.username = username
#     mem.email = email
#     mem.save()
#     return redirect("index_admin")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updatedata(request, id):
    username = request.POST['username'].strip()
    email = request.POST['email'].strip()

    mem = User.objects.get(id=id)

    if not username:
        messages.error(request, 'Username is required.')
        return redirect('update',id)

    if not email:
        messages.error(request, 'Email address is required.')
        return redirect('update',id)

    if username and username != mem.username:
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username already exists.')
            return redirect('update', id)
        mem.username = username

    if email and email != mem.email:
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email address already exists.')
            return redirect('update', id)
        mem.email = email

    mem.save()
    return redirect("index_admin")


def delete(request,id):
    # mem=Member.objects.get(id=id)
    mem=User.objects.get(id=id)
    mem.delete()
    return redirect("index_admin")


def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            detail= User.objects.filter(username=query)
            return render(request, 'search.html',{'details':detail})
        else:
            return render(request,'search.html',{})
         
