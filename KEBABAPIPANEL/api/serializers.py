from rest_framework import serializers
from .models import Kebab

class KebabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kebab
        fields = '__all__'
