from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from .models import Skill
from .models import City
from .models import Location
from .models import Job_applications

# Create your views here.
def home(request):
    home_skill=Skill.objects.all()
    home_city=City.objects.all()
    return render(request,'home.html',{'home_skill':home_skill,'city':home_city})

def about(request):
    return render(request,'about.html')

def category(request):
    return render(request,'category.html')

def contact(request):
    return render(request,'contact.html')

def job_detail(request,id):
    if not request.user.is_authenticated:
       return redirect('/login')
    else:         
        update_jobdetail=Skill.objects.get(id=id)
        job_applications=Job_applications.objects.filter(job_id=id)
        return render(request,'job-detail.html',{'update_jobdetail':update_jobdetail,'job_applications':job_applications})

def jobs(request):
    view_skill=Skill.objects.all()
    city_data=City.objects.all()

    return render(request,'job-list.html',{'view_skill':view_skill,'city':city_data})

def loginform(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def register_form(request):

    username=request.POST.get("name")
    email=request.POST.get("email")
    phone_number=request.POST.get("phone_number")
    password=request.POST.get("password")
    confirm_password=request.POST.get("confirm_password")

    if not username:
        messages.warning(request,"Please Enter Username")
        return redirect('register')
    elif not email:
        messages.warning(request,"Please Enter Email")
        return redirect('register')
    elif not phone_number:
        messages.warning(request,"Please Enter Phone Number")
        return redirect('register')
    elif password!=confirm_password:
        messages.warning(request,"Password Doesn't match")
        return redirect('register')


    my_user=User.objects.create_user(username,email,password)
    my_user.save()
    messages.success(request,"Successfully Registered Please Login")
    return redirect('login')

@login_required
def login_required_view():
    return redirect('login')
  
@never_cache
def login_user(request):

    if request.method == 'POST':
        uname=request.POST.get("username")
        pass1=request.POST.get("password")

        if not uname:
            messages.error(request,"Please Enter uname")
            return redirect('login')
        elif not pass1:
            messages.error(request,"Please Enter Password")
            return redirect('login')
        
        user=authenticate(request,username=uname,password=pass1)
        if user is not None:
            login(request,user)
            request.session['user_id'] = user.id
            # messages.success(request,'Logged in success')
            return redirect('/')
        else:
            messages.error(request,'Invalid Username or password')
            return redirect('login')
        
    return render(request, 'register')

def handle_logout(request):
    logout(request)
    # messages.info(request,"LoggedOut Succesfully")
    return redirect('/')

def skill_view(request):
    return render(request,'skill.html')

def add_skill(request):
   if request.method == 'POST':
        
        user_id = request.session.get('user_id')
        state=request.POST.get("state")
        city=request.POST.get("city")
        job_type=request.POST.get("job_type")
        job=request.POST.get("job")
        job_desc=request.POST.get("job_desc")
        salary=request.POST.get("salary")
        vacancy=request.POST.get("vacancy")
        contact=request.POST.get("contact")

        if not state:
            messages.warning(request,"Please Enter State")
            return redirect('skill')
        elif not city:
            messages.warning(request,"Please Enter City")
            return redirect('skill')
        elif not job_type:
            messages.warning(request,"Please Select Job type")
            return redirect('skill')
        elif not job:
            messages.warning(request,"Please Select Job")
            return redirect('skill')
        elif not job_desc:
            messages.warning(request,"Please Enter Job Description")
            return redirect('skill')
        elif not salary:
            messages.warning(request,"Please Enter Salary")
            return redirect('skill')

        current_date = datetime.now()
        
        insert_skill=Skill(user_id=user_id,state=state,city=city,job_type=job_type,job=job,job_desc=job_desc,salary=salary,date_posted=current_date,vacancy=vacancy,contact=contact)
        insert_skill.save()
        messages.success(request,"Successfully Added Your Skill")
        return redirect('/')
   
def profile_settings(request):
    user_id = request.session.get('user_id')
    view_user=User.objects.get(id=user_id)
    return render(request,'profile_settings.html',{'view_user':view_user})


def update_profile(request):
        user_id = request.POST.get('id')
        name=request.POST.get("name")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        profile_picture = request.FILES['pic']

        if not name:
            messages.warning(request,"Please Enter Name")
            return redirect('skill')
        elif not first_name:
            messages.warning(request,"Please Enter First Name")
            return redirect('skill')
        elif not last_name:
            messages.warning(request,"Please Select Last Name")
            return redirect('skill')
        elif not email:
            messages.warning(request,"Please Select Email")
            return redirect('skill')
        
        User.objects.filter(id=user_id).update(username=name,first_name=first_name,last_name=last_name,email=email,profile_image=profile_picture)
        # update_profile.save()
        messages.success(request,"Successfully Updated Your Profile")
        return redirect('/')

def get_locations(request):

    location_id=request.POST.get('location_id')
    all_locations=Location.objects.filter(city_id_id=location_id)
     # Convert the queryset to a list of dictionaries
    locations_data = [{'id': location.id, 'location_name': location.location_name} for location in all_locations]
    
    return JsonResponse(locations_data, safe=False)  # Return the data as JSON response


def get_applications(request):
    user_id = request.session.get('user_id')
    view_application=Job_applications.objects.filter(user_id=user_id)
    return render(request,'view_applications.html',{'view_application':view_application})

def job_applications(request):

    user_id = request.POST.get('user_id')
    job_id = request.POST.get('job_id')
    name=request.POST.get('name')
    contact=request.POST.get('contact')
    email=request.POST.get('email')
    description=request.POST.get('description')

    insert_application=Job_applications(user_id=user_id,job_id=job_id,name=name,contact=contact,email=email,description=description)
    insert_application.save()
    messages.success(request,"Successfully Applied")
    return redirect('/job-detail')

