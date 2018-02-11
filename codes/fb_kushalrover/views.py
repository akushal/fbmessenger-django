from django.shortcuts import render
import json
import pprint
from datetime import datetime
import json, requests, random, re
from pprint import pprint
# Create your views here.
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from json import dumps, loads

# Create your views here.
API_PAGE_FB="https://graph.facebook.com/v2.6/me/messages?access_token=<PAGE_TOKEN>"

def post_facebook_message(fbid, recevied_message):
    post_message_url = API_PAGE_FB
    resp = client.converse("123",recevied_message, {})
    print('Yay, got Wit.ai response: ' + str(resp))
    resp = resp['msg']
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":resp}})
    print (response_msg)
#        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        #pprint(status.json())


def interact(orig_message):
    GREETING_KEYWORDS = ("hello", "hi", "yo", "wawa", "korek", "ki pozition")

    GREETING_RESPONSES = ["emplass toi?", "hey", "Yo, how are you?", "hey bro, doing well?"]
    POST_GREETING  = ["How can I help you?", "I'm limited edition,", "Type 'Help'" ]

    GOODBYE_KEYWORDS = ("bye", "cya")
    GOODBYE_RESPONSES = ["BYE! :)", "A++", "Take care"]

    JOKE_RESPONSES = ["merry me!", "ta crapo"]
    message = orig_message.split()
    ans = ""
    for word in message:
        print ("Word is " + str(word))
        if word.lower() in GREETING_KEYWORDS:
                ans = ans + random.choice(GREETING_RESPONSES)
        elif word.lower() == "help":
                ans = "Commands: mytime, youJoke" 
        elif word.lower() == "mytime":
                ans = str(datetime.now())    
        elif word.lower() == "youJoke":
                ans = random.choice(JOKE_RESPONSES) 
        elif word.lower() in GOODBYE_KEYWORDS:

                ans = random.choice(GOODBYE_RESPONSES)
        else:
                ans = ans +  random.choice(POST_GREETING)
    print ("Ans from interact: " + ans)
    return ans

def chucknoris(messg):
    chuckurl = 'https://api.chucknorris.io/jokes/random'
    #chuckurl = 'https://api.chucknorris.io/jokes/search?query=' + messg
    replychuck = ''
    s = requests.Session()
    replyfromchuck = s.get(chuckurl, verify=False)
    print (replyfromchuck)
    replychuck = replyfromchuck.text
    data =  json.loads(replychuck)
    return data["value"]
 

 
def post_fb_custom_msg(fbid, received_message):
        post_message_url = API_PAGE_FB
        resp = interact(received_message)
        #resp = chucknoris(received_message)         
        print ("Response msg: " + str(resp))
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":resp}})
        print ("Response msg json: " + str(response_msg))
#        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        #pprint(status.json())


class KushalRoverView(generic.View):
    def get(self, request, *args, **kwargs):
     #   return HttpResponse("Hello World!")
           if self.request.GET['hub.verify_token'] == 'this_is_me_texting_myself':
                   return HttpResponse(self.request.GET['hub.challenge'])
           else:
                   return HttpResponse('Error, invalid token')
# The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                       pprint(  message)     
                       post_fb_custom_msg(message['sender']['id'], message['message']['text'])
            #post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()


