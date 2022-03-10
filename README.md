# colorado-springs-utilities-scraper
Python scraper to pull down CSU.org usage data

This is a pretty minimal explanation of whats going on but basically I watched the web traffic into CSU's log in page and tried to figure out how to generate the required cookies and various web calls in order to download the utility data.

I'm pretty sure the last call has some hard-coded stuff in it which is probably related to a utility account or something - This project was developed for home assistant as an integration for the energy meter however I've been spending a lot of time on my firepalce integration and this is somewhat on the back burner...

If someboyd wants to collaborate - or take things over a bit let me know - otherwise it might be some time before i get back to this as I'm busy :)


```
_URL1 = "https://wss.csu.org/SelfService/CMSSvcLogIn.jsp"
_URL2 = "https://wss.csu.org/SelfService/SSvcController/verifylogininfo"
_URL3 = "https://wss.csu.org/SelfService/SSvcController/authenticate"
_URL4 = "https://wss.csu.org/SelfService/SSvcController/myusage"
_URL5 = "https://wss.csu.org/MyUsage/Pages/Home.aspx"
_URL6 = "https://wss.csu.org/MyUsage/Pages/Home.aspx"
```

If you want to edit things -> probably want to look at URL5 and URL6 assuming you can get stuff working :)
