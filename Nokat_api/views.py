from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .serializer import *
from django.http import HttpResponse
import requests
import json
from django.http.response import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import *
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from .forms import ImgsFormss
from rest_framework.decorators import api_view
import logging
from rest_framework.views import APIView
from django.views import View

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# Create your views here.


class generics_list_msgstypes(generics.ListCreateAPIView):
    queryset = NokatType.objects.all()
    serializer_class = NokatTypesSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

class generics_list_Nokat(generics.ListCreateAPIView):
    queryset = Nokat.objects.all()
    serializer_class = SnippetsDetailSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
###############
class CustomPageNokatType(PageNumberPagination):
    page_size = 12  # ?II C???C?? ?? C????E
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # ?II C????CE C????
            'current_page': self.page.number,  # ??? C????E C??C??E
            'results': {"NokatTypeModel": data}  # E?I?? ??C ???? "NokatModel" E?E "results"
        })


class SnippetsListViewsNokatType(ListAPIView):
    serializer_class = NokatTypesSerializer
    pagination_class = CustomPageNokatType
    
    def get_queryset(self):
        # C?EII? exclude ?C?EE?CI C????CE C?E? E?E?? ??? new_msgs_text E???E 1
        return NokatType.objects.exclude(new_Nokat_show=1)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"NokatTypeModel": serializer.data})
###############

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12  # ?II C???C?? ?? C????E
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # ?II C????CE C????
            'current_page': self.page.number,  # ??? C????E C??C??E
            'results': {"NokatModel": data}  # E?I?? ??C ???? "NokatModel" E?E "results"
        })


class SnippetsListViews(ListAPIView):
    serializer_class = SnippetsDetailSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        # C?EII? exclude ?C?EE?CI C????CE C?E? E?E?? ??? new_msgs_text E???E 1
        return Nokat.objects.exclude(new_msgs_show=1).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"NokatModel": serializer.data})

class generics_pk_Nokat(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nokat.objects.all()
    serializer_class = SnippetsDetailSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]




################
class CustomPageNokat(PageNumberPagination):
    page_size = 12  # ÿπÿØÿØ ÿßŸÑÿπŸÜÿßÿµÿ± ŸÅŸä ÿßŸÑÿµŸÅÿ≠ÿ©
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # ÿπÿØÿØ ÿßŸÑÿµŸÅÿ≠ÿßÿ™ ÿßŸÑŸÉŸÑŸä
            'current_page': self.page.number,  # ÿ±ŸÇŸÖ ÿßŸÑÿµŸÅÿ≠ÿ© ÿßŸÑÿ≠ÿßŸÑŸäÿ©
            'results': data
        })


class SnippetsNokatWhereTID(ListAPIView):
    serializer_class = SnippetsDetailSerializer
    pagination_class = CustomPageNokat
    
    def get_queryset(self):
        # «” Œ—«Ã ﬁÌ„… ID_Type_id „‰ kwargs
        id_type_id = self.kwargs.get('ID_Type_id')

        # ﬁ„ » ’›Ì… «·«” ⁄·«„ »‰«¡ ⁄·Ï ID_Type_id Ê«” »⁄«œ new_msgs_text=1
        queryset = Nokat.objects.filter(ID_Type_id=id_type_id).exclude(new_msgs_show=1).order_by('-id')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({"NokatModel": serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({"NokatModel": serializer.data})


#####
@staff_member_required
def add_image_nokats(request):
    uploaded_image_urls = []

    if request.method == 'POST':
        form = ImgsFormss(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('pic')
            for image_file in images:
                img_instance = ImagesNokat(pic=image_file)
                img_instance.save()
                uploaded_image_url = request.build_absolute_uri(img_instance.pic.url)
                img_instance.image_url = uploaded_image_url
                img_instance.save()
                uploaded_image_urls.append(uploaded_image_url)
    else:
        form = ImgsFormss()

    return render(request, 'aa/addimgs.html', {'form': form, 'uploaded_image_urls': uploaded_image_urls})

@staff_member_required
def add_image_nokat(request):
    uploaded_image_urls = []

    if request.method == 'POST':
        images = request.FILES.getlist('pic')
        for image_file in images:
            new_img = request.POST.get('new_img')
            img_show = request.POST.get('img_show')
            
            img_instance = ImagesNokat(pic=image_file, new_img=new_img, img_show=img_show)
            img_instance.save()
            
            uploaded_image_url = request.build_absolute_uri(img_instance.pic.url)
            img_instance.image_url = uploaded_image_url
            img_instance.save()
            
            uploaded_image_urls.append(uploaded_image_url)

    return render(request, 'aa/addimgs.html', {'uploaded_image_urls': uploaded_image_urls})




class generics_pk_imgNokat(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImagesNokat.objects.all()
    serializer_class = SnippetsDetailSerializers
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ImageCountView(APIView):

    def get(self, request, *args, **kwargs):
        image_count = ImagesNokat.objects.filter(img_show=0).count()
        return Response({"total_images": image_count})

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12  # ⁄œœ «·⁄‰«’— ›Ì «·’›Õ…
    page_size_query_param = 'page_size'
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # ⁄œœ «·’›Õ«  «·ﬂ·Ì
            'current_page': self.page.number,  # —ﬁ„ «·’›Õ… «·Õ«·Ì…

            'results': {"ImgsNokatModel": data}  #  ⁄œÌ· Â‰« ·Ê÷⁄ "NokatModel"  Õ  "results"
        })


class SnippetsListView(ListAPIView):
    serializer_class = SnippetsDetailSerializers
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        # «” Œœ„ exclude ·«” »⁄«œ «·”Ã·«  «· Ì  Õ ÊÌ ⁄·Ï new_msgs_text »ﬁÌ„… 1
        return ImagesNokat.objects.exclude(img_show=1).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"ImgsNokatModel": serializer.data})

