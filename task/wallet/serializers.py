from rest_framework import serializers
from .models import Wallet, User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'email',
                  'first_name',
                  'last_name')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','uuid' ,'balance']


class OperationSerializer(serializers.Serializer):
    operationType = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW'])
    amount = serializers.DecimalField(max_digits=20, decimal_places=4)

    # fields = ['operation_type', 'amount']