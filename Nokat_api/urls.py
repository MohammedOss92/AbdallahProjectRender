from django.urls import path
from . import views
from .views import *
from django.urls import include


urlpatterns = [
path('add_image_nokat/', views.add_image_nokat, name='add_imgs'),
path('imgnokatapi/', SnippetsListView.as_view(), name='snippets-list'),
path('imgnokatup/<int:pk>', generics_pk_imgNokat.as_view(), name='snippets-list'),
path('imgsNokatapiold/', views.imgsNokatapi, name='add_imgs'),
path('imgnokatapinew/', SnippetsListViewnew.as_view(), name='snippets-list'),
path('generics/', views.generics_list_msgstypes.as_view()),
path('genericsnokat/', views.generics_list_Nokat.as_view()),
path('nokatapi/', SnippetsListViews.as_view(), name='snippets-list'),
path('nokatup/<int:pk>', generics_pk_Nokat.as_view(), name='snippets-list'),
path('image-count/', ImageCountView.as_view(), name='image-count'), 
path('nokatapiids/<int:ID_Type_id>', SnippetsNokatWhereTID .as_view(), name='snippets-list'),
path('nokattypes/', SnippetsListViewsNokatType.as_view(), name='snippets-list'),
path('update-new-img-nokat/', views.update_newImg, name='update-new-img-nokat'),
path('updateimgnokat/', UpdateImgNokatView.as_view(), name='update_messages'),


]

