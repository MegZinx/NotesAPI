from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Note
        fields = ["id", "title", "content", "owner", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(slef, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError(
                "Title cannot be empty or just whitespace."
            )
        return value
