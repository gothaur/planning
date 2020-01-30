from django.shortcuts import (
    render,
    redirect,
)
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.forms import UserCreationForm
from django.views import View


class Login(View):

    def get(self, request, redirected=0):
        logout(request)
        context = {
            'redirected': redirected
        }
        return render(request, 'registration/login.html', context)

    def post(self, request, redirected=0):

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            # if user.is_active():
            login(request, user)
            request.session['username'] = username
            return redirect('dashboard')

        return redirect('login', 0)


class Register(View):

    def get(self, request):
        form = UserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'register.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context = {
                'form': form,
            }
            return render(request, 'register.html', context)


class Logout(View):

    def get(self, request):
        try:
            del request.session['username']
        except KeyError:
            pass
        logout(request)
        return render(request, 'registration/logout.html')