def imgsapi (request,id):
    imgtype = ImageType.objects.get(id=id)
    img=Imgs.objects.exclude(new_msgs_text='1').order_by('-id').filter(ID_Type_id=imgtype.id)

    response = {
        'ImgsModel':list(img.values('id','ID_Type_id','new_img','image_url','created_at','updated_at','new_msgs_text','created_at_new_msgs_text','updated_at_new_msgs_text','my_time_auto'))

    }

    return JsonResponse(response,safe=False,json_dumps_params={'ensure_ascii': False})

def imgsNokatapi(request):
   img = ImagesNokat.objects.exclude(img_show=1).order_by('-id')
   
    
   response = {
        'ImgsNokatModel': list(img.values('id', 'new_img', 'pic','image_url', 'created_at','updated_at'))
    }
        
   return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12  # ⁄œœ «·⁄‰«’— ›Ì «·’›Õ…
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # ⁄œœ «·’›Õ«  «·ﬂ·Ì
            'current_page': self.page.number,  # —ﬁ„ «·’›Õ… «·Õ«·Ì…
            'results': {"ImgsNokatModel": data}  #  ⁄œÌ· Â‰« ·Ê÷⁄ "NokatModel"  Õ  "results"
        })

class SnippetsListViewnew(ListAPIView):
    serializer_class = SnippetsDetailSerializers
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # «” Œœ„ exclude ·«” »⁄«œ «·”Ã·«  «· Ì  Õ ÊÌ ⁄·Ï img_show »ﬁÌ„… 1
        # Ê«” Œœ„ filter · ÕœÌœ «·”Ã·«  «· Ì  Õ ÊÌ ⁄·Ï new_img »ﬁÌ„… 1
        return ImagesNokat.objects.filter(new_img=1).exclude(img_show=1).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"ImgsNokatModel": serializer.data})



@method_decorator(staff_member_required, name='dispatch') 
class UpdateImgNokatView(View):
    def get(self, request, *args, **kwargs):
        # ??? ??????? ?????? ??? ??????? ?????? ???????
        return render(request, 'aa/update_form_view.html')

    def post(self, request, *args, **kwargs):
        # ????? ??? ??????? ??????? ??????? ?? ?????
        rows_to_update_count = int(request.POST.get('rows_to_update', 5))  # ????? ????????? 5

        # ????? ??????? ??????? ??????? (new_msgs_text = '1')
        rows_to_update_ids = ImagesNokat.objects.filter(
            img_show='1'
        ).values_list('id', flat=True)[:rows_to_update_count]

        if not rows_to_update_ids:
            # ?? ???? ????? ???????
            return render(request, 'aa/update_result_view.html', {
                'message': '?? ???? ????? ????? ???????.',
            })

        # ????? ???????
        updated_count = ImagesNokat.objects.filter(id__in=rows_to_update_ids).update(img_show='0')

        # ??? ???????
        return render(request, 'aa/update_result_view.html', {
            'updated_count': updated_count,
        })
        
        
        
        
@staff_member_required        
def update_newImg(request):
    # ????? ???? new_msgs ??? 0 ??? new_msgs=1 ? new_msgs_text=0
    ImagesNokat.objects.filter(new_img=1, img_show=0).update(new_img=0)
    
    # ????? ????? ??????? ??? ??????
    context = {'message': '?? ??????? ?????'}
    return render(request, 'aa/update_page.html', context)   
        
        
        
        

