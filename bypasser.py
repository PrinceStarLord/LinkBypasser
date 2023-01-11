from dotenv import load_dotenv
load_dotenv()
import PyBypass


# don't need to change this code

ddllist = ["shareus.io"]

# follow on GitHub BotCreator99

def shareus(url):
  token = url.split("=")[-1]
  bypassed_url = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid=" + token
  response = requests.get(bypassed_url).text
  return response
  
# end of code



# check if present in list
def ispresent(inlist, url):
  for ele in inlist:
    if ele in url:
      return True
  return False


# shortners
def shortners(url):

  

  # shareus
  if "https://shareus.io/" in url:
    print("entered shareus:", url)
    return shareus(url)

  # else
  else:
    temp = PyBypass.bypass(url)
    if temp != None: return temp
    else: return "😒 Not in Supported Links"



