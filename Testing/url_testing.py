from django.test import TestCase
from django.test import Client
from django.urls import reverse
from . import urls

class UrlTests(TestCase):
    def test_urls(self):

        url_list = urls.urlpatterns
        for url in url_list:

            try:
                # this only parses the urls which have name attribute in them
                url_v = str(url)[str(url).index('[')+1:str(url).index(']')].split('=')[1][1:-1]
                response = client.get(reverse('app_name:'+url_v))
                print("response code for "+url_v+" -> "+str(response.status_code))
                self.assertEquals(response.status_code, 200, "URL Test Error for the following URL-> " + url_v)
            except ValueError:
                print("error parsing url -> "+str(url))
