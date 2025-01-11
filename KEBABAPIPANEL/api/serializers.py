from rest_framework import serializers
from .models import Kebab, Suggestion

from rest_framework import serializers
from api.models import Kebab, UserComment, Favorite

class KebabSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Kebab
        fields = '__all__'

    def get_comments(self, obj):
        comments = UserComment.objects.filter(kebab=obj)
        serializer = UserCommentSerializer(comments, many=True)
        return serializer.data

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            favorite = Favorite.objects.filter(user=request.user, kebab=obj).exists()
            return favorite
        return False

class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = '__all__'
        
class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = '__all__'