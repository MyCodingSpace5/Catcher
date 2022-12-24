from twilio.twiml.messaging_response import MessagingResponse
pnbeforeparse = input("Enter phone number so we can contact you DONT FORGET THE +1")
pnp = int(pnbeforeparse)
print("Setup is now loading the second stage of setup for your camera")
print("For the next stage of setup we need a twilio account so we can send sms to your phone in case of an emergency")
proceed = input("Do you wish to proceed? 1:Yes 2:No")
pp = int(proceed)
if(pp == 1):
    print("Great! Continuting on with setup")
else:
    exit()
twiloacountsid = input("Twilio account sid dont add the "" ")
twiloauthtoken = input("Twilio auth token dont add the "" ")
twilophonenumber = input("Twilio phone number")
import cv2
import matplotlib
import numpy
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
cam = cv2.VideoCapture(0)
import os
from twilio.rest import Client

account_sid = twiloacountsid
auth_token = twiloauthtoken
client = Client(account_sid, auth_token)
while(True):
    ret, frame = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=25)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) > 2500:
            continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            out.write(frame)
            message = client.messages.create(
                    body="Somebody unauthorized has entered your room",
                    from_=twilophonenumber,
                    to=pnbeforeparse
                )

    cv2.imshow('Catcher', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
