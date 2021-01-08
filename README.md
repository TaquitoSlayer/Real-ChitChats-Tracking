# Why was this made?
As per [this page](https://support.chitchats.com/support/solutions/articles/47000426692), ChitChats and their partner Asendia first give out a tracking number that will be updated only after the handoff is done to the courier of the country. However, as per [this page](https://support.chitchats.com/support/solutions/articles/47000426372-which-countries-does-asendia-ship-to-), they eventually go to the following Postal operators which otherwise give better tracking information.

Being a seller on eBay for almost 10 years now, having proper tracking information is a huge thing, and since I've started doing international shipments, there's a gaping hole in this for eBay sellers since Asendia doesn't offer timely tracking information, which in turn keeps your customers hanging wondering where the hell their package is, which then has you battling cases when you do decide to use them. Below is 20 cases in only 1 month alone of using Asendia with ChitChats (yep, i had 0 issues when staying within Canada and the US):<br /> 
![](https://i.imgur.com/MiF2bPQ.png)<br /> 
Now in theory, it's not ChitChats fault, they're just a middle man, it's really Asendia's fault for not scraping their shit better for other Postal operators when the handoff is done from one partner to another.

However as an eBay seller, the responsibility of the package is completely up to you, and with delays being up to 75 business days with international shipments, keeping up to date is a must. Regardless of how you notify your customers, they're still going to complain so that's why I made this script to help.
# What is this?
The script's purpose to grab the proper tracking number from Asendia once given and update tracking number respective to your Competed Sales, that way, the customer can just see the updates going forward from there instead of Asendia's crappy tracking.<br />
# How to use
First, install [python3 on your system](https://docs.python-guide.org/).<br />
For non-windows users, install [pip3](https://raturi.in/blog/installing-python3-and-pip3-ubuntu-mac-and-windows/) like so. Windows users, just select it in the installer before clicking install.<br />

Once you have that done, open your command line and navigate to your folder that you've downloaded this in and run:<br />
```pip3 install -r requirements.txt```<br /><br />
You need to make API keys for both ChitChats and eBay.<br />

For ChitChats, go to Settings > Account, then scroll down and create an Access Token:<br />
![](https://i.imgur.com/iuiAzT7.png)<br />
Copy and paste this into /configs/info.json and add your Client ID and Access Token that you just created:<br />
![](https://i.imgur.com/PMqYwy0.png)<br />
It should be in between the quotes.<br />

Once that's done, make your tokens for eBay by going over to [My Keys](https://developer.ebay.com/my/keys) and making sure you make them in production. Since I'm using the Trading API, we would need to make a User Token as well. [Generating one is straight forward](https://linuxconfig.org/introduction-to-ebay-api-with-python-the-trading-api-part-3). Make sure to add all your tokens in ebay.yaml so that your settings file is like so:<br />
![](https://i.imgur.com/6mUdOTL.png)<br /><br />
Then just run main.py<br />
```python3 main.py```<br />
![](https://i.imgur.com/HNo4XPc.png)<br />
For Linux and macOS, you can setup a cron job to run this every 24 hours, I have it like so. It works really well because it will only change orders once inducted. The basis of this is you need to make sure you're adding the Asendia tracking numbers first, or else the script won't be able to tell which order goes with what real tracking number.