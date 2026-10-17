from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Document
        fields = ['id','file','status','created_at','updated_at','processing_started_at']
        read_only_fields = ['created_at','updated_at']

    def validate_file(self,f):
        if f.size > 20 * 1024 * 1024:
            raise serializers.ValidationError('Return Max 20 MB. .')
        return f
    

