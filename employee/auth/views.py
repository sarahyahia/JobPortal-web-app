from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.decorators import api_view 
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def api_signup(request):
    serializer = UserSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            token = Token.objects.create(user=user)
        except Exception as e:
            return Response(data={
                    "success":False,
                    "errors":str(e)
            },status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
            "success":True,
            "token":user.auth_token.key,
            "message":"User has been created successfully"
        },status=status.HTTP_201_CREATED)
    return Response(data={
            "success":False,
            "passsword":serializer.errors
    },status=status.HTTP_400_BAD_REQUEST)

###### logout the current authenticated user
class Logout(APIView):
    def get(self, request, format=None):
        #delete the token to force a login
        request.user.auth_token.delete() 
        
        return Response(data={
            'success': True,
            'message': 'logged out successfully'
        }, status=status.HTTP_200_OK)


      
