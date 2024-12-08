#
# Client-side python app for photoapp, this time working with
# web service, which in turn uses AWS S3 and RDS to implement
# a simple photo application for photo storage and viewing.
#
# Authors:
#   
#   Wilson Ting
#
#   Starter code: Prof. Joe Hummel
#   Northwestern University
#

import requests  # calling web service
import jsons  # relational-object mapping

import uuid
import pathlib
import logging
import sys
import os
import base64
import time
import numpy as np
from scipy.ndimage import convolve
from configparser import ConfigParser
from PIL import Image
from io import BytesIO



# doesn't work in docker (not easily):
# import matplotlib.pyplot as plt
# import matplotlib.image as img


###################################################################
#
# classes
#
class User:
  userid: int  # these must match columns from DB table
  email: str
  lastname: str
  firstname: str
  bucketfolder: str


class Asset:
  assetid: int  # these must match columns from DB table
  userid: int
  assetname: str
  bucketkey: str


class BucketItem:
  Key: str
  LastModified: str
  ETag: str
  Size: int
  StorageClass: str

def web_service_post(url, data):
  
  try:
    retries = 0
    
    while True:
      response = requests.post(url,json=data)
        
      if response.status_code in [200, 400, 500]:
        #
        # we consider this a successful call and response
        #
        break;

      #
      # failed, try again?
      #
      retries = retries + 1
      if retries < 3:
        # try at most 3 times
        time.sleep(retries)
        continue
          
      #
      # if get here, we tried 3 times, we give up:
      #
      break

    return response

  except Exception as e:
    print("**ERROR**")
    logging.error("web_service_put() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return None


def web_service_put(url, data):
  
  try:
    retries = 0
    
    while True:
      response = requests.put(url,json=data)
        
      if response.status_code in [200, 400, 500]:
        #
        # we consider this a successful call and response
        #
        break;

      #
      # failed, try again?
      #
      retries = retries + 1
      if retries < 3:
        # try at most 3 times
        time.sleep(retries)
        continue
          
      #
      # if get here, we tried 3 times, we give up:
      #
      break

    return response

  except Exception as e:
    print("**ERROR**")
    logging.error("web_service_put() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return None

###################################################################
#
# web_service_get
#
# When calling servers on a network, calls can randomly fail. 
# The better approach is to repeat at least N times (typically 
# N=3), and then give up after N tries.
#
def web_service_get(url):
  """
  Submits a GET request to a web service at most 3 times, since 
  web services can fail to respond e.g. to heavy user or internet 
  traffic. If the web service responds with status code 200, 400 
  or 500, we consider this a valid response and return the response.
  Otherwise we try again, at most 3 times. After 3 attempts the 
  function returns with the last response.
  
  Parameters
  ----------
  url: url for calling the web service
  
  Returns
  -------
  response received from web service
  """

  try:
    retries = 0
    
    while True:
      response = requests.get(url)
        
      if response.status_code in [200, 400, 500]:
        #
        # we consider this a successful call and response
        #
        break;

      #
      # failed, try again?
      #
      retries = retries + 1
      if retries < 3:
        # try at most 3 times
        time.sleep(retries)
        continue
          
      #
      # if get here, we tried 3 times, we give up:
      #
      break

    return response

  except Exception as e:
    print("**ERROR**")
    logging.error("web_service_get() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return None


###################################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """

  try:
    print()
    print(">> Enter a command:")
    print("   0 => end")
    print("   1 => stats")
    print("   2 => users")
    print("   3 => assets")
    print("   4 => download")
    print("   5 => download and display")
    print("   6 => bucket contents")
    print("   7 => add user")
    print("   8 => upload")
    print("   9 => get image description")
    print("   10 => play trivia with ChatGPT")
    print("   11 => filter an image")

    cmd = int(input())
    return cmd

  except Exception as e:
    print("ERROR")
    print("ERROR: invalid input")
    print("ERROR")
    return -1


###################################################################
#
# stats
#
def stats(baseurl):
  """
  Prints out S3 and RDS info: bucket status, # of users and 
  assets in the database
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/stats'
    url = baseurl + api

    # res = requests.get(url)
    res = web_service_get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # deserialize and extract stats:
    #
    body = res.json()
    #
    print("bucket status:", body["message"])
    print("# of users:", body["db_numUsers"])
    print("# of assets:", body["db_numAssets"])

  except Exception as e:
    logging.error("stats() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# users
#
def users(baseurl):
  """
  Prints out all the users in the database
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/users'
    url = baseurl + api

    # res = requests.get(url)
    res = web_service_get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # deserialize and extract users:
    #
    body = res.json()
    #
    # let's map each dictionary into a User object:
    #
    users = []
    for row in body["data"]:
      user = jsons.load(row, User)
      users.append(user)
    #
    # Now we can think OOP:
    #
    for user in users:
      print(user.userid)
      print(" ", user.email)
      print(" ", user.lastname, ",", user.firstname)
      print(" ", user.bucketfolder)

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# assets
#
def assets(baseurl):
  """
  Prints out all the assets in the database
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/assets'
    url = baseurl + api

    # res = requests.get(url)
    res = web_service_get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # deserialize and extract assets:
    #
    body = res.json()
    #
    # let's map each dictionary into an Asset object:
    #
    assets = []
    for row in body["data"]:
      asset = jsons.load(row, Asset)
      assets.append(asset)
    #
    # Now we can think OOP:
    #
    for asset in assets:
      print(asset.assetid)
      print(" ", asset.userid)
      print(" ", asset.assetname)
      print(" ", asset.bucketkey)

  except Exception as e:
    logging.error("assets() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# download
#
def download(baseurl, display=False):
  """
  Prompts the user for an asset id, and downloads
  that asset (image) from the bucket. Displays the
  image after download if display param is True.
  
  Parameters
  ----------
  baseurl: baseurl for web service,
  display: optional param controlling display of image
  
  Returns
  -------
  nothing
  """

  try:
    print("Enter asset id>")
    assetid = input()

    #
    # call the web service:
    #
    api = '/image'
    url = baseurl + api + '/' + assetid

    # res = requests.get(url)
    res = web_service_get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print(body["message"])
      #
      return

    #
    # deserialize and extract image:
    #
    body = res.json()

    #
    # TODO:
    #
    userid = body["user_id"]
    assetname = body["asset_name"] 
    bucketkey = body["bucket_key"]
    bytes = base64.b64decode(body["data"])

    print("userid:", userid)
    print("asset name:", assetname)
    print("bucket key:", bucketkey)

    #
    # write the binary data to a file (as a
    # binary file, not a text file):
    #
    # TODO
    #
    outfile = open(assetname, "wb")
    outfile.write(bytes)
    print("Downloaded from S3 and saved as '", assetname, "'")

    #
    # display image if requested:
    #
    if display:
      print('Oops...')
      print('Docker is not setup to display images, see if you can open and view locally...')
      print('Oops...')
      # image = img.imread(assetname)
      # plt.imshow(image)
      # plt.show()

  except Exception as e:
    logging.error("download() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# bucket_contents
#
def bucket_contents(baseurl):
  """
  Prints out the contents of the S3 bucket
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/bucket'
    url = baseurl + api

    #
    # we have to loop since data is returned page
    # by page:
    #
    lastkey = ""
    
    while True:
      #
      # make a request...
      # check status code, if failed break out of loop
      # any data? if not, break out of loop
      # display data
      #
      res = web_service_get(url)
      if res.status_code != 200:
        # failed:
        print("Failed with status code:", res.status_code)
        print("url: " + url)
        if res.status_code in [400, 500]:  # we'll have an error message
          body = res.json()
          print("Error message:", body["message"])
        #
        break
      #
      # deserialize and extract image:
      #
      body = res.json()
      page_size = len(body['data'])

      lastkey = body['data'][page_size-1]["Key"]
      for i in body['data']:
        print(f"{i['Key']}")
        print(f"  {i['LastModified']}")
        print(f"  {i['Size']}")
      if page_size < 12:
        break
      #
      # prompt...
      # if 'y' then continue, else break
      #
      print("another page? [y/n]")
      answer = input()
      #
      if answer == 'y':
        # add parameter to url
        url = baseurl + api
        url += "?startafter=" + lastkey
        #
        continue
      else:
        break

  except Exception as e:
    logging.error("bucket_contents() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# add_user
#
def add_user(baseurl):
  """
  Prompts the user for the new user's email,
  last name, and first name, and then inserts
  this user into the database. But if the user's
  email already exists in the database, then we
  update the user's info instead of inserting
  a new user.
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    print("Enter user's email>")
    email = input()

    print("Enter user's last (family) name>")
    last_name = input()

    print("Enter user's first (given) name>")
    first_name = input()

    # generate unique folder name:
    folder = str(uuid.uuid4())

    data = {
      "email": email,
      "lastname": last_name,
      "firstname": first_name,
      "bucketfolder": folder
    }

    #
    # build the data packet:
    #
    # TODO
    #

    #
    # call the web service:
    #
    api = '/user'
    url = baseurl + api
    #
    # TODO
    #
    res = web_service_put(url,data)
    #

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # success, extract userid:
    #
    body = res.json()

    userid = body["userid"]
    message = body["message"]

    print("User", userid, "successfully", message)

  except Exception as e:
    logging.error("add_user() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# upload
#
def upload(baseurl):
  """
  Prompts the user for a local filename and user id, 
  and uploads that asset (image) to the user's folder 
  in the bucket. The asset is given a random, unique 
  name. The database is also updated to record the 
  existence of this new asset in S3.
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    print("Enter local filename>")
    local_filename = input()

    if not pathlib.Path(local_filename).is_file():
      print("Local file '", local_filename, "' does not exist...")
      return

    print("Enter user id>")
    userid = input()

    #
    # build the data packet:
    #
    infile = open(local_filename, "rb")
    bytes = infile.read()
    infile.close()

    #
    # now encode the image as base64. Note b64encode returns
    # a bytes object, not a string. So then we have to convert
    # (decode) the bytes -> string, and then we can serialize
    # the string as JSON for upload to server:
    #
    data = base64.b64encode(bytes)
    datastr = data.decode()

    data = {"assetname": local_filename, "data": datastr}

    #
    # call the web service:
    #
    api = '/image'
    url = baseurl + api + "/" + userid

    res = web_service_post(url, data)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # success, extract userid:
    #
    body = res.json()

    assetid = body["assetid"]

    print("Image uploaded, asset id =", assetid)

  except Exception as e:
    logging.error("upload() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


def trivia(baseurl):
  """
  Prompts the user with a trivia question from ChatGPT and checks the answer.
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/trivia'
    url = baseurl + api

    res = web_service_get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # deserialize and extract question:
    #
    body = res.json()
    question = body["question"]

    print("Trivia question:", question)
    print("Enter your answer>")
    user_answer = input().strip().lower()

    #
    # call ChatGPT to get the correct answer:
    #
    api = '/trivia/answer'
    url = baseurl + api
    data = {"question": question, "user_answer": user_answer}

    res = web_service_post(url, data)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # success, extract result:
    #
    body = res.json()
    correct_answer = body["correct_answer"]
    result = body["result"]

    if result:
      print("Correct! The answer is:", correct_answer)
    else:
      print("Incorrect. The correct answer is:", correct_answer)

  except Exception as e:
    logging.error("trivia() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
  

def describe_image(baseurl, display=False):
  
  """
  Prompts the user for an asset id, and downloads
  that asset (image) from the bucket. Displays the
  image after download if display param is True.
  
  Parameters
  ----------
  baseurl: baseurl for web service,
  display: optional param controlling display of image
  
  Returns
  -------
  nothing
  """

  try:
    print("Enter asset id>")
    assetid = input()

    #
    # call the web service:
    #
    api = '/project_function_1'
    url = baseurl + api + '/' + assetid

    # res = requests.get(url)
    res = web_service_get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print(body["message"])
      #
      return

    #
    # deserialize and extract image:
    #
    body = res.json()

    #
    # TODO:
    #
    image_description = body["image_description"]
    assetname = body["asset_name"] 

    print("image description:", image_description)

    assetname = os.path.splitext(assetname)[0] + '.txt'

    # Open the file in write mode (text mode)
    outfile = open(assetname, "w")

    # Write the description to the file
    outfile.write(image_description)

    # Close the file after writing
    outfile.close()

    # Print a confirmation message
    print("Image description saved as '", assetname, "'")
    #
    # display image if requested:
    #
    if display:
      print('Oops...')
      print('Docker is not setup to display images, see if you can open and view locally...')
      print('Oops...')
      # image = img.imread(assetname)
      # plt.imshow(image)
      # plt.show()

  except Exception as e:
    logging.error("describe_image() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
  
def project_function_3(baseurl):
  try:
    print("Enter asset id>")
    assetid = input()
    api = '/image'
    url = baseurl + api + '/' + assetid
    res = web_service_get(url)
    if res.status_code != 200:
      # failed:
      if res.status_code in [400, 500]:  # we'll have an error message
        body = res.json()
        print(body["message"])
      return

    body = res.json()

    userid = body["user_id"]
    assetname = body["asset_name"] 
    bucketkey = body["bucket_key"]
    bytes = base64.b64decode(body["data"])

    print("userid:", userid)
    print("asset name:", assetname)
    print("bucket key:", bucketkey)
    image = Image.open(BytesIO(bytes))
    image_array = np.array(image)
    filters = {
      "smoothing": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9,  # Average filter
      "edge_detection": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),  # Laplacian kernel
      "sharpening": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Sharpening kernel
    }
    print("Enter one of the three following filters: smoothing, edge_detection, sharpening>")
    filter = input()
    kernel = filters[filter]
    filtered_channels = [convolve(image_array[:, :, i], kernel) for i in range(3)]
    filtered_image = np.stack(filtered_channels, axis=-1).clip(0, 255).astype("uint8")
    output_image = Image.fromarray(filtered_image)
    buffer = BytesIO()
    output_image.save(buffer, format="PNG")  # You can use "JPEG" or other formats
    filtered_image_bytes = buffer.getvalue()
    file_name = filter + "_filtered_" + assetname
    outfile = open(file_name, "wb")
    outfile.write(filtered_image_bytes)
    print("Downloaded from S3, filtered, and saved as '", file_name, "'")

    data = base64.b64encode(filtered_image_bytes)
    datastr = data.decode()

    data = {"assetname": file_name, "data": datastr}
    #
    # call the web service:
    #
    api = '/image'
    url = baseurl + api + "/" + str(userid)
    res2 = web_service_post(url, data)


    #
    # let's look at what we got back:
    #
    if res2.status_code != 200:
      # failed:
      print("Failed with status code:", res2.status_code)
      print("url: " + url)
      if res2.status_code in [400, 500]:  # we'll have an error message
        body2 = res2.json()
        print("Error message:", body2["message"])
      #
      return

    body2 = res2.json()

    assetid2 = body2["assetid"]

    print("Filtered image uploaded, asset id = ", assetid2)
    
  except Exception as e:
    logging.error("project_function_3() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

#########################################################################
# main
#
print('** Welcome to PhotoApp v2 **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'photoapp-client-config.ini'

print("What config file to use for this session?")
print("Press ENTER to use default (photoapp-client-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
  pass  # already set
else:
  config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
  print("**ERROR: config file '", config_file, "' does not exist, exiting")
  sys.exit(0)

#
# setup base URL to web service:
#
configur = ConfigParser()
configur.read(config_file)
baseurl = configur.get('client', 'webservice')

#
# make sure baseurl does not end with /, if so remove:
#
if len(baseurl) < 16:
  print("**ERROR**")
  print("**ERROR: baseurl '", baseurl, "' in .ini file is empty or not nearly long enough, please fix")
  sys.exit(0)

if baseurl.startswith('https'):
  print("**ERROR**")
  print("**ERROR: baseurl '", baseurl, "' in .ini file starts with https, which is not supported (use http)")
  sys.exit(0)

lastchar = baseurl[len(baseurl) - 1]
if lastchar == "/":
  baseurl = baseurl[:-1]

# print(baseurl)

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
  #
  if cmd == 1:
    stats(baseurl)
  elif cmd == 2:
    users(baseurl)
  elif cmd == 3:
    assets(baseurl)
  elif cmd == 4:
    download(baseurl)
  elif cmd == 5:
    download(baseurl)
  elif cmd == 6:
    bucket_contents(baseurl)
  elif cmd == 7:
    add_user(baseurl)
  elif cmd == 8:
    upload(baseurl)
  elif cmd == 9:
    describe_image(baseurl)
  elif cmd == 10:
    trivia(baseurl)
  elif cmd == 11:
    project_function_3(baseurl)
  else:
    print("** Unknown command, try again...")
  #
  cmd = prompt()

#
# done
#
print()
print('** done **')
