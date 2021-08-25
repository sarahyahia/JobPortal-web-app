from rest_framework import serializers
from employee.models import Employee, ProgrammingLanguage
from employee.auth.serializers import UserSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = ProgrammingLanguage
        fields = ['name',]

class EmployeeSerializer(WritableNestedModelSerializer):
    # user = UserSerializer(read_only=True)
    programming_language = ProgrammingLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


