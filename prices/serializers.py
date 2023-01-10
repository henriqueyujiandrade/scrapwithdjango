from rest_framework import serializers
from .models import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["id", "price", "created_at"]
        read_only_fields = ["price" "created_at"]
