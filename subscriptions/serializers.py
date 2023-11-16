from rest_framework import serializers

from subscriptions.models import Package, Subscription


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('title', 'sku', 'description', 'avatar', 'price', 'duration')


class SubscriptionSerializer(serializers.ModelSerializer):
    package = PackageSerializer

    class Mata:
        model = Subscription
        fields = ('package', 'created_time', 'expire_time')
