from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FamilyConstitutionSerializer
from .services import ConstitutionService


class ConstitutionView(APIView):
    def get(self, request):
        constitution = ConstitutionService.get_or_create(request.user)
        return Response(FamilyConstitutionSerializer(constitution).data)

    def put(self, request):
        constitution = ConstitutionService.update(request.user, request.data)
        return Response(FamilyConstitutionSerializer(constitution).data)


class ConstitutionGenerateView(APIView):
    def post(self, request):
        constitution = ConstitutionService.generate_with_ai(request.user)
        return Response(FamilyConstitutionSerializer(constitution).data)
