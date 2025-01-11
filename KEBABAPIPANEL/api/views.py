from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password  # Ensure this is imported
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .fetchers import GoogleRatingsFetcher
from .models import Kebab, Suggestion, Favorite, UserComment
from .serializers import KebabSerializer, SuggestionSerializer, UserCommentSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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


class KebabListView(ListAPIView):
    queryset = Kebab.objects.all()
    serializer_class = KebabSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'craft_rating', 'in_chain']
    ordering_fields = ['name', 'latitude', 'longitude']

    def get(self, request):
        kebabs = Kebab.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(kebabs, request)
        serializer = KebabSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class KebabDetailView(RetrieveAPIView):
    queryset = Kebab.objects.all()
    serializer_class = KebabSerializer
    lookup_field = 'id'

    def get(self, request, id):
        kebab = Kebab.objects.get(id=id)
        serializer = KebabSerializer(kebab)
        return Response(serializer.data)

class GetFavoriteKebabsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        kebabs = [favorite.kebab for favorite in favorites]
        serializer = KebabSerializer(kebabs, many=True)
        return Response(serializer.data)
    
class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        kebab = get_object_or_404(Kebab, id=id)
        Favorite.objects.get_or_create(user=request.user, kebab=kebab)
        return Response({'status': 'success', 'message': 'Added to favorites'}, status=status.HTTP_201_CREATED)

class RemoveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, kebab_id):
        kebab = Kebab.objects.get(id=kebab_id)
        favorite = Favorite.objects.filter(user=request.user, kebab=kebab)
        if favorite.exists():
            favorite.delete()
            return Response({'status': 'success', 'message': 'Kebab removed from favorites'}, status=status.HTTP_200_OK)
        return Response({'error': 'Kebab not found in favorites'}, status=status.HTTP_404_NOT_FOUND)

class AddUserCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        kebab = Kebab.objects.get(id=id)
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        UserComment.objects.create(user=request.user, kebab=kebab, text=text)
        return Response({'status': 'success', 'message': 'Comment added'}, status=status.HTTP_201_CREATED)

class GetUserCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        kebab = Kebab.objects.get(id=id)
        comments = UserComment.objects.filter(kebab=kebab)
        serializer = UserCommentSerializer(comments, many=True)
        return Response(serializer.data)


class SuggestionView(APIView):
    def post(self, request):
        serializer = SuggestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SuggestionListView(APIView):
    def get(self, request):
        suggestions = Suggestion.objects.all()
        serializer = SuggestionSerializer(suggestions, many=True)
        return Response(serializer.data)


class SuggestionListCreateView(ListCreateAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer

class GetKebabStatsView(APIView):

    def get(self, request):
        open_kebabs = Kebab.objects.filter(status='open').count()
        closed_kebabs = Kebab.objects.filter(status='closed').count()
        planned_kebabs = Kebab.objects.filter(status='planned').count()
        return Response({
            'open': open_kebabs,
            'closed': closed_kebabs,
            'planned': planned_kebabs
        })
    
class GetKebabRatingView(APIView):

    def get(self, request, id):
        kebab = Kebab.objects.get(id=id)
        rating = GoogleRatingsFetcher.fetch_google_rating(kebab.name)
        if rating:
            return Response({'rating': rating['rating']})
        return Response({'error': 'Rating not found'}, status=status.HTTP_404_NOT_FOUND)