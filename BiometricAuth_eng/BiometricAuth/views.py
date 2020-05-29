from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, IrisAuth

from .authenticate import (
    IrisAuthBackend,

)
from .models import (
    UserBiometry,
    IrisImages,
    FaceImages,
    FingerPrintImages
)

class SignUp(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "BiometricAuth/signup.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def custom_logout(request):
    print('Loggin out {}'.format(request.user))
    logout(request)
    return HttpResponseRedirect('/')

 
class LogIn(View):
    html_template = 'BiometricAuth/login.html'

    def get(self, request):
        form = UserLoginForm()
        context = {
            'form' : form
        }
        return render(request, self.html_template, context=context)
   
    def post(self, request):
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user_pk = User.objects.get(username=username).pk
            except User.DoesNotExist:
                raise Http404()
            request.session['username'] = username
            request.session['password'] = password
            request.session['user_pk'] = user_pk
            return redirect('two-factor-auth')
        else:
            context = {
                'form' : form
            }
            return render(request, self.html_template, context=context)

class TwoFactorAuth(View):
    next_page = '/'

    def get(self, request):
        auth_forms = {
            'iris': IrisAuth(),
        }
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        user_pk = request.session.get('user_pk', None)
        if not username or not password or not user_pk:
            raise Http404()
        try:
            user_biometry = UserBiometry.objects.get(user__pk=user_pk)
        except UserBiometry.DoesNotExist:
            raise Http404()
        context = {
            'user_biometry':user_biometry,
            'auth_forms':auth_forms,
        }
        return render(request,'BiometricAuth/two_factor_auth.html', context=context)


    def post(self, request):
        auth_forms = {
            'iris': IrisAuth(),
        }
        form_type = request.POST.get('auth_type').strip()
        print('Form type={}'.format(form_type))
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        user_pk = request.session.get('user_pk', None)
        if not username or not password or not user_pk:
            raise Http404()
        try:
            user_biometry = UserBiometry.objects.get(user__pk=user_pk)
        except UserBiometry.DoesNotExist:
            raise Http404()

        if form_type == 'iris':
            form = IrisAuth(request.POST or None, request.FILES or None)
            if form.is_valid():
                iris_image = form.cleaned_data.get('iris_image')
                iris_auth = IrisAuthBackend()
                user = iris_auth.authenticate(username=username, password=password, uploaded_iris=iris_image)
                if user is not None:
                    login(request, user)
                    if self.next_page:
                        return redirect(self.next_page)
                    return redirect('/')
                else:
                    form.add_error(None, "УПС! Совпадений не найдено...")
                    auth_forms['iris'] = form
            else:
                auth_forms['iris'] = form
                
        elif form_type == 'fingerprint':
            pass
        
        elif form_type == 'face':
            pass

        context = {
            'user_biometry': user_biometry,
            'auth_forms': auth_forms,
        }
        return render(request,'BiometricAuth/two_factor_auth.html', context=context)


