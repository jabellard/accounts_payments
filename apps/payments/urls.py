from django.urls import include
from django.conf.urls import url
from django.urls import path
from .views import SubscriptionList
from .views import SubscriptionRetrieveUpdate
from .views import SubscriptionCancel
from .views import CardList
from .views import CardDetail
from .views import PlanList
from .views import PlanRetrieve


urlpatterns = [
    url(r'^subscriptions/$', SubscriptionList.as_view(), name='subscription_list'),
    url(r'^subscriptions/(?P<subscription_id>\d+)/$',
        SubscriptionRetrieveUpdate.as_view(), name='subscription_retrieve_update'),
    url(r'^subscriptions/(?P<subscription_id>\d+)/cancel$',
        SubscriptionCancel.as_view(), name='subscription_cancel'),
    url(r'^cards/$', CardList.as_view(), name='card_list'),
    url(r'^cards/(?P<card_id>\d+)/$', CardDetail.as_view(), name='card_detail'),
    url(r'^plans/$', PlanList.as_view(), name='plan_list'),
    url(r'^plans/(?P<plan_id>\d+)/$', PlanRetrieve.as_view(), name='plan_retrieve'),
]
