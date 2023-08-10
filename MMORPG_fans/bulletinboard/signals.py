from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import *


@receiver(post_save, sender=Comment)
def comment_notify(sender, instance, **kwargs):
    comment_author = instance.comment_author.username
    comment_text = instance.comment_text
    comment_post_pk = instance.comment_post.pk
    post_author = instance.comment_post.author

    if instance.accepted:
        # если комментарий принят,
        # его автору присылается уведомление
        mail = instance.comment_post.author.email
        subject = f'Your comment has been approved by {post_author}'
        text_content2 = (
            f'Hello, {comment_author}! \n\n'
            f'Your comment "{comment_text}" is accepted by {post_author}. \n'
            f'Read: http://127.0.0.1:8000/post/{comment_post_pk}'
        )

        send_mail(
            subject=subject,
            message=text_content2,
            from_email='pyh0n@yandex.ru',
            recipient_list=[mail],
            fail_silently=False
        )
    else:
        #если комментарий уже написан, но еще не принят,
        # отправляются сразу два письма - автору поста и автору комментария
        mail = instance.comment_post.author.email
        subject = f'A comment from {comment_author} is waiting for your approval'
        text_content = (
            f'A comment to your post!'
            f' Accept or delete: http://127.0.0.1:8000/mycomments/'
        )

        mail1 = instance.comment_author.email
        subject1 = f'You comment "{comment_text}" is sent for approval'
        text_content1 = (
            f'You comment "{comment_text}" is not approved yet. '
            f'We will notify you once it is approved and published'
        )

        send_mail(
            subject=subject,
            message=text_content,
            from_email='pyh0n@yandex.ru',
            recipient_list=[mail],
            fail_silently=False
        )

        send_mail(
            subject=subject1,
            message=text_content1,
            from_email='pyh0n@yandex.ru',
            recipient_list=[mail1],
            fail_silently=False
        )


@receiver(post_save, sender=Post)
def post_notify(sender, instance, **kwargs):
    author = instance.author
    title = instance.title
    mail = instance.author.email
    post_pk = instance.pk
    subject = f'Hello {author}! Your post is published'
    text_content = (
        f'Hello, {author}! \n\n'
        f'Your post "{title}" is published or changed. \n'
        f'Read: http://127.0.0.1:8000/post/{post_pk}'
    )

    send_mail(
        subject=subject,
        message=text_content,
        from_email='pyh0n@yandex.ru',
        recipient_list=[mail],
        fail_silently=False
    )




