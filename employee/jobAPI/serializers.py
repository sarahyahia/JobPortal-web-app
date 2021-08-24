from employee.employeeAPI.serializers import EmployeeSerializer, ProgrammingLanguageSerializer
from rest_framework import serializers
from employee.models import Job, ProgrammingLanguage, JobApplicant
from employee.auth.serializers import UserSerializer


class JobSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    programming_language = ProgrammingLanguageSerializer(many=True,read_only=True)

    class Meta:
        model = Job
        fields = '__all__'

class JobApplicantSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    applicant = EmployeeSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = JobApplicant
        fields = '__all__'
        