from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from employee.models import  Job
from .serializers import JobSerializer

@api_view(["Get",])
# @permission_classes([IsAuthenticated,]) #IsManager
def index(request):
    jobs = Job.objects.all()
    print(jobs)
    serialzier = JobSerializer(instance=jobs,many=True)
    return Response(data=serialzier.data, status=status.HTTP_200_OK)


@api_view(["POST",])
# @permission_classes([IsAuthenticated,IsAdminUser])
def create(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "success":True,
            "message":"Movie has been created successfuly"
        },status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    },status=status.HTTP_400_BAD_REQUEST)
