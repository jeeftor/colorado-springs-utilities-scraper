"""Scraper Def"""
import logging
import urllib.parse
import requests

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1

from csu.parse import make_form_data

_URL1 = "https://wss.csu.org/SelfService/CMSSvcLogIn.jsp"
_URL2 = "https://wss.csu.org/SelfService/SSvcController/verifylogininfo"
_URL3 = "https://wss.csu.org/SelfService/SSvcController/authenticate"
_URL4 = "https://wss.csu.org/SelfService/SSvcController/myusage"
_URL5 = "https://wss.csu.org/MyUsage/Pages/Home.aspx"
_URL6 = "https://wss.csu.org/MyUsage/Pages/Home.aspx"
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


print("Effective logging level is {}".format(
    logging.getLevelName(LOGGER.getEffectiveLevel())))


class CSUUtilityScraper:
    """Utility Scraper for CSU"""

    def __init__(self, username: str, password: str):
        # Predefine the cookies
        self._cookies = None
        self.password = password
        self.username = username

    def _request1(self):
        """Initial request to the login page starts the cookie process"""
        LOGGER.info("Making initial login request to get a session cookie")
        response1 = requests.get(_URL1)
        self._cookies = response1.cookies

    def _request2(self):
        """Make the second request into the verify login URL (more cookies)"""
        # Payload for second request
        payload2 = f"userId={self.username}&password={self.password}"
        headers2 = {'Content-type': 'application/x-www-form-urlencoded'}
        LOGGER.info("Verifying user credentials")
        requests.post(url=_URL2,
                      cookies=self._cookies,
                      headers=headers2,
                      data=payload2)

    def _request3(self):
        """Hit the authenticate endpoint"""
        payload3 = f"_charset_=UTF-8&password={urllib.parse.quote(self.password, safe='!')}&userId={urllib.parse.quote(self.username, safe='!')}"
        headers3 = {'Content-Type': 'application/x-www-form-urlencoded'}
        LOGGER.info("Authorizing User")
        requests.post(url=_URL3, cookies=self._cookies, headers=headers3, data=payload3)

    def _request4(self):
        """Start the MyUsage flow - and get the new cookie - ignore redirect"""
        LOGGER.info("Setting OAMUserID Cookie")
        r = requests.get(url=_URL4, cookies=self._cookies, allow_redirects=False)

        # Rewrite the OAMUserID Cookie
        oam_user_id = r.cookies.get("OAMUserID")
        # Store the cookie in the cookie jar
        self._cookies.set('OAMUserID', oam_user_id, domain='wss.csu.org', path="/")

    def _request5(self) -> str:
        """Do more cookie stuff using manual redirect"""
        LOGGER.info("Setting ASP.NET_SessionId Cookie")
        r = requests.get(url=_URL5, cookies=self._cookies)
        session_id = r.cookies.get("ASP.NET_SessionId")
        self._cookies.set("ASP.NET_SessionId", session_id, domain='wss.csu.org', path="/")
        return r.text

    def _request6(self, text):
        """Download Z Datas"""
        LOGGER.info("Extracting Data")
        form_data = make_form_data(text)
        r = requests.post(url=_URL6, data=form_data, cookies=self._cookies)
        print(r.text)

    def get_gas(self):
        # Extract initial cookie from login page
        self._request1()
        self._request2()
        self._request3()
        self._request4()
        text = self._request5()
        return self._request6(text)

