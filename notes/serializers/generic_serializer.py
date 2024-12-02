from rest_framework import serializers


class NoteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def create(self, validated_data):
        return validated_data  # Este método se utilizará en la vista
