from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.decorators import api_view 
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from employee.models import User



@api_view(['POST'])
def signup_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            token = Token.objects.create(user=user)
            user_data = User.objects.get(email = request.POST['email'] )
        except Exception as e:
            return Response(data={
                    "success":False,
                    "errors":str(e)
            },status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
            "success":True,
            "token":user.auth_token.key,
            "message":"User has been created successfully",
            "user":{
                'id': user_data.id,
                'isEmployer': user_data.isEmployer,
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'email':user_data.email,
            }
        },status=status.HTTP_201_CREATED)
    return Response(data={
            "success":False,
            "passsword":serializer.errors
    },status=status.HTTP_400_BAD_REQUEST)


###### login 

@api_view(['POST'])
def login_view(request):
    user = authenticate(email=request.POST['email'], password=request.POST['password'])
    user_data = User.objects.get(email = request.POST['email'] )
    if user:
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

