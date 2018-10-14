import csv
import dateutil
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from .models import *
from .utils import *
from .config import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import localtime
from django.template import loader
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from datetime import date
from decimal import Decimal
from django.db import connection
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core import serializers
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.decorators import login_required
import re
from django.core.files.storage import FileSystemStorage

import geocoder

import pytz
import socket

import re
import sys
import json
import logging
from django.core.cache import cache

@csrf_exempt
@xframe_options_exempt
def get_base_data(request):

    result={}
    exportClasses=[CarColor,Action,CarBrand, Funnysaying, Offense, Obstruction, EmailText]
    for theClass in exportClasses:
        result[theClass.getJsonName()] = list(map(theClass.getJsonMapping(), theClass.objects.all()))
    return JsonResponse(result, safe=False)


def getCsv(theClass):
    response=HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="'+theClass.getFilename()
    writer=csv.writer(response, quotechar='"',quoting=csv.QUOTE_ALL)
    writer.writerow(theClass.getHead())
    entries=theClass.objects.filter(deleted=False,hidden=False)
    for entry in entries:
        writer.writerow(entry.getRow())
    return response

def getOffice(postalcode):
    theClass=PublicAffairsOffice
    response=HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="'+postalcode+"_"+theClass.getFilename()
    writer=csv.writer(response)
    writer.writerow(theClass.getHead())
    entries=theClass.objects.filter(postalcode=postalcode)
    for entry in entries:
        writer.writerow(entry.getRow())
    return response

requestToCsvObject={"Color":CarColor, "Brand":CarBrand, "Action":Action, "OffenseType":Offense, "Office": PublicAffairsOffice, "Saying":Funnysaying, "Town": Town}

@csrf_exempt
@xframe_options_exempt
def get_markers(request):

    latmin = request.GET.get("latmin")
    latmax = request.GET.get("latmax")
    lngmin = request.GET.get("lngmin")
    lngmax = request.GET.get("lngmax")
    local_tz = pytz.timezone("Europe/Berlin")

    try:
        offensefilter = request.GET.get("offensefilter")
    except: 
        offensefilter=""

    lngmax = request.GET.get("lngmax")
    
    result={}

    offensewhere=""
    try:
        # avoiding sql injection
        if(offensefilter):
            strlist=offensefilter.split(",")
            filteroffenses=list(map(int, strlist))
            strlist=list(map(str, filteroffenses))
            joinlist = ",".join(strlist)
            if filteroffenses :
                offensewhere=" and r.offense_id in ("+ joinlist + ") "
    except Exception as e:
        print ("Mapping error: {}".format(e)) 

    result['comment']=offensewhere;

    try:
        untiltime = local_tz.localize(datetime.strptime(request.GET.get('untiltime'), '%Y-%m-%d %H:%M:%S'))
    except:
        try:
            untiltime = local_tz.localize(datetime.strptime(request.GET.get('untiltime'), '%Y-%m-%d'))
        except: 
            untiltime = datetime.now(pytz.utc)

    try:
        fromtime = local_tz.localize(datetime.strptime(request.GET.get('fromtime'), '%Y-%m-%d %H:%M:%S'))
    except :
        try:
            fromtime = local_tz.localize(datetime.strptime(request.GET.get('fromtime'), '%Y-%m-%d'))
        except: 
            fromtime = untiltime - dateutil.relativedelta.relativedelta(months=1)

    with connection.cursor() as cursor:
        cursor.execute("SELECT r.latitude as lat, r.longitude as lng, ifnull(b.name, '[verloren]') as name, r.tweet, r.date, offense_id FROM wegeheld_report r "
        + " left join wegeheld_car c on c.id = r.car_id " 
        + " left join wegeheld_carbrand b on b.id = c.brand_id "
        + " WHERE r.latitude >= %s "
        + " and r.latitude <= %s "
        + " and r.longitude >= %s "
        + " and r.longitude <= %s "
        + " and r.date >= %s "
        + " and date(r.date) <= %s "
        + offensewhere
        + " limit 1000", [latmin, latmax, lngmin, lngmax, fromtime, untiltime])
        rows = cursor.fetchall()
        result['markers'] = rows

    with connection.cursor() as cursor:
        cursor.execute("SELECT offense_id, o.icon, o.name, count(*) as number,o.id FROM wegeheld_report r "
        + " left join wegeheld_car c on c.id = r.car_id " 
        + " left join wegeheld_carbrand b on b.id = c.brand_id "
        + " left join wegeheld_offense o on o.id = offense_id "
        + " WHERE r.latitude >= %s "
        + " and r.latitude <= %s "
        + " and r.longitude >= %s "
        + " and r.longitude <= %s "
        + " and r.date >= %s "
        + " and date(r.date) <= %s "
        + offensewhere
        + " group by offense_id "
        + " order by number desc "
        , [latmin, latmax, lngmin, lngmax, fromtime, untiltime])
        rows = cursor.fetchall()
        nrows=[]
        total=0
        for row in rows:
            row=list(row)
            row[1] = static(row[1])
            nrows.append(row)
            total += row[3]
        result['summary'] = nrows

    with connection.cursor() as cursor:
        cursor.execute("SELECT ifnull(b.name, '[verloren]') as name, count(*) as number, b.id FROM wegeheld_report r "
        + " left join wegeheld_car c on c.id = r.car_id " 
        + " left join wegeheld_carbrand b on b.id = c.brand_id "
        + " WHERE r.latitude >= %s "
        + " and r.latitude <= %s "
        + " and r.longitude >= %s "
        + " and r.longitude <= %s "
        + " and r.date >= %s "
        + " and date(r.date) <= %s "
        + offensewhere
        + " group by b.id "
        + " order by number desc "
        + " limit 1000", [latmin, latmax, lngmin, lngmax, fromtime, untiltime])
        rows = cursor.fetchall()
        result['brands'] = rows

        result['total'] = total
    return JsonResponse(result, safe=False)

