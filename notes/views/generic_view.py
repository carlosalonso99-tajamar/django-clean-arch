from rest_framework import status, views
from rest_framework.response import Response
from ..serializers.generic_serializer import NoteSerializer
from ..use_cases.generic_use_case import CreateNoteUseCase


class CreateNoteView(views.APIView):
    def post(self, request):
        # 1. Validar la entrada usando el serializador
        serializer = NoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Delegar la lógica de negocio al caso de uso
        use_case = CreateNoteUseCase()
        note_data = serializer.validated_data
        note = use_case.execute(note_data["title"], note_data["content"])

        # 3. Serializar la respuesta para enviarla al cliente
        return Response(
            {
                "title": note.title,
                "content": note.content,
                "created_at": note.created_at,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        return Response("Hello, world!")
