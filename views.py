
import urllib.parse

import datetime
import requests
import json
from allauth.account.views import LogoutView
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.dispatch import Signal

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from users.forms import serviceproviderupdateform
from .forms import Add,login,Planss,verify1
from django.http import Http404, HttpResponse
from .models import Serviceprovider,Plan
from users.models import UserInfo,Status



@login_required()
def verify(request):
    #print("verify",request.user)

    if request.method=="GET":
        form=verify1()
        return render(request,'serviceproviders/verify.html',{'form':form})

    else:
        form=verify1(request.POST)
        add=request.POST['address']
        u=UserInfo.objects.get(user=request.user)
        u.add=add
        no=request.POST['mobile']
        #http://apilayer.net/api/validate?access_key=89b47e0348ec0941065d2b7c41cea454&number=8805047039&country_code=IN&format=1
        url1="http://apilayer.net/api/validate?access_key=89b47e0348ec0941065d2b7c41cea454&number="
        url3="&country_code=IN&format=1"
        url=url1+str(no)+url3
        json=requests.get(url).json()
        #print(json)
        #print(json["valid"])
        if json["valid"] is True:
            u.phone=no
            u.save()
            return redirect("serviceproviders:login")
        else:
            return render(request, 'serviceproviders/verify.html',{'error_message':'please enter valid number','form':form})
"""@login_required()
def verified(request):
    if request.method=='GET':
        #print("verified0,", request.user)
        s = request.get_full_path()
        s1 = s.split('&')
        acesscode = s1[1][5:]
        url1 = "https://graph.accountkit.com/v1.3/access_token?grant_type=authorization_code&code="
        url3 = "&access_token=AA|411475515942089|d5b709cc83bfa26ed7283ab9df162015"
        url2 = acesscode
        #print(acesscode)
        url = url1 + url2 + url3
        json = requests.get(url).json()
        #print(json)
        url1 = "https://graph.accountkit.com/v1.3/me/?access_token="
        url2 = json['access_token']
        url = url1 + url2
        json = requests.get(url).json()
        #print(json)
        no = json["phone"]["national_number"]
        # https://graph.accountkit.com/v1.3/logout?access_token=
        url1 = "https://graph.accountkit.com/v1.3/logout?access_token="
        url = url1 + url2
        #print(url)
        json = requests.post(url).json()
        #print("afterlogut", request.user, json["success"])

        return redirect("http://127.0.0.1:8000/accounts/logout1/")
    else:
        #print("hiiiiiii")"""

