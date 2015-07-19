# -*- coding: utf-8 -*-

# def ds_checkrequest_form():
#     if request.method == 'POST':
#         return "required.method = POST"
#     else :
#         return "else return"
#     return 

from main.models import Topic
    
def ds_showtopic(id=0, bywhat=0):
    if bywhat == 0:
        topic = Topic.objects.get(id=id)
    elif id == 0:
        topic = Topic.objects.order_by('bywhat')
    elif bywhat == 0 & id == 0:
        topic = "error"
    return topic