@csrf_exempt
def get_markersum(request):
    latmin = request.GET.get("latmin")
    latmax = request.GET.get("latmax")
    lngmin = request.GET.get("lngmin")
    lngmax = request.GET.get("lngmax")
    local_tz = pytz.timezone("Europe/Berlin")

    try:
        untiltime = local_tz.localize(datetime.strptime(request.GET.get('untiltime'), '%Y-%m-%d %H:%M:%S'))
    except:
        try:
            untiltime = local_tz.localize(datetime.strptime(request.GET.get('untiltime'), '%Y-%m-%d'))
        except: 
            untiltime = datetime.now(pytz.utc)

    try:
        fromtime = local_tz.localize(datetime.strptime(request.GET.get('fromtime'), '%Y-%m-%d %H:%M:%S'))
    except :
        try:
            fromtime = local_tz.localize(datetime.strptime(request.GET.get('fromtime'), '%Y-%m-%d'))
        except: 
            fromtime = untiltime - dateutil.relativedelta.relativedelta(months=1)

    result=[]
    with connection.cursor() as cursor:
        cursor.execute("SELECT offense_id, o.icon, o.name, count(*) as number FROM wegeheld_report r "
        + " inner join wegeheld_car c on c.id = r.car_id " 
        + " inner join wegeheld_carbrand b on b.id = c.brand_id "
        + " left join wegeheld_offense o on o.id = offense_id "
        + " WHERE r.latitude >= %s "
        + " and r.latitude <= %s "
        + " and r.longitude >= %s "
        + " and r.longitude <= %s "
        + " and r.date >= %s "
        + " and r.date <= %s "
        + " group by offense_id "
        + " limit 1500", [latmin, latmax, lngmin, lngmax, fromtime, untiltime])
        rows = cursor.fetchall()
        print("results: {}".format(len(rows)))
        return JsonResponse(rows, safe=False)

@csrf_exempt
@xframe_options_exempt
def get_obstructions(request):
    obstructions=list(map(lambda o : {'id': o.id, 'name': o.name}, Obstructions.objects.all()))
    return JsonResponse(obstructions, safe=False)

@csrf_exempt
@csrf_exempt
@xframe_options_exempt
def get_offices(request):
    offices=list(map(lambda o : {'id': o.id, 'postalcode' : o.postalcode, 'name': o.name, 'email':o.email}, PublicAffairsOffice.objects.filter(postalcode__contains=request.GET.get('postalcode'))))[:50]
    return JsonResponse(offices, safe=False)

@csrf_exempt
@xframe_options_exempt
def get_offenses(request):
    offenses=list(map(lambda o : {'id': o.id, 'icon' : static(o.icon), 'name': o.name}, Offense.objects.all()))
    return JsonResponse(offenses, safe=False)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
