from django.contrib.admin.views.decorators import staff_member_required
from django.forms import modelformset_factory

from django.shortcuts import render, redirect

from .models import *
from django.http import HttpResponse
import requests
import json
from django.http.response import JsonResponse
from .forms import *
from .serializer import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics



def index(request):
    context = {}
    return render(request, "index.html", context)


@staff_member_required
def create_img_type(request):
    if request.method == 'POST':
        img_type_name = request.POST.get('img_type_name')
        new_image_value = request.POST.get('new_image', '1')

        if img_type_name:
            # Use the correct field name "ImgTypes" in the ImageType model
            img_type, created = ImageType.objects.get_or_create(ImgTypes=img_type_name, new_img=new_image_value)

            if created:
                message = "Category created successfully."
            else:
                message = "Category already exists."

            return render(request, 'add.html', {'message': message})

    return render(request, 'add.html')


@staff_member_required
def aaa(request):
    uploaded_image_url = None

    if request.method == 'POST':
        form = ImgsForm(request.POST, request.FILES)
        if form.is_valid():
            img_instance = form.save()
            uploaded_image_url = request.build_absolute_uri(img_instance.pic.url)
            img_instance.image_url = uploaded_image_url
            img_instance.save()
    else:
        form = ImgsForm()

    return render(request, 'img.html', {'form': form, 'uploaded_image_url': uploaded_image_url})


@staff_member_required
def add_img_withTypeType2(request):
    uploaded_image_urls = []

    if request.method == 'POST':
        form = ImgsForm(request.POST, request.FILES)
        if form.is_valid():
           
            images = request.FILES.getlist('pic')

            for image_file in images:
                
                img_instance = Imgs(pic=image_file)
                
                img_instance.ID_Type = form.cleaned_data['ID_Type']
                
                img_instance.save()

                uploaded_image_url = request.build_absolute_uri(img_instance.pic.url)
                
                img_instance.image_url = uploaded_image_url
                img_instance.save()

                uploaded_image_urls.append(uploaded_image_url)

    else:
        form = ImgsForm()

    return render(request, 'img.html', {'form': form, 'uploaded_image_urls': uploaded_image_urls})

@staff_member_required
def add_img_withTypeType(request):
    uploaded_image_urls = []

    if request.method == 'POST':
        new_img = request.POST.get('new_img')
        new_msgs_text = request.POST.get('new_msgs_text')

        # Handle saving new_img and new_msgs_text to the database
        # Add your custom logic here

        form = ImgsForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('pic')

            for image_file in images:
                img_instance = form.save(commit=False)
                img_instance.new_img = new_img
                img_instance.new_msgs_text = new_msgs_text
                img_instance.save()

                uploaded_image_url = request.build_absolute_uri(img_instance.pic.url)
                img_instance.image_url = uploaded_image_url
                img_instance.save()

                uploaded_image_urls.append(uploaded_image_url)

    else:
        form = ImgsForm()

    return render(request, 'img.html', {'form': form, 'uploaded_image_urls': uploaded_image_urls})


def imgtypes_api(request):
    data = ImageType.objects.all().order_by('-id')
    response = {

        'ImgsTypesModel': list(data.values('id','ImgTypes','new_img'))
        #'guests': dict(data.values('name','mobile'))

    }

    return JsonResponse(response,safe=False,json_dumps_params={'ensure_ascii': False})




def imgsapi (request,id):
    imgtype = ImageType.objects.get(id=id)
    img=Imgs.objects.exclude(new_msgs_text='1').order_by('-id').filter(ID_Type_id=imgtype.id)

    response = {
        'ImgsModel':list(img.values('id','ID_Type_id','new_img','image_url','created_at','updated_at','new_msgs_text','created_at_new_msgs_text','updated_at_new_msgs_text','my_time_auto'))

    }

    return JsonResponse(response,safe=False,json_dumps_params={'ensure_ascii': False})

def imgsapi_new(request):
   img = Imgs.objects.filter(new_img=1).order_by('-id')
    
   response = {
        'ImgsModel': list(img.values('id', 'ID_Type_id', 'new_img', 'image_url'))
    }
        
   return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})
   