def plans(request):
    if request.method=="POST":
       sorted_name = request.POST.getlist('sorted_name')
       if len(sorted_name)>0:
           sorted_name = request.POST.getlist('sorted_name')

           """        for i in range(0,len(sorted_name)):
               serviceprobiders.append(Serviceprovider.objects.filter(service_providers_name__icontains=sorted_name[i]))
           #print(len(serviceprobiders),"length")
           for i in range(0,len(serviceprobiders)):
               #print(serviceprobiders[i])"""
           #print("sssssssssssssssssss",sorted_name)

           plans = Plan.objects.filter(serviceprovider_id__in=sorted_name)

           """            except:
                   #print("except")
                   pass"""
           #print("XXXXXXXXXXXXXXX", plans)

           #print("all", plans)
           plan_list = []
           for i in range(0, len(plans)):
               plan_list.append(plans[i].id)
           #print(plan_list)
           one_month = []
           planstosort = []
           three_month = []
           six_months = []
           yearly = []
           data = []
           ids1 = []
           ids3 = []
           ids6 = []
           ids12 = []

           for i in range(0, len(plans)):
               ids1.append(plans[i].id)
               ids3.append(plans[i].id)
               ids6.append(plans[i].id)
               ids12.append(plans[i].id)
           for i in range(0, len(plans)):
               one_month.append(plans[i].monthly_rate)
           for i in range(0, len(plans)):
               planstosort.append(plans[i].plan)
           #print(planstosort, "xxx")
           for i in range(0, len(plans)):
               three_month.append(plans[i].tree_months)
           for i in range(0, len(plans)):
               six_months.append(plans[i].six_months)
           for i in range(0, len(plans)):
               yearly.append(plans[i].yearly)
           for i in range(0, len(plans)):
               data.append(plans[i].data)
           # onemonth
           #print(planstosort, "1")
           #print("data1", data)

           for i in range(0, len(one_month) - 1):

               for j in range(0, len(one_month) - i - 1):

                   if one_month[j] < one_month[j + 1]:

                       pass
                   elif one_month[j] == one_month[j + 1]:
                       if planstosort[j] < planstosort[j + 1]:
                           planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                           one_month[j], one_month[j + 1] = one_month[j + 1], one_month[j]
                           ids1[j], ids1[j + 1] = ids1[j + 1], ids1[j]

                       elif planstosort[j] == planstosort[j + 1]:
                           if data[j + 1] == "unlimited":
                               ids1[j], ids1[j + 1] = ids1[j + 1], ids1[j]

                               planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                               one_month[j], one_month[j + 1] = one_month[j + 1], one_month[j]
                   else:
                       ids1[j], ids1[j + 1] = ids1[j + 1], ids1[j]

                       planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                       one_month[j], one_month[j + 1] = one_month[j + 1], one_month[j]
           #print(one_month, "one")
           #print(ids1)

           # 3 months

           planstosort = []
           for i in range(0, len(plans)):
               planstosort.append(plans[i].plan)
           #print(planstosort, "3")
           data = []
           for i in range(0, len(plans)):
               data.append(plans[i].data)
           #print("data3", data)
           for i in range(0, len(three_month) - 1):

               for j in range(0, len(three_month) - i - 1):

                   if three_month[j] < three_month[j + 1]:

                       pass
                   elif three_month[j] == three_month[j + 1]:
                       if planstosort[j] < planstosort[j + 1]:
                           planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                           three_month[j], three_month[j + 1] = three_month[j + 1], three_month[j]
                           ids3[j], ids3[j + 1] = ids3[j + 1], ids3[j]

                       elif planstosort[j] == planstosort[j + 1]:
                           if data[j + 1] == "unlimited":
                               ids3[j], ids3[j + 1] = ids3[j + 1], ids3[j]

                               planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                               three_month[j], three_month[j + 1] = three_month[j + 1], three_month[j]


                   else:
                       ids3[j], ids3[j + 1] = ids3[j + 1], ids3[j]

                       planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                       three_month[j], three_month[j + 1] = three_month[j + 1], three_month[j]
           #print(three_month, "3")
           #print(ids3, "3")
           # 6 months
           planstosort = []
           for i in range(0, len(plans)):
               planstosort.append(plans[i].plan)
           #print(planstosort, "6")
           data = []
           for i in range(0, len(plans)):
               data.append(plans[i].data)
           #print("data6", data)

           for i in range(0, len(six_months) - 1):

               for j in range(0, len(six_months) - i - 1):

                   if six_months[j] < six_months[j + 1]:

                       pass
                   elif six_months[j] == six_months[j + 1]:
                       if planstosort[j] < planstosort[j + 1]:
                           planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                           six_months[j], six_months[j + 1] = six_months[j + 1], six_months[j]
                           ids6[j], ids6[j + 1] = ids6[j + 1], ids6[j]

                       elif planstosort[j] == planstosort[j + 1]:
                           if data[j + 1] == "unlimited":
                               ids6[j], ids6[j + 1] = ids6[j + 1], ids6[j]

                               planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                               six_months[j], six_months[j + 1] = six_months[j + 1], six_months[j]
                   else:
                       ids6[j], ids6[j + 1] = ids6[j + 1], ids6[j]

                       planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                       six_months[j], six_months[j + 1] = six_months[j + 1], six_months[j]

           #print(six_months, "6")
           #print(ids6, "6")

           # 12 months
           planstosort = []
           for i in range(0, len(plans)):
               planstosort.append(plans[i].plan)

           #print(planstosort, "12")
           data = []
           for i in range(0, len(plans)):
               data.append(plans[i].data)
           #print("data12", data)

           for i in range(0, len(yearly) - 1):

               for j in range(0, len(yearly) - i - 1):

                   if yearly[j] < yearly[j + 1]:

                       pass
                   elif yearly[j] == yearly[j + 1]:
                       if planstosort[j] < planstosort[j + 1]:
                           planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                           yearly[j], yearly[j + 1] = yearly[j + 1], yearly[j]
                           ids12[j], ids12[j + 1] = ids12[j + 1], ids12[j]

                       elif planstosort[j] == planstosort[j + 1]:
                           if data[j + 1] == "unlimited":
                               ids12[j], ids12[j + 1] = ids12[j + 1], ids12[j]

                               planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                               yearly[j], yearly[j + 1] = yearly[j + 1], yearly[j]
                   else:
                       ids12[j], ids12[j + 1] = ids12[j + 1], ids12[j]

                       planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                       yearly[j], yearly[j + 1] = yearly[j + 1], yearly[j]

           #print(yearly, "12")
           #print(ids12, "12")
           serviceprovider_id = []
           for i in range(0, len(one_month)):
               x = Plan.objects.get(id=ids1[i])
               #print(x.serviceprovider.id)
               serviceprovider_id.append(Serviceprovider.objects.get(id=x.serviceprovider.id))
           serviceprovider_plan = []
           plan_d = []
           data_d = []

           for i in range(0, len(one_month)):
               # serviceprovider_id.append(Serviceprovider.objects.get(id=ids1[i].serviceprovider))
               serviceprovider_plan.append(serviceprovider_id[i].service_providers_name)
               x = Plan.objects.get(id=ids1[i])
               plan_d.append(x.plan)
               data_d.append(x.data)
           z = zip(one_month, serviceprovider_id, serviceprovider_plan, plan_d, data_d, ids1)

           return render(request, 'serviceproviders/sorted_plans.html', {'z': z, 'yearly': yearly,
                                                                         'ids12': ids12, 'ids6': ids6,
                                                                         'ids3': ids3,"kiti_mahine":1,
                                                                         "affordable":"affordable",
                                                                         "sorted_name": sorted_name,
                                                                         'six_months': six_months,
                                                                         'three_month': three_month})
       else:
           pass
           #print("xxxxxxxxxxxxxxxxxxx")
