from rest_framework import serializers
from pinax.stripe.models import Card
from pinax.stripe.models import Plan
from pinax.stripe.models import Subscription


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'address_line_1',
            'address_line_2',
            'address_city',
            'address_state',
            'address_country',
            'address_zip',
            'brand',
            'country',
            'exp_month',
            'exp_year',
            'last4',
        )
        read_only_fields = ('id', 'brand', 'last4',)


class CardCreateSerializer(serializers.Serializer):
    stripe_token = serializers.CharField(
        max_length=191,
        allow_null=False,
        allow_blank=False
    )


class CardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'name',
            'address_line_1',
            'address_line_2',
            'address_city',
            'address_state',
            'address_country',
            'address_zip',
            'country',
            'exp_month',
            'exp_year',
        )


class CardDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ()


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'name', 'amount', 'currency', 'interval',
                  'interval_count', 'trial_period_days',)
        read_only_fields = ('id', 'name', 'amount', 'currency', 'interval',
                            'interval_count', 'trial_period_days',)


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        #fields = ('__all__')
        exclude = ('customer',)


class SubscriptionCreateSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()


class SubscriptionUpdateSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()


class SubscriptionCancelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ()
