from rest_framework import serializers
from .models import FamilyConstitution


class FamilyConstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyConstitution
        fields = ['id', 'values', 'goals', 'communication_rules', 'conflict_rules',
                  'finance_principles', 'parenting_approach', 'is_ai_generated', 'updated_at']
