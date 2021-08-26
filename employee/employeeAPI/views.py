from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from employee.models import  Employee, ProgrammingLanguage
from .serializers import EmployeeSerializer, ProgrammingLanguageSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

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
    userId=request.user.id
    #request.data._mutable = True
    request.data.update({"user": userId})
    # ProgrammingLanguages.objects.create(name='', isActive=False)
    print(request.data)
    newEmployee = EmployeeSerializer(data=request.data)
    proglangs= request.data.get('programming_language')
    print(proglangs)

    if newEmployee.is_valid():
        newEmployee.save()
        for lang in proglangs:
            print(lang)
            emplang=Employee.programming_language.through(employee_id=userId, programminglanguage_id=lang)
            emplang.save()
            
        return Response(data={
            "success":True,
            "message":"Employee Profile has been created successfuly"
        },status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": newEmployee.errors
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

################# search all employees ##############

class EmployeeList(generics.ListAPIView):
    
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        #queryset = Employee.objects.all()
        filter_backends = (SearchFilter,)
        for x in self.request.GET :
            #print(x)
            #print(self.request.GET[x])
            if(x=="little_bio"):
              queryset=Employee.objects.filter(little_bio__search=self.request.GET[x])
              #search_fields = ('@little_bio',)
            elif(x=="programming_language"):
              queryset=Employee.objects.filter(programming_language__name=self.request.GET[x])
             # search_fields = ('programming_language__name',)
            elif(x=="city"):
              queryset=Employee.objects.filter(city=self.request.GET[x])
              #search_fields = ('city',)
            elif(x=="experience_level"):
              queryset=Employee.objects.filter(experience_level=self.request.GET[x])
              #search_fields = ('experience_level',)
            elif(x=="job_title"):
              queryset=Employee.objects.filter(job_title=self.request.GET[x])
              #search_fields = ('job_title',)
            elif(x == 'all'):
              queryset=Employee.objects.filter(Q(programming_language__name=self.request.GET[x]) | Q(little_bio__search=self.request.GET[x]) 
              | Q(city=self.request.GET[x])| Q(job_title=self.request.GET[x]) | Q(experience_level=self.request.GET[x])) 
                #search_fields = ( 'name', 'job_title','@little_bio' , 'programming_language__name', 'city', 'experience_level',)
            #queryset=Employee.objects.filter(search_fields)

        return queryset