from django.db import models
from shared.models import BaseModel


class DailyPractice(BaseModel):
    couple = models.ForeignKey('couples.Couple', on_delete=models.CASCADE, related_name='daily_practices')
    date = models.DateField()
    question_of_day = models.TextField()
    conversation_topic = models.TextField()
    trust_exercise = models.TextField()
    communication_exercise = models.TextField()
    family_activity = models.TextField()
    romantic_idea = models.TextField()
    is_ai_generated = models.BooleanField(default=False)
    i18n = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'daily_practices'
        unique_together = [['couple', 'date']]
        indexes = [models.Index(fields=['couple', '-date'])]

    def __str__(self):
        return f"DailyPractice({self.couple_id}, {self.date})"


class PracticeCompletion(BaseModel):
    practice = models.ForeignKey(DailyPractice, on_delete=models.CASCADE, related_name='completions')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'practice_completions'
        unique_together = [['practice', 'user', 'field_name']]
