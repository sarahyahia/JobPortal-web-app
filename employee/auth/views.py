from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.decorators import api_view 
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from employee.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string,get_template
from django.utils.encoding import force_bytes, force_str, force_text
from .utils import generate_token
# from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode



################### send activation mail ######################
def send_activation_email(user, request):
    current_site = get_current_site(request)
    ######################### send mail with email template ####################################
    htmly = get_template('user/Email.html')
    context = {
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': generate_token.make_token(user)
    }
    subject, from_email,to = 'Activate your account', settings.EMAIL_HOST_USER, user.email
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    ######################### send mail with string plain text ####################################
    # email_subject = 'Activate your account'
    # email_body = render_to_string('user/Email.html',{
    #     'user':user,
    #     'domain':current_site,
    #     'uid': urlsafe_base64_encode(force_bytes(user.id)),
    #     'token': generate_token.make_token(user)
    # })
    
    # email = EmailMessage(subject=email_subject,body=email_body,
    #                     from_email=settings.EMAIL_HOST_USER,
    #                     to=[user.email]
    #                     )
    # email.send()



############## registration #####################################
@api_view(['POST'])
def signup_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            token = Token.objects.create(user=user)
            user_data = User.objects.get(email = request.POST['email'] )
            send_activation_email(user_data,request)
        except Exception as e:
            return Response(data={
                    "success":False,
                    "errors":str(e)
            },status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
            "success":True,
            # "token":user.auth_token.key,
            "message":"User has been created successfully",
            # "user":{
            #     'id': user_data.id,
            #     'isEmployer': user_data.isEmployer,
            #     'first_name': user_data.first_name,
            #     'last_name': user_data.last_name,
            #     'email':user_data.email,
            # }
        },status=status.HTTP_201_CREATED)
    return Response(data={
            "success":False,
            "passsword":serializer.errors
    },status=status.HTTP_400_BAD_REQUEST)


###### login ####################################

@api_view(['POST'])
def login_view(request):
    user = authenticate(email=request.POST['email'], password=request.POST['password'])
    user_data = User.objects.get(email = request.POST['email'] )
    
    if not user.is_email_verified:
        return Response("Email is not verified, please check your email inbox", status=401)
    if user and user.is_email_verified:
        login(request, user)
        return Response(data={
            "success":True,
            "token":user.auth_token.key,
            "user":{
                'id': user_data.id,
                'isEmployer': user_data.isEmployer,
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'email':user_data.email,
            }
        },status=status.HTTP_200_OK)
    else:
        return Response("Unauthorized", status=401)


###### logout the current authenticated user
class Logout(APIView):
    def get(self, request, format=None):
        #delete the token to force a login
        request.user.auth_token.delete() 
        
        return Response(data={
            'success': True,
            'message': 'logged out successfully'
        }, status=status.HTTP_200_OK)

############# activate the user ###############################
@api_view(['GET'])
def activate_user (request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user,token):
        user.is_email_verified = True
        user.save()
        return Response(data={
            'success': True,
            'message': 'activated successfully'
        }, status=status.HTTP_200_OK)
    return Response(data={
        'message': 'activation failed, try to resend the email'
    }, status=status.HTTP_400_BAD_REQUEST)