@xframe_options_exempt
def index(request):
    template = loader.get_template('mapview.html')
    ip=get_client_ip(request)
    print("Client ip = {}".format(ip))
    if(ip=="127.0.0.1"):
        ip="46.253.63.59"
    g = geocoder.ip(ip)
    print("lat={}".format(g.latlng))
    if(g.latlng):
        context={'lat':str(g.latlng[0]),'lng':str(g.latlng[1])}
    else:
        context={'lat': str(52.3667),'lng':str(9.7167)}
    logger = logging.getLogger(__name__)
    # logger.debug("TestLog" . format(g.latlng))

    offenses=Offense.objects.all()
    context['offenses']=offenses
    return HttpResponse(template.render(context, request))

@csrf_exempt
@xframe_options_exempt
def createReporter(request):
    city    = request.POST.get("city").strip()
    zipcode = request.POST.get("zip").strip()
    email = request.POST.get("email")
    nickname = request.POST.get("nickname")

    try:
        reporter = Reporter.objects.get(email=email)
        if(reporter.city==city and reporter.zip==zipcode and reporter.email==email and nickname==nickname):
            return HttpResponse("already found!")
        else:
            return HttpResponseBadRequest("nickname exists with different data!")
    except Reporter.DoesNotExist:
        reporter = Reporter(email=email, city=city, zip=zipcode, nickname=nickname)
        reporter.createAuthKey() # deactivating it
        reporter.save()
        # ToDo: send an E-Mail with token
        return HttpResponse("ok")
    except Reporter.MultipleObjectsReturned:
        return HttpResponseBadRequest("nickname exists with different data!")

    return HttpResponse("\n\nok: " + street.name)

@csrf_exempt
@xframe_options_exempt
def verifyReporter(request):
    email = request.POST.get("email")
    nickname = request.POST.get("nickname")
    authkey=request.POST.get("authkey")
    try:
        reporter = Reporter.objects.get(email=email, nickname=nickname, authkey=authkey)
        reporter.hidden=false
        return HttpResponse("ok");
    except Reporter.DoesNotExist:
        return HttpResponseBadRequest("not found!")

