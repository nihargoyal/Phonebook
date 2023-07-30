from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Contacts, Profile
from .serializers import ContactSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

# @permission_classes((AllowAny,))
# class RegistrationView(APIView):
#     def post(self, request):
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'message': 'Registration successful', 'user_id': user.id})
#         return Response(serializer.errors, status=400)

@permission_classes((AllowAny,))
class Register(APIView):
	def post(self,request):
		if request.data["name"] is None or request.data["phone_number"] is None:
			return Response(
				{
					"Error":"Both name and phone_number are required"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		try:
			if request.data["email"]:
				email = request.data["email"]
		except:
			email="NONE"
		user=User(
				username=request.data["name"],
				password=request.data["password"],
				email=email,
			)
		if user:
			user.set_password(request.data["password"])
			user.save()
			profile=Profile.objects.create(
	        		user=user,
	        		number=request.data["number"],
	        		email=email,
	        	)
			return Response(
	        	{
	        		"Message":"Registered successfully"
	        	},
	        	status = status.HTTP_200_OK
	        )
		else:
			return Response(
        		{
        			"Message":"Error during Signup!!"
        		},
        		status = status.HTTP_400_BAD_REQUEST
        	)

# class SearchView(APIView):
#     def post(self, request):
#         serializer = SearchSerializer(data=request.data)
#         if serializer.is_valid():
#             name = serializer.validated_data.get('name')
#             phone_number = serializer.validated_data.get('phone_number')

#             if name:
#                 contacts = Contacts.objects.filter(name__istartswith=name)
#             elif phone_number:
#                 contacts = Contacts.objects.filter(phone_number=phone_number)
#             else:
#                 return Response({'message': 'Invalid search request'}, status=400)

#             serialized_data = ContactSerializer(contacts, many=True).data
#             return Response(serialized_data)

#         return Response(serializer.errors, status=400)

class SearchName(APIView):
	def get(self,request):
		name=request.data.get("name")
		if request.data["name"] is None:
			return Response(
				{
					"Error":"Name is required!!"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		profile_start=Profile.objects.filter(user__username__startswith=name)
		profile_contain=Profile.objects.filter(user__username__contains=name).exclude(user__username__startswith=name)
		contact_start=Contacts.objects.filter(name__startswith=name)
		contact_contain=Contacts.objects.filter(name__contains=name).exclude(name__startswith=name)
		response=[]
		for contact in profile_start:
			response.append(
					{
						"name":contact.name,
						"phone_number":contact.phone_number,
						"spam":contact.spam,
					}
				)
		for contact in contact_start:
			response.append(
					{
						"name":contact.name,
						"phone_number":contact.phone_number,
						"spam":contact.spam,
					}
				)
		for contact in profile_contain:
			response.append(
					{
						"name":contact.name,
						"phone_number":contact.phone_number,
						"spam":contact.spam,
					}
				)
		for contact in contact_contain:
			response.append(
					{
						"name":contact.name,
						"phone_number":contact.phone_number,
						"spam":contact.spam,
					}
				)
		return Response(
				response,
				status=status.HTTP_200_OK
			)

class SearchPhoneNumber(APIView):
	def get(self,request):
		phone_number=request.data.get("phone_number")
		if request.data["phone_number"] is None:
			return Response(
				{
					"Error":"Phone number required!!"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		profile=Profile.objects.filter(phone_number=phone_number)
		if profile:
			user=User.objects.filter(id=profile.id,is_active=True)
			return Response(
					{
						"name":user.username,
						"phone_number":profile.phone_number,
						"spam":profile.spam,
						"email":profile.email
					}
				)
		else:
			contact=Contacts.objects.filter(number=phone_number)
			serializer=ContactSerializer(contact,many=True)
			return Response(
					serializer.data
				)

# class UserDetailsView(APIView):
#     def get(self, request):
#         user = request.user
#         serializer = ProfileSerializer(user)
#         return Response(serializer.data)

# class SpamView(APIView):
#     def post(self, request, contact_id):
#         try:
#             contact = Contacts.objects.get(id=contact_id)
#         except Contacts.DoesNotExist:
#             return Response({'message': 'Contacts does not exist'}, status=404)

#         contact.spam_likelihood += 1
#         contact.save()
#         return Response({'message': 'Contacts marked as spam'})

class MarkSpam(APIView):
	def post(self,request):
		phone_number=request.data.get("phone_number")
		if request.data["phone_number"] is None:
			return Response(
				{
					"Error":"Phone number required!!"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		contact=Contacts.objects.filter(phone_number=phone_number).update(spam=True)
		profile=Profile.objects.filter(phone_number=phone_number).update(spam=True)
		if (contact+profile):
			return Response(
				{
					"Message":"Contact marked as spam successfully!!"
				},
				status = status.HTTP_200_OK
			)
		else:
			return Response(
				{
					"Error":"Phone number not found!!"
				},
				status = status.HTTP_404_NOT_FOUND
			)

# class ContactDetailView(APIView):
#     def get(self, request, contact_id):
#         try:
#             contact = Contacts.objects.get(id=contact_id)
#         except Contacts.DoesNotExist:
#             return Response({'message': 'Contacts does not exist'}, status=404)

#         serializer = ContactSerializer(contact)
#         return Response(serializer.data)

class ContactList(APIView):
	def get(self,request):
		contacts=Contacts.objects.all()
		serializer=ContactSerializer(contacts,many=True)
		return Response(
			serializer.data
		)
	def post(self,request):
		if request.data["name"] is None or request.data["phone_number"] is None:
			return Response(
				{
					"Error":"Both name and phone_number are required"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		try:
			if request.data["email"]:
				email=request.data["email"]
		except:
				email=None
		contact=Contacts.objects.create(
				name=request.data["name"],
				phone_number=request.data["phone_number"],
				email=email,
			)
		mapping=MapUserContact.objects.create(
				user=request.user,
				contact=contact,
			)
		return Response(
			{
				"Message":"Contact saved successfully!!"
			},
			status = status.HTTP_201_CREATED
		)

@permission_classes((AllowAny,))
class Login(APIView):
	def post(self,request):
		if not request.data:
			return Response(
				{
					"Error":"Please provide username/password"
				},
				status=status.HTTP_400_BAD_REQUEST
			)
		username=request.data.get("username")
		password=request.data.get("password")
		if username is None or password is None:
			return Response(
				{
					"Error":"Invalid Credentials"
				},
				status=status.HTTP_404_NOT_FOUND
			)
		user = authenticate(username = username, password = password)
		token, _ =Token.objects.get_or_create(user = user)
		return Response(
			{
				"Token":token.key
			},
			status=status.HTTP_200_OK
		)

