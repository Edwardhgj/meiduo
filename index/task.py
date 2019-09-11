# from django.core.mail import EmailMessage
# from celery import task
# from day01 import settings
#
#
#
# @task
# def sendmail(email,token ):
#     mes='欢迎注册', '点击此链接<a href="http://localhost:8000/valid_email?code=' + token + '">验证</a>'
#     esend = EmailMessage('欢迎注册',mes,settings.DEFAULT_FROM_EMAIL,[email])
#     esend.content_subtype = 'html'
#     esend.send()



