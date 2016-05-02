
from oauth.models import OauthUserProfile


yinanxu = OauthUserProfile.objects.get(username='yinanxu')

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'


if yinanxu:
    yinanxu.access_token = ACCESS_TOKEN
    yinanxu.refresh_token = REFRESH_TOKEN
    yinanxu.expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=172800)
    yinanxu.save()
else:
    OauthUserProfile.objects.create(
            username='yinanxu', 
            access_token='access_token', 
            refresh_token='refresh_token', 
            expires_timestamp=datetime.datetime.now(pytz.utc)
        )

