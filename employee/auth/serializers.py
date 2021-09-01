from rest_framework import serializers
from employee.models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email","password","password2","isEmployer","first_name", "last_name"]

    def save(self,**kwargs):
        user = User(
            email = self.validated_data.get('email'),
        )
        if self.validated_data.get('password') != self.validated_data.get('password2'):
            raise serializers.ValidationError({
                "error":"passwords doesn't match!"
            })
        else:
            user.set_password(self.validated_data.get('password'))
            user.save()