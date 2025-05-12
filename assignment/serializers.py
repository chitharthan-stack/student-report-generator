from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    type = serializers.CharField()
    created_time = serializers.DateTimeField()
    unit = serializers.IntegerField()

class ReportRequestSerializer(serializers.Serializer):
    namespace = serializers.CharField(required=True)
    student_id = serializers.CharField(required=True)
    events = EventSerializer(many=True, required=True)
    student_name = serializers.CharField(required=True)
    score = serializers.IntegerField(required=True)
    remarks = serializers.CharField(required=True)
