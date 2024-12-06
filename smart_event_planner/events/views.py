from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, EventForm
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import  User, UserProfile
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, CommentForm
from events.models import Event, Category

def index(request):
    return render(request, 'event_planner/index.html', {'user': request.user})

def event_list_by_category(request, category, sub_category):
    
    events = Event.objects.filter(category=category, sub_category=sub_category)
    return render(request, 'event_planner/category_events.html', {'events': events,'category': category})

def category_events(request, category_id):
    category = Category.objects.get(id=category_id)  
    events = Event.objects.filter(category=category)  
    return render(request, 'event_planner/category_events.html', {'events': events, 'category': category})

def user_logout(request):
    logout(request)
    return redirect('index')

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user  
            event.owner = request.user  
            event.category = form.cleaned_data['sub_category'] if form.cleaned_data['sub_category'] else form.cleaned_data['category']
            event.save()
            user = request.user
            user.score += 15  
            user.save()  
            return redirect('event_list')  
    else:
        form = EventForm()

    return render(request, 'event_planner/event_create.html', {'form': form})



def event_list(request):
    if request.method == 'POST':
        events = Event.objects.filter(user=request.user)  
        return render(request, 'event_planner/event_list.html', {'events': events})
    else:
        
        events = Event.objects.filter(user=request.user)   
        return render(request, 'event_planner/event_list.html', {'events': events})
    
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    participants = event.participants.all()
    comments = event.comments.all().order_by('-created_at')
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  
            comment.event = event  
            comment.save()
            return redirect('event_detail', id=event.id)
    else:
        form = CommentForm()

    return render(request, 'event_planner/event_detail.html', {
        'event': event,
        'participants': participants,
        'comments': comments,  
        'form': form,  
        'is_upcoming': event.is_upcoming(),
        
        
        
    })
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=username, password=password)
        if user is not None:
            
            login(request, user)
            return redirect('user_profile', username=user.username)
        else:
            
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre')
            return render(request, 'event_planner/login.html')

    return render(request, 'event_planner/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()  
            messages.success(request, "Kayıt başarılı! Giriş yapabilirsiniz.")
            return redirect('login')
        else:
            messages.error(request, "Formda hata var. Lütfen tekrar deneyin.")
    else:
        form = UserRegistrationForm()

    return render(request, 'event_planner/register.html', {'form': form})



def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username, email=email)
            if user.is_active:  
                user.password = make_password(new_password)  
                user.save()
                messages.success(request, 'Şifreniz başarıyla güncellendi. Yeni şifrenizle giriş yapabilirsiniz.')
                return redirect('login')
            else:
                messages.error(request, 'Hesabınız aktif değil. Lütfen destek ile iletişime geçin.')
        except User.DoesNotExist:
            messages.error(request, 'Kullanıcı adı veya email eşleşmiyor.')
    return render(request, 'event_planner/password_reset.html')

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile  
    except UserProfile.DoesNotExist:
        messages.error(request, "Bu kullanıcı için profil oluşturulmamış.")
        return redirect('profile_update', username=username)  

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'event_planner/profile.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'event_planner/user_profile.html', {'user': user})



def profile_update(request, username):
    
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profiliniz başarıyla güncellenmiştir.')
            return redirect('user_profile', username=user.username)   
        else:
            messages.error(request, 'Formda hata oluştu.')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'event_planner/profile_update.html', {'form': form, 'user': user})

def join_event(request, id):
    user = request.user
    event = get_object_or_404(Event, id=id)

    if not event.participants.filter(id=user.id).exists():
        
        event.participants.add(user)       
        user.participated_events_count += 1
        participation_points = 10  
        bonus_points = 20 if not user.first_participation else 0 
        user.score += participation_points + bonus_points
        if not user.first_participation:
            user.first_participation = True

        user.save()  

    return redirect('event_detail', id=event.id)
