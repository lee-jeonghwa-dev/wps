# from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
#
# User = get_user_model()
#
#
# class FacebookAuthTokenView(APIView):
#     def post(self,request):
#         serializer = FacebookAuthTokenSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     pass