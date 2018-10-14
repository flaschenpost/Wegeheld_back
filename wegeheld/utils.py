from TwitterAPI import TwitterAPI
import io
from io import BytesIO
import base64
import logging

def get_api(cfg):
    api= TwitterAPI(**cfg)
    print("api = {}".format(api))
    return api

def send_tweet(photos, report, cfg):
    logger = logging.getLogger('django')
    logger.debug("Starting send_tweet!")
 
    # Fill in the values noted in previous step here
    api = get_api(cfg)
    # print(api.verify_credentials())

    media_ids = []

    try:
        # twitterText = "Gerade in #" + report.address.town.name + " in #"+report.address.street.name + ": #runtervomradweg #falschparker " 
        twitterText = "Wieder ein #Falschparker in #" + report.address.town.name + " in "+report.address.street.name + ": #WegDa!" 
        if(report.funny_saying):
            twitterText += " " + report.funny_saying.text

        if(report.free_text):
            twitterText += " " + report.free_text

        twitterText += " " + report.date.strftime('%d.%m.%Y')

        # logger.debug("twitterText = {0}".format(twitterText))
        reply = ""
        media_ids=[]
        i=0
        for photo in photos:
            if(hasattr(photo,'read')):
                data = photo.read()
            else:
                data = photo
            r = api.request('media/upload', None, {'media': data})
            print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')
            media_ids.append(str(r.json()['media_id']))
            # reply=api.PostUpdate({'status':twitterText, 'media_ids':media_ids})
        
        data = {'status':twitterText, 'media_ids':",".join(media_ids)}
        if(report.latitude):
            data['lat']=report.latitude
            data['long']=report.longitude
            data['geo_enabled']=True

        resp= api.request('statuses/update', data)
        return(resp)

    except Exception as err:
        logger.debug("Twitter error: {}",err)
        print("Twitter error: {0}".format(err))

    return(reply)

