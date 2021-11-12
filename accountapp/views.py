from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.core.mail import EmailMessage
from django.core.mail.message import EmailMessage
from accountapp.decorators import account_ownership_required
from accountapp.forms import UserForm, AccountUpdateForm
from accountapp.tokens import account_activation_token

has_ownership = [account_ownership_required, login_required]

class SignupView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/signup.html'

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] ==request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.is_active = False #유저 비활성화
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('accountapp/activation_email.html',
                                       {'user': user, 'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user),})
            mail_title = "회원가입 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            return render(request, 'accountapp/login.html')
    # 포스트 방식 아니면 페이지 띄우기
    return render(request, 'accountapp/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # 로그인
        user = auth.authenticate(request, username=username, password=password)
        if user is not None: #성공
            auth.login(request, user)
            return render(request, 'accountapp/detail.html')
        else: #실패
            return render(request, 'accountapp/login.html', {'error':'아이디 또는 비밀번호를 다시 입력해주세요.'})
    else:
        return render(request, 'accountapp/login.html')

def logout(request):
    #if request.method == 'POST':
        auth.logout(request) #유저 로그아웃
        return render(request, 'accountapp/login.html')

def activate(request, uidb64, token, account_activation_token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return render(request, 'accountapp/detail.html')
    else:
        return render(request, 'accountapp/login.html', {'error':'계정 활성화 오류'})


class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'
    pagination_by = 8
    #def get_context_data(self, **kwargs):
     #   object_list = Article.objects.filter(writer=self.get_object())
      #  return super(AccountDetailView, self).get_context_data(object_list=object_list, **kwargs)

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accountapp:detail')
    template_name = 'accountapp/update.html'

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'