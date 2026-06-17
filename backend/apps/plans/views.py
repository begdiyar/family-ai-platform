from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shared.exceptions import NotFoundError
from apps.couples.repositories import CoupleRepository
from .models import RecoveryPlan
from .repositories import PlanRepository
from .serializers import PlanDetailSerializer, CompleteTaskSerializer, CreatePlanSerializer
from .services import PlanService


class PlanCreateView(APIView):
    def post(self, request):
        serializer = CreatePlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result_id = str(serializer.validated_data.get('result_id', '') or '')
        plan = PlanService.create_plan(request.user, result_id=result_id or None)
        couple = CoupleRepository.get_active_for_user(request.user)
        return Response(
            PlanDetailSerializer(plan, context={'user': request.user, 'couple': couple}).data,
            status=status.HTTP_201_CREATED,
        )


class PlanCurrentView(APIView):
    def get(self, request):
        couple = CoupleRepository.get_active_for_user(request.user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Нет активной пары')
        plan = PlanRepository.get_active_for_couple(couple)
        if not plan:
            raise NotFoundError('NO_PLAN', 'Активный план не найден')
        return Response(
            PlanDetailSerializer(plan, context={'user': request.user, 'couple': couple}).data
        )


class TaskCompleteView(APIView):
    def post(self, request, plan_id, task_id):
        serializer = CompleteTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = PlanService.complete_task(
            user=request.user,
            plan_id=str(plan_id),
            task_id=str(task_id),
            note=serializer.validated_data.get('note'),
        )
        return Response(result)

    def delete(self, request, plan_id, task_id):
        PlanService.undo_task(request.user, str(task_id), str(plan_id))
        return Response(status=status.HTTP_204_NO_CONTENT)