###############################################################################3
       sorted_name1 = request.POST.getlist('sorted_name1')

       if len(sorted_name1)>0:
           sorted_name = request.POST.getlist('sorted_name1')

           plans = Plan.objects.filter(serviceprovider_id__in=sorted_name)

           """            except:
                   #print("except")
                   pass"""
           #print("XXXXXXXXXXXXXXX", plans)

           #print("all", plans[0].id)
           plan_list = []
           for i in range(0, len(plans)):
               plan_list.append(plans[i].id)
           #print(plan_list)
           one_month = []
           planstosort = []
           three_month = []
           six_months = []
           yearly = []
           data = []
           ids1 = []
           ids3 = []
           ids6 = []
           ids12 = []

           for i in range(0, len(plans)):
               ids1.append(plans[i].id)
               ids3.append(plans[i].id)
               ids6.append(plans[i].id)
               ids12.append(plans[i].id)
           for i in range(0, len(plans)):
               one_month.append(plans[i].monthly_rate)
           for i in range(0, len(plans)):
               planstosort.append(plans[i].plan)
           #print(planstosort, "xxx")
           for i in range(0, len(plans)):
               three_month.append(plans[i].tree_months)
           for i in range(0, len(plans)):
               six_months.append(plans[i].six_months)
           for i in range(0, len(plans)):
               yearly.append(plans[i].yearly)
           for i in range(0, len(plans)):
               data.append(plans[i].data)
           # onemonth
           #print(planstosort, "1")
           #print("data1", data)

           for i in range(0, len(one_month) - 1):

               for j in range(0, len(one_month) - i - 1):
                   print(planstosort[j],planstosort[j+1])
                   if planstosort[j] > planstosort[j + 1]:

                       pass
                   elif planstosort[j] == planstosort[j + 1]:
                       if one_month[j] > one_month[j + 1]:
                           planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                           one_month[j], one_month[j + 1] = one_month[j + 1], one_month[j]
                           ids1[j], ids1[j + 1] = ids1[j + 1], ids1[j]

                       elif one_month[j] == one_month[j + 1]:
                           if data[j + 1] == "unlimited":
                               ids1[j], ids1[j + 1] = ids1[j + 1], ids1[j]

                               #planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                               one_month[j], one_month[j + 1] = one_month[j + 1], one_month[j]
                   else:
                       print("before idd", ids1[j], ids1[j + 1])
                       ids1[j], ids1[j + 1] = ids1[j + 1], ids1[j]
                       print("swapped", planstosort[j], planstosort[j + 1])
                       print("swapped idd", ids1[j], ids1[j + 1] )
                       planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                       one_month[j], one_month[j + 1] = one_month[j + 1], one_month[j]
           #print(one_month, "one")
           print(ids1)

           # 3 months

           planstosort = []
           for i in range(0, len(plans)):
               planstosort.append(plans[i].plan)
           #print(planstosort, "3")
           data = []
           for i in range(0, len(plans)):
               data.append(plans[i].data)
           #print("data3", data)
           for i in range(0, len(three_month) - 1):

               for j in range(0, len(three_month) - i - 1):

                   if planstosort[j] > planstosort[j + 1]:

                       pass
                   elif planstosort[j] == planstosort[j + 1]:
                       if three_month[j] > three_month[j + 1]:
                           planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                           three_month[j], three_month[j + 1] = three_month[j + 1], three_month[j]
                           ids3[j], ids3[j + 1] = ids3[j + 1], ids3[j]

                       elif three_month[j] == three_month[j + 1]:
                           if data[j + 1] == "unlimited":
                               ids3[j], ids3[j + 1] = ids3[j + 1], ids3[j]

                               planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                               three_month[j], three_month[j + 1] = three_month[j + 1], three_month[j]


                   else:
                       ids3[j], ids3[j + 1] = ids3[j + 1], ids3[j]
                       print("swapped", planstosort[j], planstosort[j + 1])

                       planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                       three_month[j], three_month[j + 1] = three_month[j + 1], three_month[j]
           #print(three_month, "3")
           #print(ids3, "3")
           # 6 months
           planstosort = []
           for i in range(0, len(plans)):
               planstosort.append(plans[i].plan)
           #print(planstosort, "6")
           data = []
           for i in range(0, len(plans)):
               data.append(plans[i].data)
           #print("data6", data)

           for i in range(0, len(six_months) - 1):

               for j in range(0, len(six_months) - i - 1):

                   if planstosort[j] > planstosort[j + 1]:

                       pass
                   elif planstosort[j] == planstosort[j + 1]:
                       if six_months[j] > six_months[j + 1]:
                           planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                           six_months[j], six_months[j + 1] = six_months[j + 1], six_months[j]
                           ids6[j], ids6[j + 1] = ids6[j + 1], ids6[j]

                       elif six_months[j] == six_months[j + 1]:
                           if data[j + 1] == "unlimited":
                               ids6[j], ids6[j + 1] = ids6[j + 1], ids6[j]

                               planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                               six_months[j], six_months[j + 1] = six_months[j + 1], six_months[j]
                   else:
                       ids6[j], ids6[j + 1] = ids6[j + 1], ids6[j]
                       print("swapped",planstosort[j],planstosort[j + 1])
                       planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                       six_months[j], six_months[j + 1] = six_months[j + 1], six_months[j]

           #print(six_months, "6")
           #print(ids6, "6")

           # 12 months
           planstosort = []
           for i in range(0, len(plans)):
               planstosort.append(plans[i].plan)

           #print(planstosort, "12")
           data = []
           for i in range(0, len(plans)):
               data.append(plans[i].data)
           #print("data12", data)

           for i in range(0, len(yearly) - 1):

               for j in range(0, len(yearly) - i - 1):

                   if planstosort[j] > planstosort[j + 1]:

                       pass
                   elif planstosort[j] == planstosort[j + 1]:
                       if yearly[j] > yearly[j + 1]:
                           planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                           yearly[j], yearly[j + 1] = yearly[j + 1], yearly[j]
                           ids12[j], ids12[j + 1] = ids12[j + 1], ids12[j]

                       elif yearly[j] == yearly[j + 1]:
                           if data[j + 1] == "unlimited":
                               ids12[j], ids12[j + 1] = ids12[j + 1], ids12[j]

                               planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                               yearly[j], yearly[j + 1] = yearly[j + 1], yearly[j]
                   else:
                       ids12[j], ids12[j + 1] = ids12[j + 1], ids12[j]

                       planstosort[j], planstosort[j + 1] = planstosort[j + 1], planstosort[j]
                       yearly[j], yearly[j + 1] = yearly[j + 1], yearly[j]

           #print(yearly, "12")
           #print(ids12, "12")
           serviceprovider_id = []
           for i in range(0, len(one_month)):
               x = Plan.objects.get(id=ids1[i])
               #print(x.serviceprovider.id)
               serviceprovider_id.append(Serviceprovider.objects.get(id=x.serviceprovider.id))
           serviceprovider_plan = []
           plan_d = []
           data_d = []
           for i in range(0, len(one_month)):
               # serviceprovider_id.append(Serviceprovider.objects.get(id=ids1[i].serviceprovider))
               serviceprovider_plan.append(serviceprovider_id[i].service_providers_name)
               x = Plan.objects.get(id=ids1[i])
               plan_d.append(x.plan)
               data_d.append(x.data)

           z = zip(one_month, serviceprovider_id, serviceprovider_plan, plan_d, data_d, ids1)
           #print("77777777777777777777777777777777777777",plan_d)

           return render(request, 'serviceproviders/sorted_plans.html', {'z': z, "speedy":"speedy",'yearly': yearly,
                                                                         'ids12': ids12,
                                                                         'ids6': ids6,

                                                                         'ids3': ids3,"kiti_mahine":1,
                                                                         "sorted_name": sorted_name,
                                                                         'six_months': six_months,
                                                                         'three_month': three_month})

       else:
           pass









