#written by sai teja using bottom up method
import json
from boltiot import Bolt,Email
import math
import time#will be used to create wait time for api
api_key = "72207486-0705-4f3c-a544-1dfa816db220"
device_id  = "BOLT14918157"
mybolt = Bolt(api_key, device_id)
#these values are obtained by inspection in main project:)
max_bound=12
min_bound=14
freq=10#give time in seconds
def std(data_frame):#used to calculate standard deviation
   k=len(data_frame)
   M=0
   for val in data_frame:
      M+=val
   M/=k
   ans=0
   for val in data_frame:
      ans+=(val-M)*(val-M)
   ans/=k
   ans=math.sqrt(ans)
   return ans
def bounds(history,frame_size,c_factor):#pass in history as an array to get bounds of next prediction(in form of array [lower_bound, upper_bound], if values are inconsistent you get false
   tot=len(history)
   if(tot<frame_size):
       return [False]
   else:
       ans=[]
       data_frame=history[tot-frame_size:tot]
       z_sigma=c_factor*std(data_frame)
       ans.append(True)
       ans.append(history[-1]-z_sigma)
       ans.append(history[-1]+z_sigma)
       return ans
def send_mail(mail_address,subject,content):#sends mail to a particular person
    mailer=Email('7f3791c8549c2fef2ff34b4d3432a10e-c485922e-f25eb8cb','sandbox1308a01f1332432d948d9d790a2ab5c5.mailgun.org','test@sandbox1308a01f1332432d948d9d790a2ab5c5.mailgun.org',mail_address)
    mailer.send_email(subject,content)
    
history=[]
while(True):
      response=mybolt.analogRead('A0')
      fin_res=json.loads(response)
      if fin_res['success']!=1:
         print('error reading::'+fin_res['value'])
         time.sleep(freq)
         continue
      data=0
      try:
         data=0.0977*int(fin_res['value'])
         history.append(data)
      except:
          print('error in value::'+e)
          time.sleep(freq)
          continue
      if (data>=max_bound):
          send_mail('tejavaranasi2003@gmail.com','alert','max temp crossed')
          time.sleep(freq)
          continue
      if  (data<min_bound):
          send_mail('tejavaranasi2003@gmail.com','alert','min temp breached')
          time.sleep(freq)
          continue
      bounnd=bounds(history,7,1)#frame size==7 , c factor==2
      if bound[0]==False:
         time.sleep(freq)
         continue
      if bound[0]==True:
           if (data>=bound[2]):
              send_mail('tejavaranasi2003@gmail.com','alert','someone opened fridge')
              print('someone opened fridge ??')
              time.sleep(freq)
              continue
           if (data<bound[1]):
              send_mail('tejavaranasi2003@gmail.com','alert','cooling overloaded')
              print('someone closed fridge ??')
              time.sleep(freq)
              continue
      time.sleep(freq)
      
      
      
      
    
