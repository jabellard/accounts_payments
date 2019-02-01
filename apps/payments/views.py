from django.utils.encoding import smart_str

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from pinax.stripe.models import Card
from pinax.stripe.models import Plan
from pinax.stripe.models import Subscription
from .serializers import CardSerializer
from .serializers import CardCreateSerializer
from .serializers import CardUpdateSerializer
from .serializers import CardDestroySerializer
from .serializers import PlanSerializer
from .serializers import SubscriptionSerializer
from .serializers import SubscriptionCreateSerializer
from .serializers import SubscriptionUpdateSerializer
from .serializers import SubscriptionCancelSerializer
import stripe

from pinax.stripe.mixins import CustomerMixin as _CustomerMixin
from pinax.stripe.actions import subscriptions
from pinax.stripe.actions import sources
from pinax.stripe.actions import customers


class CustomerMixin(_CustomerMixin):
    @property
    def customer(self):
        if not hasattr(self, "_customer"):
            self._customer = customers.get_customer_for_user(self.request.user)
            if self._customer is None:
                self._customer = customers.create(self.request.user)
        return self._customer


def get_customer_subscription_queryset(customer):
    return Subscription.objects.filter(customer=customer)


class SubscriptionList(CustomerMixin, generics.ListCreateAPIView):
    model = Subscription
    queryset = None
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = get_customer_subscription_queryset(customer=self.customer)
        self.queryset = queryset
        return queryset

    def subscribe(self, plan):
        subscriptions.create(customer=self.customer, plan=plan)

    def get(self, request, *args, **kwargs):
        self.serializer_class = SubscriptionSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = SubscriptionCreateSerializer
        try:
            plan = Plan.objects.get(id=request.data["plan_id"])
        except Plan.DoesnNotExist:
            return Response(
                {
                    'detail': 'Plan with specified plan_id does not exist.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            self.subscribe(plan=plan)
        except stripe.error.StripeError as e:
            return Response(
                {
                    'detail': smart_str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {
                'detail': 'OK.'
            },
            status=status.HTTP_200_OK
        )


class SubscriptionRetrieveUpdate(CustomerMixin, generics.RetrieveUpdateAPIView):
    model = Subscription
    queryset = None
    lookup_url_kwarg = 'subscription_id'
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = get_customer_subscription_queryset(customer=self.customer)
        self.queryset = queryset
        return queryset

    def update_subscription(self, plan):
        subscriptions.update(subscription=self.object, plan=plan)

    def get(self, request, *args, **kwargs):
        self.serializer_class = SubscriptionSerializer
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return Response(
            {
                'detail': 'Not implemented. Use PATCH'
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def patch(self, request, *args, **kwargs):
        self.serializer_class = SubscriptionUpdateSerializer
        self.object = self.get_object()
        try:
            plan = Plan.objects.get(id=request.data["plan_id"])
        except Plan.DoesNotExist:
            return Response(
                {
                    'detail': 'Plan with specified plan_id does not exist.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            self.update_subscription(plan=plan)
        except stripe.error.StripeError as e:
            return Response(
                {
                    'detail': smart_str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {
                'detail': 'OK.'
            },
            status=status.HTTP_200_OK
        )


class SubscriptionCancel(CustomerMixin, generics.UpdateAPIView):
    model = Subscription
    queryset = None
    lookup_url_kwarg = 'subscription_id'
    serializer_class = SubscriptionCancelSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = get_customer_subscription_queryset(customer=self.customer)
        self.queryset = queryset
        return queryset

    def cancel_subscription(self):
        subscriptions.cancel(subscription=self.object)

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.cancel_subscription()
        except stripe.error.StripeError as e:
            return Response(
                {
                    'detail': smart_str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {
                'detail': 'OK.'
            },
            status=status.HTTP_200_OK
        )


def get_customer_card_queryset(customer):
    return Card.objects.filter(customer=customer)


class CardList(CustomerMixin, generics.ListCreateAPIView):
    model = Card
    queryset = None
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = get_customer_card_queryset(customer=self.customer)
        self.queryset = queryset
        return queryset

    def create_card(self, customer, stripe_token):
        sources.create_card(customer=customer, token=stripe_token)

    def get(self, request, *args, **kwargs):
        self.serializer_class = CardSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = CardCreateSerializer
        try:
            self.create_card(self.customer, request.data['stripe_token'])
        except stripe.error.StripeError as e:
            return Response(
                {
                    'detail': smart_str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {
                'detail': 'OK.'
            },
            status=status.HTTP_200_OK
        )


class CardDetail(CustomerMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Card
    queryset = None
    lookup_url_kwarg = 'card_id'
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = get_customer_card_queryset(customer=self.customer)
        self.queryset = queryset
        return queryset

    def update_card(self, name=None, exp_month=None, exp_year=None):
        sources.update_card(
            customer=self.customer,
            source=self.object.stripe_id,
            name=name,
            exp_month=exp_month,
            exp_year=exp_year
        )

    def delete_card(self):
        sources.delete_card(customer=self.customer, source=self.object.stripe_id)

    def get(self, request, *args, **kwargs):
        self.serializer_class = CardSerializer
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.serializer_class = CardUpdateSerializer
        self.object = self.get_object()
        try:
            name = None
            exp_month = None
            exp_year = None
            if 'name' in request.data:
                name = request.data['name']
            if 'exp_month' in request.data:
                exp_month = request.data['exp_month']
            if 'exp_year' in request.data:
                exp_year = request.data['exp_year']
            self.update_card(name=name, exp_month=exp_month, exp_year=exp_year)
        except stripe.error.StripeError as e:
            return Response(
                {
                    'detail': smart_str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {
                'detail': 'OK.'
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        self.serializer_class = CardDestroySerializer
        self.object = self.get_object()
        try:
            self.delete_card()
        except stripe.error.StripeError as e:
            return Response(
                {
                    'detail': smart_str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {
                'detail': 'OK.'
            },
            status=status.HTTP_200_OK
        )


class PlanList(generics.ListAPIView):
    model = Plan
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        self.serializer_class = PlanSerializer
        return self.list(request, *args, **kwargs)


class PlanRetrieve(generics.RetrieveAPIView):
    queryset = Plan.objects.all()
    lookup_url_kwarg = 'plan_id'
    serializer_class = PlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        self.serializer_class = PlanSerializer
        return self.retrieve(request, *args, **kwargs)