##############################################################
    else:
        kitne= request.GET["kitne months ka"]
        if kitne=="three_months":
            sorted_name = request.GET.getlist('sorted_name')

            three_month = request.GET.getlist('three_month')
            ids3=request.GET.getlist('ids3')
            six_months = request.GET.getlist('six_months')
            ids6 = request.GET.getlist('ids6')
            yearly = request.GET.getlist('yearly')
            ids12 = request.GET.getlist('ids12')
            #print(three_month,ids3)
            serviceprovider_id = []
            for i in range(0, len(three_month)):
                x = Plan.objects.get(id=ids3[i])
                #print(x.serviceprovider.id)
                serviceprovider_id.append(Serviceprovider.objects.get(id=x.serviceprovider.id))
            serviceprovider_plan = []
            plan_d = []
            data_d = []

            for i in range(0, len(three_month)):
                serviceprovider_plan.append(serviceprovider_id[i].service_providers_name)
                x = Plan.objects.get(id=ids3[i])
                plan_d.append(x.plan)
                data_d.append(x.data)
            z = zip(three_month, serviceprovider_id, serviceprovider_plan, plan_d, data_d, ids3)

            return render(request, 'serviceproviders/sorted_plans.html', {'z': z, 'yearly': yearly,
                                                                          'ids12': ids12, 'ids6': ids6,
                                                                          'ids3': ids3,"kiti_mahine":3,
                                                                          "sorted_name": sorted_name,
                                                                          "affordable": "affordable",
                                                                          'six_months': six_months,
                                                                          'three_month': three_month})

        elif kitne=="six_months":
            sorted_name = request.GET.getlist('sorted_name')

            three_month = request.GET.getlist('three_month')
            ids3 = request.GET.getlist('ids3')
            six_months = request.GET.getlist('six_months')
            ids6 = request.GET.getlist('ids6')
            yearly = request.GET.getlist('yearly')
            ids12 = request.GET.getlist('ids12')
            #print(six_months, ids6)
            serviceprovider_id = []
            for i in range(0, len(six_months)):
                x = Plan.objects.get(id=ids6[i])
                #print(x.serviceprovider.id)
                serviceprovider_id.append(Serviceprovider.objects.get(id=x.serviceprovider.id))
            serviceprovider_plan = []
            plan_d = []
            data_d = []

            for i in range(0, len(six_months)):
                serviceprovider_plan.append(serviceprovider_id[i].service_providers_name)
                x = Plan.objects.get(id=ids6[i])
                plan_d.append(x.plan)
                data_d.append(x.data)
            z = zip(six_months, serviceprovider_id, serviceprovider_plan, plan_d, data_d, ids6)

            return render(request, 'serviceproviders/sorted_plans.html', {'z': z, 'yearly': yearly,
                                                                          'ids12': ids12, 'ids6': ids6,
                                                                          'ids3': ids3,"kiti_mahine":6,
                                                                          "sorted_name": sorted_name,
                                                                          "affordable": "affordable",
                                                                          'six_months': six_months,
                                                                          'three_month': three_month})

        elif kitne=="yearly":
            sorted_name = request.GET.getlist('sorted_name')

            three_month = request.GET.getlist('three_month')
            ids3 = request.GET.getlist('ids3')
            six_months = request.GET.getlist('six_months')
            ids6 = request.GET.getlist('ids6')
            yearly = request.GET.getlist('yearly')
            ids12 = request.GET.getlist('ids12')
            #print(yearly, ids12)
            serviceprovider_id = []
            for i in range(0, len(yearly)):
                x = Plan.objects.get(id=ids12[i])
                #print(x.serviceprovider.id)
                serviceprovider_id.append(Serviceprovider.objects.get(id=x.serviceprovider.id))
            serviceprovider_plan = []
            plan_d = []
            data_d = []

            for i in range(0, len(yearly)):
                serviceprovider_plan.append(serviceprovider_id[i].service_providers_name)
                x = Plan.objects.get(id=ids12[i])
                plan_d.append(x.plan)
                data_d.append(x.data)
            z = zip(yearly, serviceprovider_id, serviceprovider_plan, plan_d, data_d, ids12)

            return render(request, 'serviceproviders/sorted_plans.html', {'z': z, 'yearly': yearly,
                                                                          'ids12': ids12, 'ids6': ids6,
                                                                          'ids3': ids3,"kiti_mahine":12,
                                                                          "sorted_name": sorted_name,
                                                                          "affordable": "affordable",

                                                                          'six_months': six_months,
                                                                          'three_month': three_month})

        elif kitne=="three_months_speedy":
            sorted_name = request.GET.getlist('sorted_name')

            three_month = request.GET.getlist('three_month')
            ids3 = request.GET.getlist('ids3')
            six_months = request.GET.getlist('six_months')
            ids6 = request.GET.getlist('ids6')
            yearly = request.GET.getlist('yearly')
            ids12 = request.GET.getlist('ids12')
            #print(three_month, ids3)
            serviceprovider_id = []
            for i in range(0, len(three_month)):
                x = Plan.objects.get(id=ids3[i])
                #print(x.serviceprovider.id)
                serviceprovider_id.append(Serviceprovider.objects.get(id=x.serviceprovider.id))
            serviceprovider_plan = []
            plan_d = []
            data_d = []

            for i in range(0, len(three_month)):
                serviceprovider_plan.append(serviceprovider_id[i].service_providers_name)
                x = Plan.objects.get(id=ids3[i])
                plan_d.append(x.plan)
                data_d.append(x.data)
            z = zip(three_month, serviceprovider_id, serviceprovider_plan, plan_d, data_d, ids3)

            return render(request, 'serviceproviders/sorted_plans.html', {'z': z, 'yearly': yearly,
                                                                          'ids12': ids12, 'ids6': ids6,
                                                                          "speedy": "speedy",

                                                                          'ids3': ids3,"kiti_mahine":3,
                                                                          "sorted_name": sorted_name,

                                                                          'six_months': six_months,
                                                                          'three_month': three_month})

        elif kitne=="six_months_speedy":
            sorted_name = request.GET.getlist('sorted_name')

            three_month = request.GET.getlist('three_month')
            ids3 = request.GET.getlist('ids3')
            six_months = request.GET.getlist('six_months')
            ids6 = request.GET.getlist('ids6')
            yearly = request.GET.getlist('yearly')
            ids12 = request.GET.getlist('ids12')
            #print(six_months, ids6)
            serviceprovider_id = []
            for i in range(0, len(six_months)):
                x = Plan.objects.get(id=ids6[i])
                #print(x.serviceprovider.id)
                serviceprovider_id.append(Serviceprovider.objects.get(id=x.serviceprovider.id))
            serviceprovider_plan = []
            plan_d = []
            data_d = []

            for i in range(0, len(six_months)):
                serviceprovider_plan.append(serviceprovider_id[i].service_providers_name)
                x = Plan.objects.get(id=ids6[i])
                plan_d.append(x.plan)
                data_d.append(x.data)
            z = zip(six_months, serviceprovider_id, serviceprovider_plan, plan_d, data_d, ids6)

            return render(request, 'serviceproviders/sorted_plans.html', {'z': z, 'yearly': yearly,
                                                                          'ids12': ids12, 'ids6': ids6,
                                                                            "speedy":"speedy",
                                                                          'ids3': ids3,"kiti_mahine":6,
                                                                          "sorted_name": sorted_name,

                                                                          'six_months': six_months,
                                                                          'three_month': three_month})
        else:
            sorted_name = request.GET.getlist('sorted_name')

            three_month = request.GET.getlist('three_month')
            ids3 = request.GET.getlist('ids3')
            six_months = request.GET.getlist('six_months')
            ids6 = request.GET.getlist('ids6')
            yearly = request.GET.getlist('yearly')
            ids12 = request.GET.getlist('ids12')
            #print(yearly, ids12)
            serviceprovider_id = []
            for i in range(0, len(yearly)):
                x = Plan.objects.get(id=ids12[i])
                #print(x.serviceprovider.id)
                serviceprovider_id.append(Serviceprovider.objects.get(id=x.serviceprovider.id))
            serviceprovider_plan = []
            plan_d = []
            data_d = []

            for i in range(0, len(yearly)):
                serviceprovider_plan.append(serviceprovider_id[i].service_providers_name)
                x = Plan.objects.get(id=ids12[i])
                plan_d.append(x.plan)
                data_d.append(x.data)
            z = zip(yearly, serviceprovider_id, serviceprovider_plan, plan_d, data_d, ids12)

            return render(request, 'serviceproviders/sorted_plans.html', {'z': z, 'yearly': yearly,
                                                                          'ids12': ids12, 'ids6': ids6,
                                                                          "speedy": "speedy",

                                                                          'ids3': ids3,"kiti_mahine":12,
                                                                          "sorted_name": sorted_name,

                                                                          'six_months': six_months,
                                                                          'three_month': three_month})

