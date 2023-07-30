from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from .models import Contact, Profile
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from .serializers import ContactSerializer, SearchSerializer, RegistrationSerializer, UserSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
                email=serializer.validated_data.get('email', ''),
            )

            profile = Profile.objects.create(
                user=user,
                number=serializer.validated_data['phone_number']
            )

            return Response({'message': 'Registration successful', 'user_id': user.id})

        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        if not request.data:
                return Response({"Error":"Please provide username/password"}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        return Response({'message': 'Invalid credentials'}, status=401)


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            phone_number = serializer.validated_data.get('phone_number')
            user = request.user

            if name:
                contacts = Contact.objects.filter(
                    Q(name__istartswith=name) | Q(name__icontains=name)
                ).order_by('-name')
            elif phone_number:
                contacts = Contact.objects.filter(phone_number=phone_number)
            else:
                return Response({'message': 'Invalid search request'}, status=400)

            serialized_data = []
            for contact in contacts:
                contact_data = ContactSerializer(contact).data
                contact_data['spam'] = contact.get_spam()

                if contact.user:
                    if user.profile.contact.filter(number=contact.number).exists():
                        contact_data['email'] = contact.user.email
                    else:
                        contact_data.pop('email', None)

                serialized_data.append(contact_data)

            return Response(serialized_data)

        return Response(serializer.errors, status=400)

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class SpamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number=request.data.get("phone_number")
        if request.data["phone_number"] is None:
                    return Response({"Error":"Phone number required!!"}, status = status.HTTP_400_BAD_REQUEST)

        contact = Contact.objects.filter(phone_number=phone_number).update(spam=True)
        if contact:
            return Response({'message': 'Contacts marked as spam'}, status = status.HTTP_200_OK)
        else:
            return Response({"Error":"Phone number not found!!"}, status = status.HTTP_404_NOT_FOUND)

class ContactListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)