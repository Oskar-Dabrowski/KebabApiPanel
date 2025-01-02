from rest_framework import serializers
from .models import Kebab

class KebabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kebab
        fields = '__all__'  

    def validate_social_links(self, value):
        
        if value:
            if not isinstance(value, dict):
                raise serializers.ValidationError("Social links must be a dictionary.")
            for platform, url in value.items():
                if not isinstance(platform, str) or not isinstance(url, str):
                    raise serializers.ValidationError("Both platform names and URLs must be strings.")
        return value
