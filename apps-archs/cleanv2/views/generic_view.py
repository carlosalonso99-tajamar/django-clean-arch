from injector import inject
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.generic_serializer import NoteSerializer
from ..use_cases.generic_use_case import CreateNoteUseCase


class CreateNoteView(APIView):
    @inject
    def __init__(self, create_note_use_case: CreateNoteUseCase, **kwargs):
        """
        Inyección directa de dependencias en el constructor.
        """
        super().__init__(**kwargs)
        self.create_note_use_case = create_note_use_case

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        title = serializer.validated_data["title"]
        content = serializer.validated_data["content"]
        note = self.create_note_use_case.execute(title=title, content=content)

        return Response(
            {"title": note.title, "content": note.content, "created_at": note.created_at},
            status=status.HTTP_201_CREATED,
        )
