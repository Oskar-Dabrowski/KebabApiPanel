from rest_framework import serializers
from .models import Kebab, UserComment, OpeningHour, Suggestion

class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = '__all__'

class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = '__all__'

    def validate_hours(self, value):
        from datetime import datetime

        valid_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
        if not isinstance(value, dict):
            raise serializers.ValidationError("Opening hours must be a JSON object.")

        for day, times in value.items():
            if day not in valid_days:
                raise serializers.ValidationError(f"Invalid day: {day}")
            if "open" not in times or "close" not in times:
                raise serializers.ValidationError(f"Missing 'open' or 'close' for {day}.")
            try:
                datetime.strptime(times["open"], "%H:%M")
                datetime.strptime(times["close"], "%H:%M")
            except ValueError:
                raise serializers.ValidationError(f"Invalid time format for {day}. Use HH:MM.")

        return value

class KebabSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    location = serializers.CharField(source='description')
    comments = UserCommentSerializer(many=True, read_only=True)
    opening_hours = OpeningHourSerializer(many=True, read_only=True)

    class Meta:
        model = Kebab
        fields = '__all__'

    def validate_social_links(self, value):
        """
        Validates the structure of social_links to ensure it is a dictionary
        with valid string keys and values.
        """
        if value:
            if not isinstance(value, dict):
                raise serializers.ValidationError("Social links must be a dictionary.")
            for platform, url in value.items():
                if not isinstance(platform, str) or not isinstance(url, str):
                    raise serializers.ValidationError("Both platform names and URLs must be strings.")
        return value

class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = '__all__'
