from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):  # АВТОРИЗАЦИЯ
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):  # ЛОГИКА РЕГИСТРАЦИИ
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались'
    title = 'Store - Регистрация'

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        return context


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):  # ЛОГИКА ОБНОВЛЕНИЯ ИНФОРМАЦИИ ПОЛЬЗОВАТЕЛЯ
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Store - Личный Кабинет'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['baskets'] = Basket.objects.filter(user=self.object) # можно self.request.user
    #     return context

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:email-verify'))

# def login(request):    #АВТОРИЗАЦИЯ
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


# def registration(request):  #ЛОГИКА РЕГИСТРАЦИИ
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегестрировались')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


# @login_required
# def profile(request):  #ЛОГИКА ОБНОВЛЕНИЯ ИНФОРМАЦИИ ПОЛЬЗОВАТЕЛЯ
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     baskets = Basket.objects.filter(user=request.user)

# total_sum = sum(basket.sum() for basket in baskets)
# total_quantity = sum(basket.quantity for basket in baskets)

# total_sum = 0
# total_quantity = 0
# for basket in baskets:
#     total_sum += basket.sum()
#     total_quantity += basket.quantity

# contex = {
#     'title': 'Store - Профиль',
#     'form': form,
#     'baskets': Basket.objects.filter(user=request.user),
#     # 'total_sum': sum(basket.sum() for basket in baskets),
#     # 'total_quantity': sum(basket.quantity for basket in baskets),
# }
# return render(request, 'users/profile.html', contex)

# def logout(request):    #ВЫХОД ИЗ СИСТЕМЫ(АККАУНТА)
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
#
