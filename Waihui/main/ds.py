# -*- coding: utf-8 -*-

# def ds_checkrequest_form():
#     if request.method == 'POST':
#         return "required.method = POST"
#     else :
#         return "else return"
#     return 

from main.models import Topic
from main.models import User
    
def ds_showtopic(id=0, bywhat=0):
    if bywhat == 0:
        topic = Topic.objects.get(id=id)
    elif id == 0:
        topic = Topic.objects.order_by('bywhat')
    elif bywhat == 0 & id == 0:
        topic = "error"
    return topic

def ds_addlog(source, type, user, character):
    user=User.objects.get(id=user)
    log = Log(source=source,
        type=type,
        user=user,
        character=character)
    log.save()
    return "OK!" + "from " + log.source + "log.user" + " logged in"