@login_required()
def createplans(request):
    if request.method=="GET":
        forms=Planss()

        return render(request,'serviceproviders/createplan.html',{'forms':forms})
    else:
        forms=Planss(request.POST)
        if forms.is_valid():
            p=Plan()
            p.plan=request.POST['plan']
            p.monthly_rate=request.POST['monthly_rate']
            p.tree_months=request.POST['tree_months']
            p.six_months=request.POST['six_months']
            p.yearly=request.POST['yearly']
            p.data=request.POST['data']

            service=request.user
            p.serviceprovider=service.serviceprovider

            p.save()
        return redirect("serviceproviders:litap")
@login_required()
def serviceproviderupdate(request):
    if request.method=="GET":

        try:
            instance = Serviceprovider.objects.get(user=request.user)
            form = serviceproviderupdateform(instance=instance)
            s=Serviceprovider.objects.get(user=request.user)
        except:
            return redirect("users:home")
        #print(s)
        plan=Plan.objects.filter(serviceprovider=s)
        #print(plan)
        users=[]
        for i in range(0,len(plan)):
            li=UserInfo.objects.filter(plan_id=plan[i])
            for j in range(0,len(li)):
                users.append(li[j])
        names=[]
        plans=[]
        rs=[]
        months=[]
        last_recharge=[]
        expire_date=[]
        days=[]
        no=[]
        id=[]

        for i in range(0,len(users)):
            names.append(users[i].name)
            no.append(users[i].phone)
            id.append(users[i].id)
            last_recharge.append(users[i].last_recharge)
            months.append(users[i].months)
            plan_id=users[i].plan
            plans.append(plan_id.plan)
            kiti_mahine1=users[i].months
            if kiti_mahine1 == 1:
                plan_months = 1
                plan_rate = plan_id.monthly_rate
                plan_days = 30
            elif kiti_mahine1 == 3:
                plan_months = 3
                plan_rate = plan_id.tree_months
                plan_days = 90

            elif kiti_mahine1 == 6:
                plan_months = 6
                plan_rate = plan_id.six_months
                plan_days = 180

            else:
                plan_months = 12
                plan_days = 360
                plan_rate = plan_id.yearly
            rs.append(plan_rate)
            expire_date1=datetime.timedelta(days=plan_days)
            #print(expire_date1)
            today = datetime.date.today()

            #print(last_recharge[i] + expire_date1)
            expire_date.append(last_recharge[i] + expire_date1)
            #print("today", today, type(today))
            #print("expire_date", expire_date, type(expire_date))
            expire_date[i]= expire_date[i].date()
            days.append((expire_date[i] - today).days)
        #print(id,"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        z=zip(no,id,names,plans,rs,months,last_recharge,expire_date,days)

        return render(request,"serviceproviders/serviceprovider_form.html",{'z':z,'form':form,"users":users})

    else:
        print("0000000000000000000000000000000000000000000000000000")
        instance=Serviceprovider.objects.get(user=request.user)
        form=serviceproviderupdateform(request.POST)
        if form.is_valid():
            #print("tttttttttttttttttttttttttttt")
            s=Serviceprovider.objects.get(user=request.user)
            s.service_providers_name=request.POST['service_providers_name']
            s.service_providers_address=request.POST['service_providers_address']
            s.website=request.POST['website']
            s.save()

            form.save()
        s=Serviceprovider.objects.get(user=request.user)
        #print(s)
        plan=Plan.objects.filter(serviceprovider=s)
        #print(plan)
        users=[]
        for i in range(0,len(plan)):
            li=UserInfo.objects.filter(plan_id=plan[i])
            for j in range(0,len(li)):
                users.append(li[j])
        names=[]
        plans=[]
        rs=[]
        months=[]
        last_recharge=[]
        expire_date=[]
        days=[]


        for i in range(0,len(users)):
            names.append(users[i].name)

            last_recharge.append(users[i].last_recharge)
            months.append(users[i].months)
            plan_id=users[i].plan
            plans.append(plan_id.plan)
            kiti_mahine1=users[i].months
            if kiti_mahine1 == 1:
                plan_months = 1
                plan_rate = plan_id.monthly_rate
                plan_days = 30
            elif kiti_mahine1 == 3:
                plan_months = 3
                plan_rate = plan_id.tree_months
                plan_days = 90

            elif kiti_mahine1 == 6:
                plan_months = 6
                plan_rate = plan_id.six_months
                plan_days = 180

            else:
                plan_months = 12
                plan_days = 360
                plan_rate = plan_id.yearly
            rs.append(plan_rate)
            expire_date1=datetime.timedelta(days=plan_days)
            #print(expire_date1)
            today = datetime.date.today()

            #print(last_recharge[i] + expire_date1)
            expire_date.append(last_recharge[i] + expire_date1)
            #print("today", today, type(today))
            #print("expire_date", expire_date, type(expire_date))
            expire_date[i]= expire_date[i].date()
            days.append(expire_date[i] - today)

        z=zip(names,plans,rs,months,last_recharge,expire_date,days)

        return render(request,"serviceproviders/serviceprovider_form.html",{'z':z,'form':form,"users":users})


