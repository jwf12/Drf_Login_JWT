from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from .serializer import UserSerilizer, User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


class RegisterAPIView(APIView):

    def post (self, request):        
        data = request.data#Traemos la data  
        username = data.get('username')  #traemos el username
        email = data.get('email') #traemos el mail
        password = data.get('password') #De ahi sacamos password

        if password: #Validamos         
            data['password'] = make_password(password)# Encripta la contraseña antes de guardarla

        serializer = UserSerilizer(data=data)#serializamos data y seguimos el register

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User created succesfully!'}, status=status.HTTP_201_CREATED)
        else:
            if User.objects.filter(username=username):#validacion del username, unique=True
                return Response({'error': 'Username already exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email):#validacion de mail, unique=True
                return Response({'error': 'Email already exist'}, status=status.HTTP_400_BAD_REQUEST)                
            
            return Response({'error': 'All fields required'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):
        data = request.data
        username = data.get('username') #traemos username
        password = data.get('password') # Traemos pass

        user = User.objects.filter(username=username).first() #Asignamos user

        if user is None:#si no existe user
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)        

        if not user.check_password(password):#Si no existe pass
            return Response({'error': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        #Se instancia tiempo de duracion de el token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        #se crea el token
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
    
        return response

            
class UpdateAPIView(APIView):

    def put(self, request):
        token = request.COOKIES.get('jwt') #traemos el usuario con las cookies
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        object = User.objects.get(id= payload['id'])#Traemos el objeto

        if object:#Validamos

            password = request.data.get('password') #Codificamos la contraseña
            request.data['password'] = make_password(password)

            object_serilize = UserSerilizer(object, data=request.data)#Serializamos el objeto y la actualizacion
            if object_serilize.is_valid():#Validamos

                object_serilize.save()
                return Response({'message': 'Updated'}, status=status.HTTP_200_OK)
            
            return Response({'error': 'All fields required'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class UserGetViewAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        user_serialize = UserSerilizer(user)

        return Response(user_serialize.data)
    

class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt') #Al no tener token se cierra la sesion.
        response.data = {
            'message': 'Logout succesfully'
        }
        return response