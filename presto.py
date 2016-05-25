#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a prestocard site miner. Checks your prestocard balance and slacks
# you the result

import requests, os, json
from bs4 import BeautifulSoup as bs

#USERNAME = os.environ["PRESTO_USERNAME"]
#PASSWORD = os.environ["PRESTO_PASSWORD"]
#SLACKHOOK = os.environ["PRESTO_SLACKHOOK"]

def get_balance(username='', password=''):
    #slack = "https://hooks.slack.com/services/%s" % SLACKHOOK

    login = 'https://www.prestocard.ca/en-US/Pages/TransactionalPages/AccountLogin.aspx'
    formData = {
        "__VIEWSTATE":"/wEPDwUBMA9kFgJmD2QWAgIBD2QWBgIBD2QWAgISD2QWAgIBDxYCHgRocmVmBTQvX2xheW91dHMvMTAzMy9zdHlsZXMvUFJFU1RPL3RoZW1lLm1pbi5jc3M/dj0yLjMuMC4wZAIDDw8WAh4HVmlzaWJsZWhkZAIFD2QWCgIED2QWAgUaQWNjb3VudExvZ2luV2VicGFydENvbnRyb2wPZBYCZg9kFggCBQ9kFgJmDw8WBh4IQ3NzQ2xhc3MFDGVycm9ybWVzc2FnZR4EXyFTQgICHwFnZBYCAgMPFCsAAg8WBB4LXyFEYXRhQm91bmRnHgtfIUl0ZW1Db3VudAIBZGQWAmYPZBYCAgEPZBYEAgEPFgIeBFRleHQFaVlvdSBjb3VsZCBub3QgYmUgbG9nZ2VkIGluIHRvIHlvdXIgb25saW5lIGFjY291bnQuIFBsZWFzZSBjaGVjayB5b3VyIFVzZXJuYW1lIGFuZCBQYXNzd29yZCBhbmQgdHJ5IGFnYWluLmQCAw8PFgIfBgVpWW91IGNvdWxkIG5vdCBiZSBsb2dnZWQgaW4gdG8geW91ciBvbmxpbmUgYWNjb3VudC4gUGxlYXNlIGNoZWNrIHlvdXIgVXNlcm5hbWUgYW5kIFBhc3N3b3JkIGFuZCB0cnkgYWdhaW4uZGQCBw8PFgIfBgX/AUVudGVyIHlvdXIgdXNlcm5hbWUgYW5kIHBhc3N3b3JkIHRvIGxvZyBpbnRvIHlvdXIgb25saW5lIGFjY291bnQuIElmIHlvdSBoYXZlIG5vdCByZWdpc3RlcmVkLCB5b3UgY2FuIDxhICAgICBocmVmPSIvZW4tVVMvUGFnZXMvVHJhbnNhY3Rpb25hbFBhZ2VzL0Fzc29jaWF0ZUZhcmVNZWRpYS5hc3B4ICI+PHU+Y3JlYXRlIGFuIGFjY291bnQgbm93PC91PjwvYT4sIG9yIGxvZ2luIGFub255bW91c2x5IHdpdGggbGltaXRlZCBmdW5jdGlvbmFsaXR5LmRkAgkPZBYCZg8PFgIeEUFTV0ZlYXR1cmVFbmFibGVkaGQWAgIDD2QWBGYPZBYGAgEPZBYMAgEPDxYCHwFoZBYCAgEPDxYCHwYFClJlZ2lzdGVyZWRkZAIDDw8WAh8BZ2QWAgIBDw8WAh8GBQpSZWdpc3RlcmVkZGQCBQ9kFgICAw8PFgIeC1Bvc3RCYWNrVXJsBTcvZW4tVVMvUGFnZXMvVHJhbnNhY3Rpb25hbFBhZ2VzL0Fzc29jaWF0ZUZhcmVNZWRpYS5hc3B4ZGQCBw8PFgIfBgUIVXNlcm5hbWVkZAIJDw8WAh4JTWF4TGVuZ3RoAhlkZAINDw8WAh8JAhlkZAIDDw8WAh8IBTMvZW4tVVMvUGFnZXMvVHJhbnNhY3Rpb25hbFBhZ2VzL0ZvcmdvdFBhc3N3b3JkLmFzcHhkZAIFDw8WAh8IBTMvZW4tVVMvUGFnZXMvVHJhbnNhY3Rpb25hbFBhZ2VzL0ZvcmdvdFVzZXJuYW1lLmFzcHhkZAIBD2QWAgIBD2QWAmYPZBYCAgEPZBYIAgUPZBYCZg8WAh4Fc3R5bGUFDGRpc3BsYXk6bm9uZRYCAgMPFgIfCgUMZGlzcGxheTpub25lZAIHD2QWAmYPZBYCAgMPFCsAAmRkZAIVDw8WAh8IBTMvZW4tVVMvUGFnZXMvVHJhbnNhY3Rpb25hbFBhZ2VzL0ZvcmdvdFBhc3N3b3JkLmFzcHhkZAIXDw8WAh8IBTMvZW4tVVMvUGFnZXMvVHJhbnNhY3Rpb25hbFBhZ2VzL0ZvcmdvdFVzZXJuYW1lLmFzcHhkZAILD2QWAmYPZBYGAgEPZBYCZg8WAh8KBQxkaXNwbGF5Om5vbmUWAgIDDxYCHwoFDGRpc3BsYXk6bm9uZWQCAw9kFgJmD2QWAgIDDxQrAAJkZGQCBQ9kFgYCAQ8PFgIfAWhkZAIDDw8WAh8BZ2RkAgcPDxYCHwkCEWRkAggPZBYEAgMPZBYCAgEPZBYCAgIPFgIeBGxhbmcFAmZyFgICAQ8WAh8FAgFkAgcPDxYCHwFnZGQCCg9kFgICAQ9kFgICAQ8PFgIfCAUjL2VuLVVTL1BhZ2VzL0NvbnRlbnRQYWdlcy9Ib21lLmFzcHhkZAIUD2QWAgIDD2QWAgIBD2QWAmYPZBYIAgEPDxYCHg1BbHRlcm5hdGVUZXh0BRdMaW5rIHRvIFBSRVNUTyBGYWNlYm9va2RkAgIPDxYCHwwFFkxpbmsgdG8gUFJFU1RPIFR3aXR0ZXJkZAIDDw8WAh8MBRZMaW5rIHRvIFBSRVNUTyBZb3VUdWJlZGQCBA8PFgIfDAUVTGluayB0byBQUkVTVE8gRmxpY2tyZGQCGA9kFgICAw9kFgICAQ8PFgIfCAUjL2VuLVVTL1BhZ2VzL0NvbnRlbnRQYWdlcy9Ib21lLmFzcHhkZBgFBV5jdGwwMCRTUFdlYlBhcnRNYW5hZ2VyMSRBY2NvdW50TG9naW5XZWJwYXJ0Q29udHJvbCRjdGwwMCR1Y0luZm9ybWF0aW9uTWVzc2FnZSRsc3RWSW5mb01lc3NhZ2VzDzwrAAoCBxQrAAFkCAIBZAV+Y3RsMDAkU1BXZWJQYXJ0TWFuYWdlcjEkQWNjb3VudExvZ2luV2VicGFydENvbnRyb2wkY3RsMDAkd2VicGFydEFub255bW91c1VzZXJMb2dpbiRjdGwwMCR1Y0luZm9ybWF0aW9uTWVzc2FnZSRsc3RWSW5mb01lc3NhZ2VzD2dkBX9jdGwwMCRTUFdlYlBhcnRNYW5hZ2VyMSRBY2NvdW50TG9naW5XZWJwYXJ0Q29udHJvbCRjdGwwMCR3ZWJwYXJ0UmVnaXN0ZXJlZFVzZXJMb2dpbiRjdGwwMCR1Y0luZm9ybWF0aW9uTWVzc2FnZSRsc3RWSW5mb01lc3NhZ2VzD2dkBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgU5Y3RsMDAkUGxhY2VIb2xkZXJTaXRlTG9nbyRDYXJkQ1NpdGVMb2dvJGltYWdlYnV0dG9uU2VhcmNoBTdjdGwwMCRQbGFjZUhvbGRlclNpdGVMb2dvJENhcmRDU2l0ZUxvZ28kaW1hZ2VidXR0b25Mb2dvBWxjdGwwMCRTUFdlYlBhcnRNYW5hZ2VyMSRBY2NvdW50TG9naW5XZWJwYXJ0Q29udHJvbCRjdGwwMCR3ZWJwYXJ0UmVnaXN0ZXJlZFVzZXJMb2dpbiRjdGwwMCR3aXphcmRSZWdpc3RlclVzZXIPD2RmZFiUFjdstXs/gN2EEAGzp+nxIJ/V",
        "__EVENTVALIDATION":"/wEWDgKo8PCDDALF5PS7CAK05rSuCwKKpM+pCwKhsI3RAgLimtuvBgLj26T2BgLp4sXIDgKKwvuCBwKXmOToCAL8jMzRDAKLkOH9DgKIrZ7NDgKHrORNyr/X1zbOnkgjU21du0R3Wh8i58g=",
        "ctl00$SPWebPartManager1$AccountLoginWebpartControl$ctl00$webpartRegisteredUserLogin$ctl00$textboxRegisteredLogin":username,
        "ctl00$SPWebPartManager1$AccountLoginWebpartControl$ctl00$webpartRegisteredUserLogin$ctl00$textboxPassword":password,
        "ctl00$SPWebPartManager1$AccountLoginWebpartControl$ctl00$webpartRegisteredUserLogin$ctl00$buttonSubmit":"Log In",
    }
    headers = {"Content-Type":"application/x-www-form-urlencoded"}

    response = requests.post(login, data=formData, headers=headers)
    soup = bs(response.text, "html.parser")

    balance = soup.find(id="ctl00_SPWebPartManager1_AFMSCardSummaryWebpart_ctl00_wizardCardSummary_labelDisplayBalance").text
    #requests.post(slack, data=json.dumps({"text": "Your presto balance is %s" % balance}))
    return str("Your presto balance is %s" % balance)
