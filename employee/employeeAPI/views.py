from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from employee.models import  Employee, ProgrammingLanguage
from .serializers import EmployeeSerializer, ProgrammingLanguageSerializer


################# show all employees ##############

@api_view(["Get",])
def get_emps(request):
    employees = Employee.objects.all()
    serialzier = EmployeeSerializer(instance=employees,many=True)
    return Response(data=serialzier.data, status=status.HTTP_200_OK)

################# show one employee profile##############

@api_view(["Get",])
def get_emp(request,pk):
    employee = Employee.objects.filter(pk = pk)
    if (not(request.user.id) or request.user.id != pk ):
        emp_views = Employee.objects.get(pk = pk).views
        emp_views += 1
        employee.update(views=emp_views)
    serialzier = EmployeeSerializer(instance=employee,many=True)
    return Response(data=serialzier.data, status=status.HTTP_200_OK)

################# create employee profile ##############

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_emp_profile(request):
    request.data._mutable = True
    request.data.update({"user": request.user.id})
    # ProgrammingLanguages.objects.create(name='', isActive=False)
    print(request.data)
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "success":True,
            "message":"Employee Profile has been created successfuly"
        },status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    },status=status.HTTP_400_BAD_REQUEST)

################# edit employee profile ##############

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_emp_profile(request):
    employee=Employee.objects.get(user = request.user.id)
    request.data._mutable = True
    request.data.update({"user": request.user.id})
    print(request.data)
    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


################# show all programming languages ##############

@api_view(["Get",])
def get_program_langs(request):
    program_langs = ProgrammingLanguage.objects.all()
    serialzier = ProgrammingLanguageSerializer(instance=program_langs,many=True)
    return Response(data=serialzier.data, status=status.HTTP_200_OK)
