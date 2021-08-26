from rest_framework import serializers
from employee.models import Employee, ProgrammingLanguage
from employee.auth.serializers import UserSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    # name = serializers.CharField()
    class Meta:
        model = ProgrammingLanguage
        fields = ['name',]

class EmployeeSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    programming_language = ProgrammingLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
    # def create(self, validated_data):
    #     progLang =validated_data.pop('programming_language')
    #     print(progLang)
    #     emp = Employee.objects.create(**validated_data)
    #     print(emp)
    #     for x in progLang:
    #         ProgrammingLanguage.objects.create(**x)
    #     # EmpLang.objects.create(ProgrammingLanguage=progLang, Employee=instance)
    #     return emp