"""class serviceproviderupdate(UpdateView):
    model=Serviceprovider
    fields = ['service_providers_name','service_providers_address',
              'website']

    def get_object(self):
        return Serviceprovider.objects.get(user=self.request.user)"""



#after google login this view is used
@login_required()
def serviceproviderlogin(request):
    #print("serviceproviderlogin",request.user)
    if request.method=="GET":
        try:
            u=UserInfo.objects.get(user=request.user)
            #print("user try",u)

            if u.add=="default":

                return redirect("/verify/")

            else:
                pass

        except:
            #print("user except")
            u=UserInfo()
            u.user=request.user
            s = SocialAccount.objects.filter(user_id=request.user.id, provider='google')
            u.name=s[0].extra_data['name']
            u.email=s[0].extra_data['email']
            x = settings.EMAIL_HOST
            message ="thanks for login into LITAP"
            send_mail(
                'LITAP :)',
                message,
                x,
                [u.email],
            )
            u.save()
            return redirect("/verify/")
        try:
            s=Serviceprovider.objects.get(user=request.user)
            u = UserInfo.objects.get(user=request.user)
            s.service_provider_phone=u.phone
            s.service_provider_email=u.email
            s.service_provider=u.name
            s.save()
        except:
            pass


        form=login()
        return render(request,'serviceproviders/login1.html',{'form':form})

    else:

        s=Serviceprovider.objects.get(user=request.user)
        password=request.POST["serviceproviderpassword"]
        print(password)
        if s.login_password==password:
            try:
                s=Status.objects.get(user=request.user)
            except:
                s=Status()
            s.status=True

            return redirect("serviceproviders:update")
        else:
            form = login()
            return render(request, 'serviceproviders/login1.html', {'form': form,
                                                                    "login_error": "incorrect password please login again"})










def detail(request,pk):
    s=Serviceprovider.objects.get(pk=pk)
    detailed_name=s.service_providers_name
    detailed_addres=s.service_providers_address
    detailed_ratings=s.rating
    detailed_website=s.website
    rating=float(s.rating)*20
    args = {'detailed_name': detailed_name, 'detailed_addres': detailed_addres, 'detailed_ratings': detailed_ratings,
            'detailed_website': detailed_website,'rating':rating}
    if True:
    #try:
        plans = Plan.objects.filter(serviceprovider_id=s)
        pid = []
        p_onemonth=[]
        p_six_months=[]
        p_three_months=[]
        p_yearly=[]
        p_data=[]
        p_plan=[]
        for i in range(0, len(plans)):
            pid.append(plans[i].id)
            p_onemonth.append(plans[i].monthly_rate)
            p_six_months.append(plans[i].six_months)
            p_three_months.append(plans[i].tree_months)
            p_yearly.append(plans[i].yearly)
            p_data.append(plans[i].data)
            p_plan.append(plans[i].plan)
        """args["pid"]=pid
        args["p_onemonth"]=p_onemonth
        args["p_six_months"] = p_six_months
        args["p_three_months"] = p_three_months
        args["p_yearly"] = p_yearly
        args["p_data"] = p_data
        args["p_plan"] = p_plan"""
        print("ppppppppppppppppppppppppppppppppppppppppppppppccccccccc",pid)
        z=zip(pid,p_onemonth,p_six_months,p_three_months,p_yearly,p_data,p_plan)
        args['z']=z
        z1=zip(pid,p_onemonth,p_six_months,p_three_months,p_yearly,p_data,p_plan)
        args['z1']=z1
        z2 = zip(pid, p_onemonth, p_six_months, p_three_months, p_yearly, p_data, p_plan)
        args['z2'] = z2
        z3 = zip(pid, p_onemonth, p_six_months, p_three_months, p_yearly, p_data, p_plan)
        args['z3'] = z3
        try:
            s=Status.objects.get(user=request.user)
            if s.status=="True":
                args["status"]="serviceprovider"
        except:
            pass











    else:
    #except:

        args["no"]="no plans"


    return render(request,'serviceproviders/details.html',args)


class List(generic.ListView):
    def get(self,request):
        try:
            u=UserInfo.objects.get(user=request.user)
            #print(u," uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
            if u is None:
                redirect("serviceproviders:serviceproviderlogin")
        except:
            pass
        query=request.GET.get("q")
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        s=Serviceprovider.objects.all()
        if query:
            s=s.filter(service_providers_name__icontains=query)
            sorted_website = []
            sorted_phone=[]
            sorted_rating = []
            sorted_name = []
            sorted_address = []
            sorted_photo = []
            sorted_id=[]
            for i in range(0,len(s)):
                sorted_website.append(s[i].service_providers_name)
                sorted_phone.append(s[i].service_providers_phone)
                sorted_rating.append(s[i].rating)
                sorted_name.append(s[i].service_provider)
                sorted_address.append(s[i].service_providers_address)
                sorted_photo.append(s[i].photo_reference)
                sorted_id.append(s[i].id)
                z = zip(sorted_name, sorted_address, sorted_rating, sorted_photo, sorted_website,sorted_id)
                return render(request,'serviceproviders/list1.html',{'z':z,'message':"v"})

        form=Add()
        args={'form':form,'post':"post"}
        return render(request,'serviceproviders/list.html',args)

    def post(self,request):

        form=Add(request.POST)

        try:
            u=UserInfo.objects.get(user=request.user)
            #print(u," uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
            if u is None:
                redirect("serviceproviders:serviceproviderlogin")
        except:
            pass
        if form.is_valid():
            add=form.cleaned_data['address']
