from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .models import Room, Topic, Message, User, Property
from .forms import RoomForm, UserForm, MyUserCreationForm, PropertyForm, PropertySearchForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Please provide both email and password')
            return render(request, 'base/login_register.html', {'page': page})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist')
            return render(request, 'base/login_register.html', {'page': page})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower() if user.email else ''
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Keja!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    # Property search functionality
    form = PropertySearchForm(request.GET)
    properties = Property.objects.filter(is_available=True).order_by('-created')
    
    if form.is_valid():
        location = form.cleaned_data.get('location')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        property_type = form.cleaned_data.get('property_type')
        bedrooms = form.cleaned_data.get('bedrooms')
        
        if location:
            properties = properties.filter(
                Q(location__icontains=location) | Q(address__icontains=location)
            )
        if min_price:
            properties = properties.filter(rent_amount__gte=min_price)
        if max_price:
            properties = properties.filter(rent_amount__lte=max_price)
        if property_type:
            properties = properties.filter(property_type=property_type)
        if bedrooms:
            properties = properties.filter(bedrooms__gte=bedrooms)
    
    # Pagination
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)
    
    # Get some stats
    total_properties = Property.objects.filter(is_available=True).count()
    property_types = Property.objects.values_list('property_type', flat=True).distinct()
    
    context = {
        'properties': properties,
        'form': form,
        'total_properties': total_properties,
        'property_types': property_types,
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


# Property Views
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk, is_available=True)
    related_properties = Property.objects.filter(
        location__icontains=property.location,
        is_available=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'property': property,
        'related_properties': related_properties,
    }
    return render(request, 'base/property_detail.html', context)


@login_required(login_url='login')
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.landlord = request.user
            property.save()
            messages.success(request, 'Property added successfully!')
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'base/add_property.html', {'form': form})


@login_required(login_url='login')
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, landlord=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm(instance=property)
    
    return render(request, 'base/edit_property.html', {'form': form, 'property': property})


@login_required(login_url='login')
def my_properties(request):
    properties = Property.objects.filter(landlord=request.user).order_by('-created')
    return render(request, 'base/my_properties.html', {'properties': properties})


@login_required(login_url='login')
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, landlord=request.user)
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('my_properties')
    
    return render(request, 'base/delete.html', {'obj': property})
