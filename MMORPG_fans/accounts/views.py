import random

from django.contrib.auth.models import User
from django.core.mail import send_mail, mail_managers, mail_admins
from django.shortcuts import render, redirect

from .forms import SignUpForm, ConfirmationForm
from .models import Code


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=request.POST['email'],
                username=request.POST['username'],
                password=request.POST['password1'],
                is_active=False
            )
            #генерируем код проверки
            generated_code = Code.objects.create(
                name=User.objects.get(id=user.id),
                code=random.randint(1000, 9999)
            )
            print(generated_code.code)
            # отправляем его по почте, указанной пользователем
            send_mail(subject='Confirm your registration.',
                      message=f'Proceed with this confirmation code {generated_code.code} .',
                      from_email=None,
                      recipient_list=[request.POST['email']])
            context = {
                'generated_code': generated_code,
                'user': user
            }
            return render(request, 'registration/confirm.html', context)
        else:
            return render(request, 'registration/reset.html')
    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


def confirm(request, code_id):
    # страница для проверки кода
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            user = request.POST['name']
            user_code = request.POST['code']
            confirmation = Code.objects.get(id=code_id)
            # проверка кода
            if int(user_code) == int(confirmation.code):
                user_upd = User.objects.get(username=confirmation.name)
                user_upd.is_active = True
                # если код совпадает, сохраянем пользователя и отправляем уведомления менеджерам и админу
                user_upd.save()

                mail_managers(
                    subject='New user!',
                    message=f'Hello, manager! New user {user} is registered.'
                )

                mail_admins(
                    subject='News user!',
                    message=f'Hello, admin! New user {user} is registered.'
                )

                return render(request, 'registration/successful.html', {'user': user})
            return render(request, 'registration/unsuccessful.html')
        return render(request, 'registration/unsuccessful.html')
    else:
        form = ConfirmationForm()
        return render(request, 'registration/confirm.html', {'form': form})


def reset(request):
    obj = User.objects.filter(is_active=False)
    obj.delete()
    return redirect('signup')



