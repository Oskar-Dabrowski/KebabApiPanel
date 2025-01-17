from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Kebab, Suggestion, Favorite, UserComment, OpeningHour
from django.http import JsonResponse
from .serializers import (
    FeedbackSerializer, KebabSerializer, SuggestionSerializer, UserCommentSerializer, OpeningHourSerializer
)

# User Registration
class RegisterUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=email).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=email, password=make_password(password))
        return Response({'status': 'success', 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


# User Login
class LoginUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(username=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'token': str(refresh.access_token),
                'email': user.username
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Kebab List and Details
class KebabListView(ListAPIView):
    queryset = Kebab.objects.all()
    serializer_class = KebabSerializer


class KebabDetailView(RetrieveAPIView):
    queryset = Kebab.objects.all()
    serializer_class = KebabSerializer
    lookup_field = 'id'


# Kebab Hours View
class KebabHoursView(APIView):
    def get(self, request):
        kebabs = Kebab.objects.all()
        kebab_hours = []
        for kebab in kebabs:
            opening_hours = kebab.openinghour_set.first()  # Get the first associated opening hours
            if opening_hours:
                hours = opening_hours.hours
                kebab_hours.append({
                    'name': kebab.name,
                    'hours': hours
                })
        return Response(kebab_hours)


# Favorite Management
class GetFavoriteKebabsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        data = [{'id': fav.kebab.id, 'name': fav.kebab.name} for fav in favorites]
        return Response(data)


class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        kebab = get_object_or_404(Kebab, id=id)
        Favorite.objects.get_or_create(user=request.user, kebab=kebab)
        return Response({'status': 'success', 'message': 'Added to favorites'}, status=status.HTTP_201_CREATED)


class RemoveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        kebab = get_object_or_404(Kebab, id=id)
        Favorite.objects.filter(user=request.user, kebab=kebab).delete()
        return Response({'status': 'success', 'message': 'Removed from favorites'}, status=status.HTTP_200_OK)


# Comments Management
class AddUserCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        kebab = get_object_or_404(Kebab, id=id)
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)
        UserComment.objects.create(user=request.user, kebab=kebab, text=text)
        return Response({'status': 'success', 'message': 'Comment added'}, status=status.HTTP_201_CREATED)


class GetKebabCommentsView(APIView):
    def get(self, request, id):
        kebab = get_object_or_404(Kebab, id=id)
        comments = UserComment.objects.filter(kebab=kebab)
        serializer = UserCommentSerializer(comments, many=True)
        return Response(serializer.data)


# Bulk Opening Hours Management
class BulkOpeningHoursView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        hours_data = request.data.get('hours', [])
        for entry in hours_data:
            kebab = get_object_or_404(Kebab, id=entry.get('kebab_id'))
            OpeningHour.objects.update_or_create(
                kebab=kebab,
                defaults={'hours': entry.get('hours')}
            )
        return Response({'status': 'success', 'message': 'Opening hours updated successfully'}, status=status.HTTP_200_OK)


# Suggestion Management
class SuggestionListCreateView(ListCreateAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer


class SuggestionView(APIView):
    def post(self, request):
        serializer = SuggestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuggestionListView(APIView):
    def get(self, request):
        suggestions = Suggestion.objects.all()
        serializer = SuggestionSerializer(suggestions, many=True)
        return Response(serializer.data)

def kebab_list_view(request):
    """
    API View to return kebab data filtered by Legnica.
    """
    kebabs = Kebab.objects.filter(
        latitude__gte=51.1500, latitude__lte=51.2300,
        longitude__gte=16.1200, longitude__lte=16.2500
    )
    
    data = [
        {
            'name': kebab.name,
            'latitude': kebab.latitude,
            'longitude': kebab.longitude,
            'meats': kebab.meats,
            'sauces': kebab.sauces,
            'status': kebab.status,
            'google_rating': kebab.google_rating,
            'pyszne_rating': kebab.pyszne_rating,
        }
        for kebab in kebabs
    ]
    return JsonResponse({'kebabs': data})

class FeedbackView(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Feedback added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)