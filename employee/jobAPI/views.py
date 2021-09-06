from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from employee.models import  Job, JobApplicant
from .serializers import JobSerializer, JobApplicantSerializer
from rest_framework.filters import SearchFilter
from django.db import IntegrityError


################# show all jobs ##############

@api_view(["Get",])
# @permission_classes([IsAuthenticated,]) #IsManager
def get_jobs(request):
    jobs = Job.objects.all()
    serialzier = JobSerializer(instance=jobs,many=True)
    return Response(data=serialzier.data, status=status.HTTP_200_OK)


################# show one job ##############

@api_view(["Get",])
def get_job(request, pk):
    job = Job.objects.filter(pk =pk)
    print(job)
    serialzier = JobSerializer(instance=job, many=True)
    return Response(data=serialzier.data, status=status.HTTP_200_OK)


################# create a job ##############


@api_view(["POST",])
@permission_classes([IsAuthenticated])
def create_job(request):
    request.data._mutable = True
    request.data.update({"user": request.user.id})
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "success":True,
            "message":"Job has been created successfuly"
        },status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    },status=status.HTTP_400_BAD_REQUEST)


################# delete a job ##############

@api_view(["DELETE",])
@permission_classes([IsAuthenticated])
def delete_job(request, pk):
    job = Job.objects.get(pk =pk).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


################# get all applicants ##############

@api_view(["Get",])
# @permission_classes([IsAuthenticated,])
def get_applicants(request, job_id):
    applicants = JobApplicant.objects.filter(job_id = job_id)
    print(applicants)
    serialzier = JobApplicantSerializer(instance=applicants,many=True)
    return Response(data=serialzier.data, status=status.HTTP_200_OK)

################# edit applicant status ##############

@api_view(['PUT'])
def edit_applicant_status(request,job_id):
    applicant = JobApplicant.objects.get(job_id = job_id)
    request.data._mutable = True
    request.data.update({"applicant": request.user.id})
    serializer = JobApplicantSerializer(applicant, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#################  apply for this job ##############

@api_view(["POST",])
@permission_classes([IsAuthenticated])
def apply_job(request):
    request.data._mutable = True
    request.data.update({"applicant_id": f"{request.user.id}", 'applicant_status': f"{0}"})
    reqData = request.data
    print(reqData)
    serializer = JobApplicantSerializer(data=reqData)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "success":True,
            "message":"you applied successfuly"
        },status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    },status=status.HTTP_400_BAD_REQUEST)


################# search all jobs ##############

class JobList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('job_title', '@description', 'programming_language__name', 'city', 'job_status', 'experience_level',)
