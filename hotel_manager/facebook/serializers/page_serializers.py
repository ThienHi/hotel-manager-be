from rest_framework import serializers
from hotel_manager.facebook.models import FanPage


class FanPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FanPage
        fields = ['id', 'name', 'page_id', 'page_url', 'avatar_url', 'is_active', 'is_deleted', 'created_by', 'created_at', 'last_subscribe', 'type']

    def create(self, validated_data: dict):
        return FanPage.objects.create(**validated_data) 
    
    def update(self, instance: FanPage, validated_data: dict):
        instance.page_id = validated_data.get('page_id', instance.page_id)
        instance.name = validated_data.get('name', instance.name)
        instance.access_token_page = validated_data.get('access_token_page', instance.access_token_page)
        instance.refresh_token_page = validated_data.get('refresh_token_page', instance.refresh_token_page)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.is_active = validated_data.get('is_active', instance.is_active )
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.last_subscribe = validated_data.get('last_subscribe', instance.last_subscribe)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.type = validated_data.get('type', instance.type)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.page_url = validated_data.get('page_url', instance.page_url)
        instance.save()
        return instance


class FacebookAuthenticationSerializer(serializers.Serializer):
    redirect_url = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


class FacebookConnectPageSerializer(serializers.Serializer):
    is_subscribe = serializers.BooleanField(required=True)
    page_id = serializers.CharField(required=True)
    def validate(self, attrs):
        if attrs.get("page_id"):
            page = FanPage.objects.filter(type='facebook',page_id=attrs.get("page_id")).first()            
            if not page:
                raise serializers.ValidationError({"page_id": "FanPage Invalid"})
            elif page and not page.access_token_page:
                raise serializers.ValidationError({"FanPage": "FanPage was removed on app. Please remove connection!"}) 
        return attrs


class DeleteFanPageSerializer(serializers.Serializer):
    id =  serializers.ListField(child=serializers.IntegerField(min_value=0))
    class Meta:
       fields = ['id']
    def validate(self, attrs):
        for item in attrs.get("id"):
            page = FanPage.objects.filter(id=item).first()
            if not page:
                raise serializers.ValidationError({"id": "FanPage Invalid"})
        return attrs


class WebhookFacebookSerializer(serializers.Serializer):
    mode = serializers.CharField(required=False)
    challenge = serializers.CharField(required=False)
    verify_token = serializers.CharField(required=False)
