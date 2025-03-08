from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from .models import *
from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from .serializer import *
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, filters
import requests
import json
from rest_framework.response import Response
from django.http import Http404
import base64
import sys
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator






# 6 Generics 
#6.1 get and post
class generics_list_msgstypes(generics.ListCreateAPIView):
    queryset = MeesageType.objects.all()
    serializer_class = MsgsTypesSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


   
   # authentication_classes = [TokenAuthentication]
    #authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

#6.2 get put and delete 
class generics_pk_msgstypes(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeesageType.objects.all()
    serializer_class = MsgsTypesSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    

######################################


###############################################


class AllInfoRelatedToIDView(generics.RetrieveAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
        
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs.get('id')  #                            URL
        msgtype = MeesageType.objects.get(id=id)  #                MessageType                
        related_messages = Messages.objects.filter(ID_Type_id=msgtype.id)  #                                     Messages
        
        msgtype_serializer = MsgsTypesSerializer(msgtype)  #           MessageType                         
        messages_serializer = MessegasSerializer(related_messages, many=True)  #                  Messages                         
        
        return Response({
            'message_type_info': msgtype_serializer.data,
            'related_messages_info': messages_serializer.data
        })
    


    
#class generics_msgs(generics.ListCreateAPIView):
#    queryset = Messages.objects.all()
#    serializer_class = MessegasSerializer
#    authentication_classes = [BasicAuthentication]
#    permission_classes = [IsAuthenticated]

class CustomPageNumberPagination2(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class generics_msgs(generics.ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessegasSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination2


    

#6.2 get put and delete 
class generics_pk_msgs(generics.RetrieveUpdateDestroyAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessegasSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
   




def msgtypes_api_show(request):
    #                               new_msgs_text       0
    data = MeesageType.objects.exclude(new_msgs_text=1).values(
        'id', 'MsgTypes', 'new_msg', 'new_msgs_text', 'created_at_new_msgs_text', 'updated_at_new_msgs_text','my_time_auto'
    )

    response = {
        'MsgsTypesModel': list(data)
    }

    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})





def msgsapi_show(request, id):
    msgtype = MeesageType.objects.get(id=id)
    
    #                                   new_msgs_text    0
    msg = Messages.objects.exclude(new_msgs_text='1').filter(ID_Type_id=msgtype.id)

    response = {
        'MsgsModel': list(msg.values('id', 'MessageName', 'new_msgs', 'ID_Type_id', 

'created_at', 'updated_at', 'new_msgs_text', 'created_at_new_msgs_text', 

'updated_at_new_msgs_text'))
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
            'results': data
        })

class SnippetsListViewWhereidtypeidpa(ListAPIView):
    serializer_class = MessegasSerializer
    pagination_class = CustomPageNumberPagination
    

    def get_queryset(self):
        # «” »⁄«œ «·’›Ê› ÕÌÀ new_msgs_text=1
        queryset = Messages.objects.exclude(new_msgs_text=1)

        # ≈–«  „  Ê›Ì— ID_Type_id ›Ì «·ÿ·»° «” Œœ„Â ··»ÕÀ
        id_type_id = self.kwargs.get('ID_Type_id')
        if id_type_id is not None:
            queryset = queryset.filter(ID_Type_id=id_type_id).exclude(new_msgs_text=1)

        # «—Ã«⁄ «·‰ ÌÃ… „— »…  ‰«“·Ì« Õ”» id
        return queryset.order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # ﬁ„ »«·Õ’Ê· ⁄·Ï ’›Õ… «·»Ì«‰«  »«” Œœ«„ «· ﬁ”Ì„
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({"MsgsModel": serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({"MsgsModel": serializer.data})

def no_rest_msgs_all (request):
    data = Messages.objects.all()
    response = {
        'data': list(data.values('msgs_types','msgs_name','new_msgs'))
    }

    return JsonResponse(response,safe=False,json_dumps_params={'ensure_ascii': False})

def send_notification_page(request):
    return render(request, 'send_notification.html')

def send_notification(request):
    if request.method == 'POST':
        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Authorization': 'key=AAAAQoSHBzU:APA91bF8BsHHVYLiTjrFCYKeBLvezTBXg7GTKqS0ur2p8zTtGsbN-FkjUpHrZYUzdETwJ-Rd0uf5Zp8ebC6JWEI_q5TnsI5117skL5RnPFf0qTvJdvnurm1tvPJsjekrV7zyaxFkdeLa',
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
###################################

class CustomPageMeesageTypess(PageNumberPagination):
    page_size = 12  # ?II C???C?? ?? C????E
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # ?II C????CE C????
            'current_page': self.page.number,  # ??? C????E C??C??E
            'results': {"MsgsTypesModel": data}  # E?I?? ??C ???? "NokatModel" E?E "results"
        })


class SnippetsListViewsMsgssType(ListAPIView):
    serializer_class = MsgsTypesSerializer
    pagination_class = CustomPageMeesageTypess
    
    def get_queryset(self):
        # C?EII? exclude ?C?EE?CI C????CE C?E? E?E?? ??? new_msgs_text E???E 1
        return MeesageType.objects.exclude(new_msgs_text=1)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"MsgsTypesModel": serializer.data})


