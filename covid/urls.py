"""covid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from covid_hospitals.apis import NewPatient, BedStatusBasedOnId, PatientCheckout, GetBedListBasedOnStatus, \
    GetPatientsListBasedOnBedType, BedListBasedOnBedType

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new_patient/', NewPatient.as_view(), name='new_patient'),
    path('bed_status/<int:pk>/', BedStatusBasedOnId.as_view(), name='bed_status_based_d'),
    path('patient_checkout/<int:pk>/', PatientCheckout.as_view(), name='patient_checkout'),
    path('patient_list/', GetPatientsListBasedOnBedType.as_view(),name='patient_list'),
    path('bed_list_based_status/', GetBedListBasedOnStatus.as_view(),name= 'bed_list_based_on_status'),
    path('bed_list_based_type/', BedListBasedOnBedType.as_view(), name= 'bed_list_based_type')

]
