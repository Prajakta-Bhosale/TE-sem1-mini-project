from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('login/', views.LoginView, name="login"),
    path('otp/', views.OTPView, name="otp"),
    path('options/', views.options, name="options"),
    path('analyze_options/', views.analyze_optionsView, name='analyze_options'),
    path('NewDoc/', views.EventFormView, name="NewDoc"),
    path('Search/', views.SearchView, name="Search"),
    url(r'Search/search/(?P<id>\d+)/$', views.search_event, name='search_event'),
    path('Edit/', views.EditView, name="Edit"),
    url(r'Edit/edit/(?P<id>\d+)/$', views.edit_event, name='edit_event'),
    path('email/', views.email, name='email'),
    path('doc/', views.GeneratePDF, name="GeneratePDF"),
    path('event_analysis/', views.EventAnalysisView, name='EventAnalysis'),
    path('subevent_analysis/', views.SubEventAnalysisView, name='SubEventAnalysis'),
    path('details/', views.DetailsView, name="Details"),
]
