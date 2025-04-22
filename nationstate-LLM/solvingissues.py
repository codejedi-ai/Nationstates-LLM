# Time Version
# Must be left running
import nationstates
import time
#When to rerun
#https://www.nationstates.net/page=show_dilemma/dilemma=1174
# I have to bitch code this
import requests
# get the environment variables from a .env file
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()
USERAGENT = "YOUR USERAGENT"
NATION = os.getenv("NATION")
X_PASSWORD = os.getenv("NATION_PASSWD")


def print_env():
    print(NATION, X_PASSWORD)
# need to reimplement address ISSUE

# get_nation_issues gets all the pending issues for nation
# curl -A "USERAGENT" "https://www.nationstates.net/cgi-bin/api.cgi?nation=darcy_liu&q=policies"
def get_nation_issues():
    url = f"https://www.nationstates.net/cgi-bin/api.cgi"
    headers = {
    "X-Password": X_PASSWORD,
    "User-Agent": "Nationstate LLM"
    }
    params = {
        "nation": NATION,
        "q": "issues"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.text
def address_issue(i,OPTION):
  api = nationstates.Nationstates(USERAGENT)
  nation = api.nation(NATION, password=X_PASSWORD)
  try:
      # Replace 'YourNationName' with your actual nation name
      # the API is 0 indexied
      issue = nation.pick_issue(issue_id = i,OPTION =OPTION - 1)
      return (issue)
  except:
      print(f"ERROR: Issue-{i} is not an issue encounterd by {NATION}")


# add to file
def add_to_file(file, str):
    with open(file, 'a') as f:
        f.write(str)
        f.write('\n')
        f.close()