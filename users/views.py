from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# TEST USER CREATION
def user_register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        user = form.save(commit=False)
        print("New user username:", user)
    context = {'form': form}
    return render(request, 'users/register.html', context=context)
