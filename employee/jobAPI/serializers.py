from rest_framework import serializers
from employee.models import Job, ProgrammingLanguage
from employee.auth.serializers import UserSerializer

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    programming_language = ProgrammingLanguageSerializer(many=True,read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        