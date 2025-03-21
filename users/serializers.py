from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializers, UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializers):
    class Meta(BaseUserCreateSerializers.Meta):
        fields = ['id', 'email', 'password', 'first_name',
                  'last_name', 'address', 'phone_number']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'first_name',
                  'last_name', 'address', 'phone_number']