class CustomPageMessagess(PageNumberPagination):
    page_size = 12  # ⁄œœ «·⁄‰«’— ›Ì «·’›Õ…
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # ≈Ã„«·Ì ⁄œœ «·⁄‰«’—
            'total_pages': self.page.paginator.num_pages,  # ≈Ã„«·Ì ⁄œœ «·’›Õ« 
            'current_page': self.page.number,  # —ﬁ„ «·’›Õ… «·Õ«·Ì…
            'results': data  # «·»Ì«‰«  ›Ì «·’›Õ… «·Õ«·Ì…
        })


class SnippetsMsgssWhereTID(ListAPIView):
    serializer_class = MessegasSerializer
    pagination_class = CustomPageMessagess
    
    def get_queryset(self):
        # «” Œ—«Ã ﬁÌ„… ID_Type_id „‰ «·„⁄«„·« 
        id_type_id = self.kwargs.get('ID_Type_id')
        
        #  ’›Ì… «·—”«∆· »‰«¡ ⁄·Ï ID_Type_id Ê«” »⁄«œ «·—”«∆· «· Ì  Õ ÊÌ ⁄·Ï new_msgs_text = 1
        queryset = Messages.objects.filter(ID_Type_id=id_type_id).exclude(new_msgs_text=1).order_by('-id')
        
        # ÿ»«⁄… ⁄œœ «·—”«∆· «·„” —Ã⁄…
        print(f"Fetched {queryset.count()} messages for ID_Type_id: {id_type_id}")
        
        return queryset

    def list(self, request, *args, **kwargs):
        # «·Õ’Ê· ⁄·Ï «·—”«∆· «·„’›«…
        queryset = self.get_queryset()

        #  ÿ»Ìﬁ «· ’›Õ ⁄·Ï «·‰ «∆Ã
        page_number = request.GET.get('page', 1)  # «·’›Õ… «·«› —«÷Ì… ÂÌ 1
        page_number = int(page_number)

        #  Õﬁﬁ „‰ ’Õ… —ﬁ„ «·’›Õ…
        total_count = queryset.count()  # «·⁄œœ «·≈Ã„«·Ì ··—”«∆·
        total_pages = (total_count + self.pagination_class.page_size - 1) // self.pagination_class.page_size  # Õ”«» ≈Ã„«·Ì «·’›Õ« 
        
        if page_number < 1 or page_number > total_pages:
            raise NotFound("Invalid page number.")  # √Ê Ì„ﬂ‰ﬂ ≈⁄«œ… —”«·… Œÿ√ „Œ’’…

        page = self.paginate_queryset(queryset)

        if page is not None:
            # ≈–« ﬂ«‰  Â‰«ﬂ ’›Õ«  „ ⁄œœ…° ≈⁄«œ… «·»Ì«‰«  „⁄  ›«’Ì· «· ’›Õ
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({"MsgsModel": serializer.data})

        # ≈–« ﬂ«‰  «·‰ «∆Ã ﬂ·Â« ›Ì ’›Õ… Ê«Õœ…° ≈—Ã«⁄Â« „»«‘—…
        serializer = self.get_serializer(queryset, many=True)
        return Response({"MsgsModel": serializer.data})
        
        
        ####################
        

@method_decorator(staff_member_required, name='dispatch') 
class UpdateMessagesView(View):
    def get(self, request, *args, **kwargs):
        # ??? ???? ??????? ?? ???? MessageType
        message_types = MeesageType.objects.all()

        # ??? ??????? ?? ????? ??????? ??? ??????
        return render(request, 'Msgs_Api/update_form_view.html', {
            'message_types': message_types,
        })
        
    def post(self, request, *args, **kwargs):
        # ?????? ??? ??? ?????? ???? ???? ??????? ?? ???????
        rows_to_update_count = int(request.POST.get('rows_to_update', 5))  # ?????? ?????????? ?? 50
        id_type_id = request.POST.get('ID_Type_id')  # ?????? ??? ID_Type_id ?? ?????

        # ?????? IDs ?????? ????????
        rows_to_update_ids = Messages.objects.filter(
            ID_Type_id=id_type_id,
            new_msgs_text='1'
        ).values_list('id', flat=True)[:rows_to_update_count]

        if not rows_to_update_ids:
            # ??? ?? ??? ???? ?????? ??????? ??? ????? ??????
            return render(request, 'Msgs_Api/update_result_view.html', {
                'message': '?? ???? ?????? ?????? ???????.',
                'ID_Type_id': id_type_id,
            })

        # ????? ?????? ???????? IDs
        updated_count = Messages.objects.filter(id__in=rows_to_update_ids).update(new_msgs_text='0')

        # ??? ??????? ?? ???? ????? ?? ??? ?????? ???????
        return render(request, 'Msgs_Api/update_result_view.html', {
            'updated_count': updated_count,
            'ID_Type_id': id_type_id,
        })

        

@staff_member_required        
def update_msgs(request):
    # ????? ???? new_msgs ??? 0 ??? new_msgs=1 ? new_msgs_text=0
    Messages.objects.filter(new_msgs=1, new_msgs_text=0).update(new_msgs=0)
    
    # ????? ????? ??????? ??? ??????
    context = {'message': '?? ??????? ?????'}
    return render(request, 'Msgs_Api/update_page.html', context)   
    

  
        
        
        
        
        
        
        
        
        
        
