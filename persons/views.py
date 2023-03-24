from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import PersonCreationForm
from django.contrib import messages
from .models import Student, Department
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
import mimetypes
from django.db.models import Q
from persons.filters import ProjectFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse
# Import render module
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail, mail_admins,EmailMessage
from django.conf import settings
# from django_mail_admin import mail, models

def home(request):
    return render(request,'persons/login.html')
def add(request):
    if request.user.is_superuser:
        form = PersonCreationForm()
        if request.method == 'POST':
            form = PersonCreationForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                nd = form.cleaned_data['level']
                name = form.cleaned_data['name']
                print("this is nd",nd)
                if Student.objects.filter(Q(title=title) and Q(level=nd) and Q(name=name)).exists():

                    messages.error(request,'this project has been uploaded previously, search to get project details')
                  
                    return redirect('projects')
                else:
                    form.save()
                    messages.success(request,'item added successfully')
                return redirect('add')
            else:
                form = PersonCreationForm(request.POST, request.FILES)
                messages.error(request, 'check the data format')
                return redirect('add')
        return render(request, 'persons/home.html', {'form': form})
    else:
        messages.error(request,'you aint authorized ')
        return HttpResponse("You are not Authorized")



def update(request, id):
    student = get_object_or_404(Student, id=id)
    form = PersonCreationForm(instance=student)
    if request.method == 'POST':
        form = PersonCreationForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'persons/home.html', {'form': form})


def projects(request):
    if request.user.is_superuser:
       
        student = Student.objects.all()
        myfilter = ProjectFilter(request.GET, queryset=student)
        
        
        page = request.GET.get('page', 1)

        paginator = Paginator(myfilter.qs, 2)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            
        context = {'myfilter':myfilter,'page_obj':page_obj,'student':student}
        return render(request,'persons/project.html',context)
        # return render(request,'persons/project.html',context)
    else:
        messages.error(request,'you aint authorized ')
        return redirect("signup")


def student_projects(request):
    if request.user.is_authenticated:
        student = Student.objects.all().order_by('id')
        myfilter = ProjectFilter(request.GET, queryset=student)
        
        
        page = request.GET.get('page', 1)

        paginator = Paginator(myfilter.qs, 2)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            
        context = {'myfilter':myfilter,'page_obj':page_obj,'student':student}
        return render(request,'persons/projects.html',context)
    else:
        messages.error(request,'you aint authorized ')
        return redirect("signup")



def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('home')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('home')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user = authenticate(username = username,password = password)
                auth.login(request, user)
            return redirect('student_projects')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('home')
        
    else:
        return render(request, 'persons/login.html')


def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                
                # to redirect admin to django admin page

                # return HttpResponseRedirect('/admin/')
                return redirect('projects')
            else:
                auth.login(request, user)
                return redirect('student_projects')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'persons/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'you have successfully log out')
    return redirect('home')

def delete(request,id):
    dele = Student.objects.get(id=id)
    dele.delete()
    messages.success(request,'item deleted successfully')
    return redirect('projects')

# def download_file(request, filename=''):
#     if filename != '':
#         # Define Django project base directory
#         BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         # Define the full file path
#         filepath = BASE_DIR + '/filedownload/Files/' + filename
#         # Open the file for reading content
#         path = open(filepath, 'rb')
#         # Set the mime type
#         mime_type, _ = mimetypes.guess_type(filepath)
#         # Set the return value of the HttpResponse
#         response = HttpResponse(path, content_type=mime_type)
#         # Set the HTTP header for sending to browser
#         response['Content-Disposition'] = "attachment; filename=%s" % filename
#         # Return the response value
#         return response
#     else:
#         # Load the template
#         return render(request, 'file.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('signup')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'persons/change_password.html', {
        'form': form
    })


def password_reset_request(request):
    
    if request.method == "POST":

        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    # subject = "Password Reset Requested"
                    email_template_name = "persons/password_reset_email.txt"
                    
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    email_from = 'princegeestar@gmai.com'
                    
                    try:
                        mail.send(
                            'princegeestar@gmail.com',
                            [user.email],
                            subject='Hello',
                    
            
                        
                        )
                        # mail_admins(subject,email,fail_silently=False, connection=None, html_message=None)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="persons/password_reset_form.html", context={"password_reset_form":password_reset_form})

def email(request): 
    # if request.method =="GET":
    e = request.GET.get('email')   
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = 'gfgabrielfalade@gmail.com'
    recipient_list = ['e',]    
    send_mail=( subject, message, email_from, recipient_list ) 
    # send_mail.send(fail_silently=False)   
    # return redirect('email')
    return render(request,'persons/email.html')

# AJAX
def load_cities(request):
    faculty_id = request.GET.get('faculty_id')
    cities = Department.objects.filter(faculty_id=faculty_id).all()
    return render(request, 'persons/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

