
# Create your views here.
from django.shortcuts import render
from .models import Event, Registration
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

#event_list
def event_list(request):

    events = Event.objects.annotate(
        registered_count=Count('registration')
    )

    for event in events:
        event.available_seats = max(
            event.capacity - event.registered_count, 0
        )

    return render(request, 'events/event_list.html', {
        'events': events
    })

#student signup
def student_signup(request):

    if request.method == 'POST':

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password'])

            user.save()

            login(request, user)

            return redirect('event_list')

    else:
        form = StudentRegistrationForm()

    return render(request, 'events/signup.html', {'form': form})

#student login
def student_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('event_list')

        else:
            return render(request, 'events/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'events/login.html')

#logout
def student_logout(request):

    logout(request)

    return redirect('event_list')


@login_required
def register_event(request, event_id):

    if request.method == 'POST':

        event = Event.objects.get(id=event_id)

        # Check if student is already registered
        already_registered = Registration.objects.filter(
            student=request.user,
            event=event
        ).exists()

        if already_registered:
            messages.info(
                request,
                'You are already registered for this event.'
            )

        else:
            # Count total registrations
            total_registrations = Registration.objects.filter(
                event=event
            ).count()

            # Check event capacity
            if total_registrations >= event.capacity:
                messages.error(
                    request,
                    'Sorry, this event is full!'
                )

            else:
                Registration.objects.create(
                    student=request.user,
                    event=event
                )

                messages.success(
                    request,
                    'Successfully registered for the event!'
                )

    return redirect('event_list')


@login_required
def my_registrations(request):

    registrations = Registration.objects.filter(
        student=request.user
    )

    return render(
        request,
        'events/my_registrations.html',
        {'registrations': registrations}
    )