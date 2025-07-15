from rest_framework import serializers
from .models import Pass

class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = [
            'id', 'name', 'email', 'phone', 'temple', 'num_persons',
            'visit_date', 'id_proof_type', 'id_proof_number', 'status',
            'accommodation_date', 'darshan_date', 'darshan_type',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'processed_at', 'processed_by']

class PassAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']