#building geocode api and retrieving lat lang
            url1="https://maps.googleapis.com/maps/api/geocode/json?"
            url2=url1 + urllib.parse.urlencode({'address': add})
            url3="&key=AIzaSyBZJTGBhR1FLTV_pw9ybTkFKH-xvgEz4es"
            ke = "AIzaSyBZJTGBhR1FLTV_pw9ybTkFKH-xvgEz4es"

            url=url2 + url3
            geocode=requests.get(url).json()

            try:
                lat = geocode["results"][0]["geometry"]["location"]["lat"]
                lng = geocode["results"][0]["geometry"]["location"]["lng"]
            except:
                return render(request, 'serviceproviders/list.html', {'form': form,
                                                                  'error': "no isp found nearby you"})
# building nearby api and getting name , isopen,placeid,ratings,address(viciity),photo ref

            url1="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
            url2=str(lat)
            url4=","
            url5=str(lng)
            url6="&radius=5000&keyword=internet+service+provider&key=AIzaSyBZJTGBhR1FLTV_pw9ybTkFKH-xvgEz4es"
            url=url1+url2+url4+url5+url6
            nearby=requests.get(url).json()
#AIzaSyC6lLodUwpgrNMhtsVVA-FJ3GaBkLxzcMU

# building placeid api and getting phone no website
            sorted_website = []
            sorted_phone=[]
            sorted_rating = []
            sorted_name = []
            sorted_address = []
            sorted_opennow = []
            sorted_photo = []
            sorted_placeid = []
            sorted_id=[]
            length = len(nearby["results"])
            if length==0:
                return render(request, 'serviceproviders/list.html', {'form':form,
                                                                      'error':"no isp found nearby you"})

            for i in range(0, length, 1):
                url1 = "https://maps.googleapis.com/maps/api/place/details/json?placeid="
                url2 = nearby["results"][i]["place_id"]
                url3 = "&key=AIzaSyBZJTGBhR1FLTV_pw9ybTkFKH-xvgEz4es"
                url = url1 + url2 + url3
                sort_ke_liye = requests.get(url).json()
                try:
                    sorted_phone.append(sort_ke_liye["result"]["formatted_phone_number"])
                except:
                    sorted_phone.append("not available")
                try:
                    sorted_website.append(sort_ke_liye["result"]["website"])
                except:
                    sorted_website.append("not available")

            for k in range(0,length,1):
                x=1
                list = Serviceprovider.objects.all()

                for i in list:
                     if i.service_providers_name == nearby["results"][k]["name"]:
                        x=0
                        break
                     else:
                        pass
            #to generate sortedphone and sortedwebsite


                if x==1:
                    s=Serviceprovider()
                    sorted_id.append(s)
                    s.service_providers_name=nearby["results"][k]["name"]
                    s.service_providers_address=nearby["results"][k]["vicinity"]

                    try:
                        s.rating = nearby["results"][k]["rating"]
                        #s.open_now = nearby["results"][k]["opening_hours"]["open_now"]
                        s.photo_reference=nearby["results"][k]["photos"][0]["photo_reference"]
                    except:
                        pass
                    s.place_id=nearby["results"][k]["place_id"]
                    # building placeid api and getting phone no website

                    url1="https://maps.googleapis.com/maps/api/place/details/json?placeid="
                    url2=nearby["results"][k]["place_id"]
                    url3="&key=AIzaSyBZJTGBhR1FLTV_pw9ybTkFKH-xvgEz4es"
                    url=url1+url2+url3
                    placedetail=requests.get(url).json()
                    try:

                        s.service_providers_phone=placedetail["result"]["formatted_phone_number"]
                    except:
                        pass
                    try:
                        s.website=placedetail["result"]["website"]
                    except:
                        pass
                    s.save()

            for i in range(0,length,1):
                    sorted_name.append(nearby["results"][i]["name"])
                    sorted_address.append(nearby["results"][i]["vicinity"])
                    sorted_placeid.append(nearby["results"][i]["place_id"])
                    try:

                        sorted_opennow.append(nearby["results"][i]["opening_hours"]["open_now"])
                    except:
                        sorted_opennow.append("not available")
                        pass
                    try:
                        sorted_photo.append(nearby["results"][i]["photos"][0]["photo_reference"])
                    except:
                        sorted_photo.append("not available")

            for i in range(0, length, 1):

                    try:
                        x = nearby["results"][i]["rating"]
                        sorted_rating.append(x)

                    except:
                        sorted_rating.append(0)

            sorted_index = []
            for i in range(0, length, 1):
                    sorted_index.append(i)

            for i in range(length - 2, -1, -1):
                    for j in range(0, i + 1, 1):
                        if sorted_rating[j] < sorted_rating[j + 1]:
                            temp = sorted_rating[j]
                            sorted_rating[j] = sorted_rating[j + 1]
                            sorted_rating[j + 1] = temp
                            temp = sorted_index[j]
                            sorted_index[j] = sorted_index[j + 1]
                            sorted_index[j + 1] = temp
                            temp = sorted_name[j]
                            sorted_name[j] = sorted_name[j + 1]
                            sorted_name[j + 1] = temp
                            temp = sorted_address[j]
                            sorted_address[j] = sorted_address[j + 1]
                            sorted_address[j + 1] = temp
                            temp = sorted_placeid[j]
                            sorted_placeid[j] = sorted_placeid[j + 1]
                            sorted_placeid[j + 1] = temp
                            temp = sorted_opennow[j]
                            sorted_opennow[j] = sorted_opennow[j + 1]
                            sorted_opennow[j + 1] = temp



#zippind sorted_data
            #print("ixzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",sorted_name)
            sorted_id=[]
            for i in range(0,length,1):
                s=Serviceprovider.objects.get(service_providers_name=sorted_name[i])
                sorted_id.append(s.id)
            z=zip(sorted_name,sorted_address,sorted_rating,sorted_photo,sorted_opennow,sorted_website,sorted_id)


            args={'z':z,'rating':sorted_rating,'sorted_name':sorted_id,'ke':ke}



            return render(request,'serviceproviders/list1.html',args)



