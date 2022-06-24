from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form with default Django registration form
        form = UserCreationForm()
    else:
        # Process completed form, use data given to register a new user
        form = UserCreationForm(data=request.POST)
    
        # If everything was filled in properly save new user and log them in
        if form.is_valid():
            # Save user to database (automatically hashes password)
            new_user = form.save()
            # Log user in and then redirect them to home page by calling login fucntion w/ their info
            login(request, new_user)
            return redirect('blogs:index')
    
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)