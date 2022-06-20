from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView


class UserRegisterView(ListCreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()



# class VerifyCodeAPIView(APIView):
#     serializer_class = VerifyCodeSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         from accounts.serializers.client.users import UserRetrieveSerializer
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = User.objects.filter(activation_code=serializer.validated_data['activation_code']).first()
#         if not user or not user.is_active:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         data = {}
#         refresh = RefreshToken.for_user(user)
#         serialized_user_object = UserRetrieveSerializer(user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['user'] = json.loads(json.dumps(serialized_user_object.data, ensure_ascii=True))
#         update_last_login(None, user)
#
#         return Response(data, status=status.HTTP_200_OK)