@login_required()
def plansconfirmed(request,pk):
    if request.method=="POST":

        try:
            u = UserInfo.objects.get(user=request.user)

        except:
            return redirect("serviceproviders:login")

        try:




            u=UserInfo.objects.get(user=request.user)
            if u.plan == None:
                print(u.plan)
                #print("try", int(pk), u)
            else:
                return redirect('users:home')
        except:
            pass

        #print(type(pk),"niiiiiiiiiiiiiiiiiiii")
        kiti_mahine1=request.POST["kiti_mahine"]
        #print("kiti",kiti_mahine1)
        u=UserInfo.objects.get(user=request.user)
        u.plan_id=int(pk)
        u.months=kiti_mahine1
        u.last_recharge=datetime.date.today()
        u.ratings_giver=False

        u.save()
        return redirect('users:home')
        plan_id=Plan.objects.get(id=int(pk))
        serviceprovider_id=plan_id.serviceprovider_id
        s=Serviceprovider.objects.get(id=serviceprovider_id)
        serviceprovider_name=s.service_providers_name
        plan=plan_id.plan
        plan_rate=plan_id.monthly_rate
        #print(type(kiti_mahine1))

        if kiti_mahine1=="1":
            plan_months=1
            plan_days=30
        elif kiti_mahine1=="3":
            plan_months = 3
            plan_days=90

        elif kiti_mahine1=="6":
            plan_months = 6
            plan_days=180

        else:
            plan_months=12
            plan_days=360
        #print("plan days",plan_days)
        expire_date=datetime.timedelta(days=plan_days)
        today=datetime.date.today()
        expire_date=today+expire_date
        #print("today",today)
        #print("expire_date",expire_date)


        day_remaining=expire_date-today
        #print("day_remaining",day_remaining)
        args={"expire_date":expire_date,"day_remaining":day_remaining,
              "serviceprovider_name":serviceprovider_name,"serviceprovider_id":serviceprovider_id,
                "plan":plan,"plan_rate":plan_rate
              }

        serviceproviderupdate(request)
        return render(request,'serviceproviders/plan_confirmation.html',args)
    else:
        try:
            u=UserInfo.objects.get(user=request.user)

        except:
            return redirect("serviceproviders:login")


        if True:

            u = UserInfo.objects.get(user=request.user)
            if u.plan == None:
                print(u.plan)
                #print("try", int(pk), u)
            else:
                return redirect('users:home')
        else:
            pass

        #print(type(pk), "niiiiiiiiiiiiiiiiiiii")
        kiti_mahine1 = request.POST["kiti_mahine"]
        #print("kiti", kiti_mahine1)
        u = UserInfo.objects.get(user=request.user)
        u.plan_id = int(pk)
        u.months = kiti_mahine1
        u.last_recharge = datetime.date.today()

        u.save()
        return redirect('users:home')
        plan_id = Plan.objects.get(id=int(pk))
        serviceprovider_id = plan_id.serviceprovider_id
        s = Serviceprovider.objects.get(id=serviceprovider_id)
        serviceprovider_name = s.service_providers_name
        plan = plan_id.plan
        plan_rate = plan_id.monthly_rate
        #print(type(kiti_mahine1))

        if kiti_mahine1 == "1":
            plan_months = 1
            plan_days = 30
        elif kiti_mahine1 == "3":
            plan_months = 3
            plan_days = 90

        elif kiti_mahine1 == "6":
            plan_months = 6
            plan_days = 180

        else:
            plan_months = 12
            plan_days = 360
        #print("plan days", plan_days)
        expire_date = datetime.timedelta(days=plan_days)
        today = datetime.date.today()
        expire_date = today + expire_date
        #print("today", today)
        #print("expire_date", expire_date)

        day_remaining = expire_date - today
        #print("day_remaining", day_remaining)
        args = {"expire_date": expire_date, "day_remaining": day_remaining,
                "serviceprovider_name": serviceprovider_name, "serviceprovider_id": serviceprovider_id,
                "plan": plan, "plan_rate": plan_rate
                }

        serviceproviderupdate(request)
        return render(request, 'serviceproviders/plan_confirmation.html', args)



@login_required()
def sendmail(request):

    if request.method=="POST":
        message=request.POST["message"]
        id=request.POST["id"]
        #print(id)
        u=UserInfo.objects.get(pk=int(id))
        plan=u.plan
        S=plan.serviceprovider.id
        to=u.email
        #print("to",to)
        s=Serviceprovider.objects.get(pk=S)
        name=s.service_providers_name
        #print("sssssss",s.service_providers_name)
        x = settings.EMAIL_HOST
        message+="" \
                 "" \
                 "                      -Regards "+name
        send_mail(
            'LITAP :)',
            message,
            x,
            [to],
        )

        return redirect("serviceproviders:update")


def exit(request):
    return redirect("serviceproviders:litap")

@login_required()
def serviceproviderplans(request):
    if request.method=="GET":
        s=Serviceprovider.objects.get(user=request.user)
        p=Plan.objects.filter(serviceprovider_id=s)
        id=[]
        plan=[]
        monthly=[]
        six=[]
        three=[]
        yearly=[]
        status=[]
        for i in range(0,len(p)):
            id.append(p[i].id)
            plan.append(p[i].plan)
            monthly.append(p[i].monthly_rate)
            six.append(p[i].six_months)
            three.append(p[i].tree_months)
            yearly.append(p[i].yearly)
            status.append(p[i].data)
        #print(yearly,"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",id)
        z=zip(id,plan,monthly,three,six,yearly,status)
        args={"z":z,"ramesh":"ramesh"}
        return render(request,"serviceproviders/serviceproviderplans.html",args)


@login_required()
def update(request):
    if request.method=="GET":
        id=request.GET.get("id")
        p = Plan.objects.get(pk=id)
        instance = p
        form = Planss(instance=instance)
        form = Planss(instance=instance)
        return render(request,"serviceproviders/serviceproviderplansupdate.html",{"form":form,"p":p.id})

    else:
        id=request.POST["id"]
        #print("ttttttttttttttttttttttttttttttttttttt",type(id),id)
        form=Planss(request.POST)
        if form.is_valid():
            p=Plan.objects.get(pk=int(id))

            p.plan=request.POST["plan"]
            p.monthly_rate=request.POST["monthly_rate"]
            p.tree_months=request.POST["tree_months"]
            p.six_months=request.POST["six_months"]
            p.yearly=request.POST["yearly"]
            p.data=request.POST["data"]
            p.save()
            return redirect("serviceproviders:serviceproviderplans")
        else:
            return render(request, "serviceproviders/serviceproviderplansupdate.html", {"form": form, "error": "error"})
