from django.db import models
from shared.models import BaseModel


class FamilyConstitution(BaseModel):
    couple = models.OneToOneField(
        'couples.Couple', on_delete=models.CASCADE, related_name='constitution'
    )
    values = models.JSONField(default=list, blank=True)
    goals = models.JSONField(default=list, blank=True)
    communication_rules = models.JSONField(default=list, blank=True)
    conflict_rules = models.JSONField(default=list, blank=True)
    finance_principles = models.JSONField(default=list, blank=True)
    parenting_approach = models.JSONField(default=list, blank=True)
    is_ai_generated = models.BooleanField(default=False)

    class Meta:
        db_table = 'family_constitutions'

    def __str__(self):
        return f"Constitution(couple={self.couple_id})"

    def is_empty(self):
        return not any([self.values, self.goals, self.communication_rules,
                        self.conflict_rules, self.finance_principles])