def imgsapia(request, id):
    # استلام قيم المعلمات من الطلب (startIndex و itemsPerPage)
    start_index = int(request.GET.get('startIndex', 0))
    items_per_page = int(request.GET.get('itemsPerPage', 10))

    imgtype = ImageType.objects.get(id=id)
    # حساب نطاق الصور بناءً على startIndex و itemsPerPage
    img = Imgs.objects.all().order_by('-id').filter(ID_Type_id=imgtype.id)[start_index:start_index + items_per_page]

    response = {
        'ImgsModel': list(img.values('id', 'ID_Type_id', 'new_img', 'image_url'))
    }

    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

def no_rest_Imgs_all (request):
    img = Imgs.objects.all()
    response = {
        'ImgsModel': list(img.values('id', 'ID_Type_id', 'new_img', 'image_url'))
    }

    return JsonResponse(response,safe=False,json_dumps_params={'ensure_ascii': False})


def imgsapi_pa(request, id):
    imgtype = ImageType.objects.get(id=id)
    img_list = Imgs.objects.filter(ID_Type_id=imgtype.id).order_by('-id').values('id', 'ID_Type_id', 'new_img', 'image_url')

    
    items_per_page = 10

    paginator = Paginator(img_list, items_per_page)

    page = request.GET.get('page')
    try:
        img_page = paginator.get_page(page)
    except EmptyPage:
        # إذا كان رقم الصفحة خارج النطاق، يمكنك التعامل مع الخطأ هنا
        return JsonResponse({'error': 'Page not found'}, status=404)

    response = {
        'ImgsModel': list(img_page),
        'current_page': img_page.number,
        'total_pages': paginator.num_pages,
    }

    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

# class CustomPagination(PageNumberPagination):
#     # page_size = 10  # ����� ��� ������� ���� ���� �� �� ����
#     def get_paginated_response(self, data):
#         return Response({
#             'total_pages': self.page.paginator.num_pages,
#             'current_page': self.page.number,
#             'count': self.page.paginator.count,
#             'next': self.get_next_link(),
#             'previous': self.get_previous_link(),
#             'results': data
#         })

# class SnippetsListView(ListAPIView):
#     serializer_class = SnippetsDetailSerializer
#     # pagination_class = CustomPagination  # ����� ��� ������� �������

#     def get_queryset(self):
#         return Imgs.objects.all().order_by('-id')


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12  # عدد العناصر في الصفحة
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # عدد الصفحات الكلي
            'current_page': self.page.number,  # رقم الصفحة الحالية
            'results': data
        })


class SnippetsListViewWhereidtypeidpa(ListAPIView):
    serializer_class = SnippetsDetailSerializer
    pagination_class = CustomPageNumberPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ������� ���� ID_Type_id �� kwargs
        id_type_id = self.kwargs.get('ID_Type_id')

        # �� ������ ��������� ����� ��� ID_Type_id �������� new_msgs_text=1
        queryset = Imgs.objects.filter(ID_Type_id=id_type_id).exclude(new_msgs_text=1).order_by('-id')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({"ImgsModel": serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({"ImgsModel": serializer.data})



def send_notification_page(request):
    return render(request, 'send_notification.html')

def send_notification(request):
    if request.method == 'POST':
        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Authorization': 'key=AAAAhqrLFCo:APA91bEND1dC-5LlVFxsOz6TmpNVDjb8Op1_i2kO-cLqJpV8pC4jiGgElB8eI2IPSw1U-G-c9HiBRQiCU57ItT5J5vM-abCdS9FHAVSuhZTmAZhzgX2d1SQggKN9qJJnLmDIH115lY7o',
            # 'Authorization': 'key=AAAAPgSHYpA:APA91bGqy9XXlDnP9KoD05LYVTeXSlHICeFupGYZpL4QWY0XkZ8kpBuNaM1qf3wvkY5JqdGJuVk3Wu3Q3GmLs4_Qg3ntwH3LLcZqEZ3T-ycXviqFDSb7ap-iX2JlIahMyFHq07CwgD1k',
            'Content-Type': 'application/json'
        }
        payload = {
            'to': '/topics/alert',
            'notification': {
                'title': request.POST.get('title', ''),
                'body': request.POST.get('body', '')
            },
            'data': {
                'data': 'get',
                'pranay': 'pranay',
                'image': 'https://www.webrooper.com/androiddb/uploads/12.jpeg',
                'tag': 'image'
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return HttpResponse(response.text)
    else:
        return HttpResponse('Method Not Allowed')








class generics_pk_imgs(generics.RetrieveUpdateDestroyAPIView):
    queryset = Imgs.objects.all()
    serializer_class = SnippetsDetailSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


#####################




