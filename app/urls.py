from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index),

    path('input/', views.input),
    path('ReferenceGuide/', views.reference_guide),

    path('card/<card_name>', views.return_result_as_card),

    path('card_info/<card_name>', views.view_card_information),

    path('card_full/<card_name>', views.view_all_cards)
]

handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'
