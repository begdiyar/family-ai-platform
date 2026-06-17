from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'report_type', 'status', 'file_url', 'created_at']


class CreateReportSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=['diagnostic', 'progress'])
    result_id = serializers.UUIDField(required=False, allow_null=True)


class ShareSerializer(serializers.Serializer):
    share_token = serializers.CharField()
    share_url = serializers.URLField()
    expires_at = serializers.DateTimeField()