@csrf_exempt
@xframe_options_exempt
def sendReport(request):
    lat    = request.POST.get("lat")
    lng    = request.POST.get("lng")
    print("lat={}, lng={}".format(lat,lng))
    lat=lat.replace(',','.');
    lng=lng.replace(',','.');
    dat    = request.POST.get("start")
    off    = request.POST.get("offense")
    action    = request.POST.get("action")
    saying = request.POST.get("saying")
    twn    = request.POST.get("city")
    zipcode    = request.POST.get("zipcode")
    pstreet = request.POST.get("street")
    streetnr = request.POST.get("streetnr")
    color =  request.POST.get("color")
    brand =  request.POST.get("brand")
    obstruction =  request.POST.get("obstruction")
    authkey=request.POST.get("authkey")
    
    plate=""
    nick=request.POST.get("reporter")
    reporteremail=request.POST.get("reporteremail")

    if(not action):
        action = 10
    
    twitteraccount=request.POST.get("twitteraccount")

    try:
        print("check sendREport Files: ")
        print("files: {}".format(request.FILES.items()))
    except Exception as e:
        print("error: ")
        print(e)
    if(request.POST.get("saveOnly")):
        image_data = request.POST.get("thephoto");
        image_data = dataUrlPattern.match(image_data).group(2)
        # image_data = image_data.encode()
        image_data = base64.b64decode(image_data)
        fname='photo_'+twn+"_"+nick+"_"+dat+request.POST.get("filename")
        fname = fname.translate ({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        fname='/opt/data/images/'+fname+'.jpg'
        with open(fname, 'wb') as img:
             img.write(image_data)
             img.flush()
        files.append(image_data)
        sys.stdout.flush();

    # logger.debug("post = \n{0}".format(request.POST))
    # print("post = \n{0}".format(request.POST))
    return importReport(request, lat, lng, dat, off, action, saying, twn, zipcode, pstreet, streetnr, color, brand, obstruction, nick, reporteremail, authkey, plate, twitteraccount)
    # return HttpResponse("OK");


@csrf_exempt
def uploadfile(request):
    template = loader.get_template('upload.html')
    prefill={}
    return HttpResponse(template.render(prefill))

    action = request.GET.get("action")
    postalcodelist = request.GET.get("postalcodes")
    if(not postalcodelist and not action):
        return HttpResponse(template.render({"user":request.user.username}))

    postalcodes=""
    try:
        postalcodes = re.split("[ ,]+",postalcodelist)
    except:
        pass
    email=request.GET.get("email")
    city=request.GET.get("city")
    if (action == "prepare"):
        prefill={
            "postalcodes": ",".join(postalcodes),
            "email":request.GET.get("email"),
            "city":request.GET.get("city"),
            "search":"http://www.plz-postleitzahl.de/site.plz/search.html?c=ort&q=" + request.GET.get("city")
            }
        foundOffices = PublicAffairsOffice.objects.filter(name__startswith=request.GET.get("city"))
        prefill['found']="\n".join(map(lambda o: str(o), foundOffices))
        return HttpResponse(template.render(prefill))

    message=""
    for code in postalcodes:
        try:
            office=PublicAffairsOffice.objects.get(postalcode=code)
        except:
            office = PublicAffairsOffice()
            office.postalcode=code
        office.email=email
        office.name=city
        office.deleted=0
        office.hidden=0
        office.save()
        message += "insert into wegeheld_publicaffairsoffice (postalcode, email, name, tmstmp, crdate, deleted, hidden) values ('{}', '{}','{}',now(), now(), 0, 0);".format(code,email,city)
        message += "\n"

    return HttpResponse(template.render(
        {"user":request.user.username,
            "message":message
            }
    ))

@csrf_exempt
@login_required
def oamt(request):
    if(not request.user.is_authenticated):
        return HttpResponse("uh, should not happen!")
    template = loader.get_template('oamt.html')
    action = request.GET.get("action")
    postalcodelist = request.GET.get("postalcodes")
    if(not postalcodelist and not action):
        return HttpResponse(template.render({"user":request.user.username}))

    postalcodes=""
    try:
        postalcodes = re.split("[ ,]+",postalcodelist)
    except:
        pass
    email=request.GET.get("email")
    city=request.GET.get("city")
    if (action == "prepare"):
        prefill={
            "postalcodes": ",".join(postalcodes),
            "email":request.GET.get("email"),
            "city":request.GET.get("city"),
            "search":"http://www.plz-postleitzahl.de/site.plz/search.html?c=ort&q=" + request.GET.get("city")
            }
        foundOffices = PublicAffairsOffice.objects.filter(name__startswith=request.GET.get("city"))
        prefill['found']="\n".join(map(lambda o: str(o), foundOffices))
        return HttpResponse(template.render(prefill))

    message=""
    for code in postalcodes:
        try:
            office=PublicAffairsOffice.objects.get(postalcode=code)
        except:
            office = PublicAffairsOffice()
            office.postalcode=code
        office.email=email
        office.name=city
        office.deleted=0
        office.hidden=0
        office.save()
        message += "insert into wegeheld_publicaffairsoffice (postalcode, email, name, tmstmp, crdate, deleted, hidden) values ('{}', '{}','{}',now(), now(), 0, 0);".format(code,email,city)
        message += "\n"

    return HttpResponse(template.render(
        {"user":request.user.username,
            "message":message
            }
    ))

def importReport(request, lat, lng, dat, off, act, saying, twn, zipcode, pstreet, streetnr, color, brand, obstruction, nick, reporteremail, authkey, plate, twitteraccount):

    # logger.debug("encoding=")
    # logger.debug(request.encoding)
    # if(HttpRequest.encoding):
    #    logger.debug("encoding = {}",str(HttpRequest.encoding))

    print("import report: {} {} nick {} '{}' plate {}".format(lat, dat, nick, reporteremail, plate))

    fname="log_"+nick+"_"+now
    fname='/opt/data/logs/'+fname+'.txt'
    with open(fname, 'w') as log:
        try:
            if(lat):
                log.write("\nlat="+lat)
            if(lng):
                log.write("\nlng="+lng)
            if(dat):
                log.write("\ndat="+dat)
            if(off):
                log.write("\noff="+off)
            if(act):
                log.write("\nact="+act)
            if(saying):
                log.write("\nsaying="+saying)
            if(twn):
                log.write("\ntwn="+twn)
            if(zipcode):
                log.write("\nzipcode="+zipcode)
            if(pstreet):
                log.write("\npstreet="+pstreet)
            if(color):
                log.write("\ncolor="+color)
            if(brand):
                log.write("\nbrand="+brand)
            if(obstruction):
                log.write("\nobstruction="+obstruction)
            if(reporteremail):
                log.write("\nreporteremail="+reporteremail)
            if(plate):
                log.write("\nplate="+plate)
            log.write("\n--------\n")
            log.write("POST: {}".format(request.POST))
            log.flush()
        except Exception as e:
            print("logging ex: {}".format(e))

        sys.stdout.flush();
    report = Report()
    report.latitude    = lat
    report.longitude   = lng
    dat=re.sub(r"[ +]+[0-9]*$","",dat)
    dat=str.replace(dat, 'T', ' ')
    if(len(dat) < 19):
        dat += ":00"
    print("dat={}".format(dat))
    # tzname = request.session.get('django_timezone')
    local_tz = pytz.timezone("Europe/Berlin")
    timezone.activate(local_tz)
    foundDat=False
    sys.stdout.flush()
    try:
        idat=int(dat)
        print("idat={}".format(idat))
        if(idat > 1344451932):
            report.date = local_tz.normalize(datetime.utcfromtimestamp(idat).replace(tzinfo=pytz.utc).astimezone(local_tz))
            #  print("date = {}".format(report.date))
            foundDat=True
            sys.stdout.flush()

    except ValueError:
        try:
            report.date = local_tz.localize(datetime.strptime(dat, '%Y-%m-%d %H:%M:%S'))
        except ValueError:
            print("no date from {}".format(dat))
            sys.stdout.flush()
            return HttpResponseBadRequest("Fehlendes oder ungueltiges Datum: '" + dat + "'")

    if(obstruction):
        print("obstruction?")
        sys.stdout.flush()
        try:
            obstruction=Obstruction.objects.get(id=obstruction)
            report.obstruction=obstruction
        except Obstruction.DoesNotExist:
            print ("Behinderung '{}' nicht gefunden!".format(obstruction))
            return HttpResponseBadRequest("Behinderung '"+obstruction+"' nicht gefunden!")

    try:
        offense=Offense.objects.get(id=off)
        report.offense=offense
    except Offense.DoesNotExist:
        print ("Offense '{}' nicht gefunden!".format(off))
        return HttpResponseBadRequest("Vorfall '"+off+"' nicht gefunden!")


    try:
        action=Action.objects.get(id=act)
        report.action=action
    except Action.DoesNotExist:
        return HttpResponseBadRequest("Aktion '"+act+"' nicht gefunden!")



    try:
        reporter=Reporter.objects.get(nickname=nick)
        report.reporter=reporter
        print("reporter = " + str(reporter.id))
    except Reporter.DoesNotExist:
        return HttpResponseBadRequest("Melder '"+nick+"' nicht gefunden!")
    except Reporter.MultipleObjectsReturned:
        print("Melder '"+nick+"' nicht eindeutig!")
        logger.debug("post = \n{0}".format(request.POST))
        reporter=Reporter.objects.filter(nickname=nick, email=reporteremail)[0]
        report.reporter=reporter


    twn=twn.strip()
    zipcode=zipcode.strip()
    print("twn={} zipcode={}".format(twn,zipcode))
    sys.stdout.flush()
    
    try:
        town=Town.objects.get(name=twn, postalcode=zipcode)
    except Town.DoesNotExist:
        town = Town(name=twn, postalcode=zipcode, deleted=False, hidden=False)
        town.save()

    sys.stdout.flush()
    files = []
    if(request.POST.get("thephoto")):
        print("thephoto!");
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        image_data = request.POST.get("thephoto");
        image_data = dataUrlPattern.match(image_data).group(2)
        # image_data = image_data.encode()
        image_data = base64.b64decode(image_data)
        fname='photo_'+twn+"_"+nick+"_"+dat
        fname = fname.translate ({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        fname='/opt/data/images/'+fname+'.jpg'
        with open(fname, 'wb') as img:
             img.write(image_data)
             img.flush()
        files.append(image_data)
        sys.stdout.flush();
        

    pstreet=pstreet.strip()
    try:
        streetlist = Street.objects.filter(name=pstreet,town=town)
        if(streetlist):
            street=streetlist[0]
        else:
            street=Street(name=pstreet, town=town, deleted=False,hidden=False)
            street.hidden=False
            street.deleted=False
            street.save()



    except Street.DoesNotExist:
        street=Street(name=pstreet, town=town, deleted=False,hidden=False)
        street.save()

    try:
        address=Address.objects.get(street=street,town=town,streetnumber=streetnr)
        address.hidden=False
        address.deleted=False
    except Address.DoesNotExist:
        address=Address(street=street,town=town,streetnumber=streetnr)
        address.save()

    report.address=address
    if(not plate > ""):
        plate="/"


    if(plate > ""):
        try: 
            car = Car.objects.get(brand_id=brand, color_id=color, licenseplate=plate)
            print("Car = %s" % car.licenseplate)
        except Car.DoesNotExist:
            car = Car(brand_id=brand, color_id=color, licenseplate=plate)
            car.save()
        report.car = car

    if(saying and int(saying) > -1):
        try:
            funnySaying=Funnysaying.objects.get(id=saying)
            report.funny_saying =funnySaying
        except Funnysaying.DoesNotExist:
            return HttpResponseBadRequest("Spruch '"+saying+"' nicht gefunden!")

    report.save()
    report.crdate = report.date
    report.crdate = report.date
    
    if(twitteraccount == "test"):
        cfg = cfgTest()
    else:
        cfg = cfgWeh()
        # cfg = cfgTest()


    if(request.FILES):
        for name,content in request.FILES.items():
            if('photoO' in name):
                continue
            if('PHOTOO' in name):
                continue
            files.append(content)
        
    if(files):
        reply=send_tweet(files, report, cfg)
        idstr=reply.json().get("id_str")
        if(idstr):
            report.tweet="https://twitter.com/i/web/status/"+idstr
        else:
            print("tweet not successful!")
            sys.stdout.flush()
        report.save()
    

    return HttpResponse("ok")


@csrf_exempt
def home(request):

    logger = logging.getLogger('django')

    reqstr=request.GET.get("tx_ssm_ssmfe[data]")

    if(reqstr):
        if(reqstr == "Office" and request.GET.get("zipcode")): 
            postalcode=request.GET.get("zipcode")
            return getOffice(postalcode)
        if(reqstr == "Office" and request.GET.get("plz")): 
            postalcode=request.GET.get("plz")
            return getOffice(postalcode)

        if(requestToCsvObject[reqstr]):
            return getCsv(requestToCsvObject[reqstr])

        return HttpResponse("nix")



    origp=request.POST
    if(origp.get('twitteraccount')):
        logger.debug("POST = \n{0}".format(origp))
     

    # logger.debug("post = \n{0}".format(request.POST))
    reqstr=request.GET.get("tx_ssm_ssmfe[action]")
    postreqstr=request.POST.get("tx_ssm_ssmfe[action]")
    # logger.debug('req={}, postreq={}', reqstr, postreqstr)
    if(reqstr == "importReport" or postreqstr == "importReport"):
        lat    = request.POST.get("tx_ssm_ssmfe[latitude]")
        lng    = request.POST.get("tx_ssm_ssmfe[longitude]")
        dat    = request.POST.get("tx_ssm_ssmfe[date]")
        off    = request.POST.get("tx_ssm_ssmfe[offense_id]")
        act    = request.POST.get("tx_ssm_ssmfe[action_id]")
        saying = request.POST.get("tx_ssm_ssmfe[saying_id]")
        text = request.POST.get("tx_ssm_ssmfe[text]")
        twn    = request.POST.get("tx_ssm_ssmfe[town]")
        zipcode    = request.POST.get("tx_ssm_ssmfe[postal]")
        pstreet = request.POST.get("tx_ssm_ssmfe[street]")
        streetnr = request.POST.get("tx_ssm_ssmfe[street_number]")
        color =  request.POST.get("tx_ssm_ssmfe[color_id]")
        brand =  request.POST.get("tx_ssm_ssmfe[brand_id]")
        obstruction =  request.POST.get("tx_ssm_ssmfe[obstruction_id]")
        nick=request.POST.get("tx_ssm_ssmfe[reporter]")
        reporteremail=request.POST.get("tx_ssm_ssmfe[reporteremail]")
        plate=request.POST.get("tx_ssm_ssmfe[plate]")
        twitteraccount=request.POST.get("twitteraccount")
        # logger.debug("encoding=")
        # logger.debug(request.encoding)
        # if(HttpRequest.encoding):
        #    logger.debug("encoding = {}",str(HttpRequest.encoding))


        ## activate
        # return importReport(request, lat, lng, dat, off, act, saying, twn, zipcode, pstreet, streetnr, color, brand, obstruction, nick, reporteremail, authkey, plate, twitteraccount)

        now = datetime.now().strftime('%Y_%m_%d_%H%M%S.%f')

        fname="log_"+nick+"_"+now
        fname='/opt/data/logs/'+fname+'.txt'
        with open(fname, 'w') as log:
            try:
                if(lat):
                    log.write("\nlat="+lat)
                if(lng):
                    log.write("\nlng="+lng)
                if(dat):
                    log.write("\ndat="+dat)
                if(off):
                    log.write("\noff="+off)
                if(act):
                    log.write("\nact="+act)
                if(saying):
                    log.write("\nsaying="+saying)
                if(twn):
                    log.write("\ntwn="+twn)
                if(zipcode):
                    log.write("\nzipcode="+zipcode)
                if(pstreet):
                    log.write("\npstreet="+pstreet)
                if(color):
                    log.write("\ncolor="+color)
                if(brand):
                    log.write("\nbrand="+brand)
                if(obstruction):
                    log.write("\nobstruction="+obstruction)
                if(reporteremail):
                    log.write("\nreporteremail="+reporteremail)
                if(plate):
                    log.write("\nplate="+plate)
                log.write("\n--------\n")
                log.write("POST: {}".format(request.POST))
                log.flush()
            except Exception as e:
                print("logging ex: {}".format(e))

            sys.stdout.flush();


        report = Report()
        report.latitude    = lat
        report.longitude   = lng
        dat=re.sub(r"[ +]+[0-9]*$","",dat)
        # tzname = request.session.get('django_timezone')
        local_tz = pytz.timezone("Europe/Berlin")
        timezone.activate(local_tz)
        foundDat=False
        try:
            idat=int(dat)
            if(idat > 1344451932):
                report.date = local_tz.normalize(datetime.utcfromtimestamp(idat).replace(tzinfo=pytz.utc).astimezone(local_tz))
                print("date = {}".format(report.date))
                foundDat=True

        except ValueError:
            try:
                report.date = local_tz.localize(datetime.strptime(dat, '%Y-%m-%d %H:%M:%S'))
            except ValueError:
                return HttpResponseBadRequest("Datum ungültig oder leer: '" + dat + "'")



        if(obstruction):
            try:
                obstruction=Obstruction.objects.get(id=obstruction)
                report.obstruction=obstruction
            except Obstruction.DoesNotExist:
                return HttpResponseBadRequest("Behinderung '"+obstruction+"' nicht gefunden!")

        try:
            offense=Offense.objects.get(id=off)
            report.offense=offense
        except Offense.DoesNotExist:
            return HttpResponseBadRequest("Vorfall "+off+"nicht gefunden!")


        try:
            action=Action.objects.get(id=act)
            report.action=action
        except Action.DoesNotExist:
            return HttpResponseBadRequest("Action "+act+" nicht gefunden!")



        twn=twn.strip()
        zipcode=zipcode.strip()
        
        try:
            town=Town.objects.get(name=twn, postalcode=zipcode)
        except Town.DoesNotExist:
            town = Town(name=twn, postalcode=zipcode, deleted=False, hidden=False)
            town.save()

        try:
            reporter=Reporter.objects.get(nickname=nick)
            report.reporter=reporter
            print("reporter = " + str(reporter.id))
        except Reporter.DoesNotExist:
            reporter = Reporter(city=twn, zip=zipcode, nickname=nick)
            if(reporteremail):
                reporter.email=reporteremail
            reporter.save()
            print("reporter angelegt:" + str(reporter))
            report.reporter=reporter
        except Reporter.MultipleObjectsReturned:
            print("reporter '"+nick+"' not unique!")
            logger.debug("post = \n{0}".format(request.POST))
            reporter=Reporter.objects.filter(nickname=nick, email=reporteremail)[0]
            report.reporter=reporter


        pstreet=pstreet.strip()
        try:
            streetlist = Street.objects.filter(name=pstreet,town=town)
            if(streetlist):
                street=streetlist[0]
            else:
                street=Street(name=pstreet, town=town, deleted=False,hidden=False)
                street.hidden=False
                street.deleted=False
                street.save()



        except Street.DoesNotExist:
            street=Street(name=pstreet, town=town, deleted=False,hidden=False)
            street.save()

        try:
            address=Address.objects.get(street=street,town=town,streetnumber=streetnr)
            address.hidden=False
            address.deleted=False
        except Address.DoesNotExist:
            address=Address(street=street,town=town,streetnumber=streetnr)
            address.save()

        report.address=address
        if(not plate > ""):
            plate="/"


        if(plate > ""):
            try: 
                car = Car.objects.get(brand_id=brand, color_id=color, licenseplate=plate)
                print("Car = %s" % car.licenseplate)
            except Car.DoesNotExist:
                car = Car(brand_id=brand, color_id=color, licenseplate=plate)
                car.save()
            report.car = car

        if(saying and int(saying) > -1):
            try:
                funnySaying=Funnysaying.objects.get(id=saying)
                report.funny_saying =funnySaying
            except Funnysaying.DoesNotExist:
                return HttpResponseBadRequest("saying '"+saying+"' nicht gefunden!")

        if(text):
            report.free_text=text

        report.save()
        
        if(twitteraccount == "test"):
            cfg = cfgTest()
        else:
            cfg = cfgWeh()
            # cfg = cfgTest()


        if(request.FILES):
            files = []
            for name,content in request.FILES.items():
                if('photoO' in name):
                    continue
                if('PHOTOO' in name):
                    continue
                files.append(content)
            
            reply=send_tweet(files, report, cfg)
            idstr=reply.json().get("id_str")
            if(idstr):
                report.tweet="https://twitter.com/i/web/status/"+idstr
            else:
                logger.debug("tweet not successful!")
            report.save()
        

        return HttpResponse("ok")

    if(reqstr == "importReporter" or postreqstr == "importReporter"):
        city    = request.POST.get("tx_ssm_ssmfe[city]").strip()
        zipcode = request.POST.get("tx_ssm_ssmfe[zip]").strip()
        email = request.POST.get("tx_ssm_ssmfe[email]")
        nickname = request.POST.get("tx_ssm_ssmfe[nickname]")

        try:
            reporter = Reporter.objects.get(nickname=nickname)
            if(reporter.city==city and reporter.zip==zipcode and reporter.email==email):
                return HttpResponse("already found!")
            else:
                return HttpResponseBadRequest("nickname exists with different data!")
        except Reporter.DoesNotExist:
            reporter = Reporter(email=email, city=city, zip=zipcode, nickname=nickname)
            reporter.save()
            return HttpResponse("ok")
        except Reporter.MultipleObjectsReturned:
            print("reporter '"+nick+"' not unique!")
            logger.debug("post = \n{0}".format(request.POST))
            reporter=Reporter.objects.filter(nickname=nick, email=reporteremail)[0]
            report.reporter=reporter

        return HttpResponse("\n\nok: " + street.name)

    lastTouched=cache.get('lastTouched')
    if(not lastTouched):
        lastTouched=last_touched()
        cache.set('lastTouched',lastTouched,300)
    return HttpResponse(lastTouched)

def fillMailtext(emailText, request):
    t = emailText.template
    for key,value in request.GET.items():
        t = t.replace("{{"+key+"}}", value)
    t = re.sub(r"\{\{.*?\}\}"," ", t)
    return t

@csrf_exempt
@xframe_options_exempt
def get_mailtext(request):
    offense = request.GET.get("offense")
    postalcode = request.GET.get("postalcode")
    if(offense and postalcode):
        try:
            mailtext = EmailText.objects.get(offense=offense, postalcode=postalcode)
            return HttpResponse(fillMailtext(mailtext, request))
        except Exception as e:
            print("first ex: {}".format(e))
    if(offense):
        try:
            mailtext = EmailText.objects.get(offense=offense, postalcode__isnull=True)
            return HttpResponse(fillMailtext(mailtext, request))
        except Exception as e:
            print("sec ex: {}".format(e))

    try:
        mailtext = EmailText.objects.get(postalcode=postalcode, offense__isnull=True)
        return HttpResponse(fillMailtext(mailtext, request))
    except Exception as e:
        print("3. ex: {}".format(e))
    try:
        mailtext = EmailText.objects.get(postalcode__isnull=True, offense__isnull=True)
        return HttpResponse(fillMailtext(mailtext, request))
    except Exception as e:
        print("4. ex: {}".format(e))
    return HttpResponse("Fehler bei der Suche nach einem E-Mail-Text.")



# Create your views here.
