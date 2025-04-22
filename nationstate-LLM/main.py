

from home.tasks import *
import openai
import os
import openai
import time
# openai.organization = "DARCY_LIU_NS"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()


def issues(gptnationstate):
    from bs4 import BeautifulSoup

    # Your XML-like data
    xml_data = (gptnationstate.get_nation_issues())
    # print(xml_data)
    # Parse the XML-like data using BeautifulSoup
    soup = BeautifulSoup(xml_data, 'xml')

    # Find all ISSUE elements
    issue_elements = soup.find_all('ISSUE')

    # Create a list to store issue objects
    issues = []

    # Loop through the ISSUE elements
    
    for issue_element in issue_elements:
        issue_id = issue_element.get('id')
        title = issue_element.find('TITLE').text
        text = issue_element.find('TEXT').text
        # author = issue_element.find('AUTHOR').text
        # editor = issue_element.find('EDITOR').text
        # pic1 = issue_element.find('PIC1').text
        # pic2 = issue_element.find('PIC2').text
        options_find = issue_element.find_all('OPTION')
        options = []
        # for inconsistant policy order: Some skip some indicies, thus I need to add.
        cur_options_id = 0
        
        for opt in options_find:
            while cur_options_id < int(opt["id"]):
                options.append({"role": "user", "content": f'OPTION-{cur_options_id}: NO OPTION'})
                cur_options_id += 1
            # cur_options_id == int(opt["id"])
            options.append({"role": "user", "content": f'OPTION-{opt["id"]}: {opt.text}'})
            cur_options_id += 1
        option_count = max([int(opt["id"]) for opt in issue_element.find_all('OPTION')])
        # Create a dictionary to represent the issue
        issue = {
            'id': issue_id,
            'title': title,
            'text': text,
            'options': options, # This is a list of dictionaries representing the options
            'option_count': option_count,
            # 'author': author,
            # 'editor': editor,
            # 'pic1': pic1,
            # 'pic2': pic2

        }

        # Append the issue dictionary to the list of issues
        issues.append(issue)
    return issues





# given a string starting with OPTION-#
# return the number
# str = 'OPTION-1:xxxx'
# the max is inclusive
def get_option(str, max=5):
    # turn str to lowercase
    str = str.lower()
    for i in range(0, max + 1):
        if str.startswith(f'option-{i}'):
            return i
    # if not found keep looking
    return get_option(str[1:])

def obtain_option(analysis):
    return analysis

def run_issues(nation, issue_list):
    # read the text file and print its contents
    AIPurpose = open('../media/NationFramework/AIPurpose.txt', 'r').read().replace('\n', '')
    constitution = open('../media/NationFramework/Constitution.txt', 'r').read().replace('\n', '')
    ideas = open('../media/NationFramework/ideas.txt', 'r').read().replace('\n', '')
    values = open('../media/NationFramework/values.txt', 'r').read().replace('\n', '')
    news = open('../media/NationFramework/News.txt', 'r').read().replace('\n', '')
    # Now, 'issues' list contains dictionaries representing each issue
    # You can access issue information like this:
    for issue in issue_list:
        # At this point This is where my program would be making the decisions
        # I want to abolish
        # ritual sacrifice,
        # vat grown people,
        # compulsory organ harvesting,
        # Socialism,
        messages = ([
                {"role": "system", "content": f"MEMBER STATE: {nation.NATION}"},
                {"role": "system", "content": AIPurpose},
                {"role": "system", "content": constitution},
                {"role": "system", "content": ideas},
                {"role": "system", "content": values},
                {"role": "system", "content": news},
                {"role": "user", "content": f"GIVEN ISSUE: TITLE: { issue['title']} CONTENT: {issue['text']}"},
            ] + issue['options'] +
            [
                {"role": "assistant", "content": "What is the best option?"},
            ])
        #print(messages)
        print(f"TITLE:{issue['title']}")
        print(f"ISSUE:{issue['id']} {issue['text']}")

        options_str = ""
        for option in issue['options']:
            options_str += option['content'] + "\n"
        print(options_str)


        if issue['id'] == 333:
                response = "OPTION-0"
        else:
            response = openai.ChatCompletion.create(
                # model="gpt-3.5-turbo-0613",
                model="gpt-4-0613",
                messages=messages)


        print(response)
        analysis = response['choices'][0]['message']['content']
        # write issue description
        # get datetime


        # now call another model that tells which option to pick
        # get the first option

        # this would always begin with "OPTION-#:"
        reply_msg = obtain_option(analysis)
        # add_to_file(f"outputs/{nation.NATION}/{(current_date)}/{issue['id']}/responses.txt", f"ISSUE:{issue['id']} {reply_msg} \n")

        print(f"ISSUE:{issue['id']} {reply_msg}")
        issuecomplete_response = nation.address_issue(issue['id'],
                                                      get_option(reply_msg, issue['option_count']))
        if not issuecomplete_response:
            print(f"NATION: {nation.NATION}\nNO ISSUE {issue['id']} CHOICE: {get_option(reply_msg, issue['option_count'])} ADDRESSED: {reply_msg}")
            continue
        print(f"ISSUE {issuecomplete_response['issue']['id']} CHOICE: {issuecomplete_response['issue']['choice']} ADDRESSED: {issuecomplete_response['issue']['desc']}")
        # if directory do not exist then make it
        current_date = time.strftime("%Y-%m-%d")
        if not os.path.exists(f"../media/data/issue/{nation.NATION}/{(current_date)}"):
            os.makedirs(f"../media/data/issue/{nation.NATION}/{(current_date)}")
        add_to_file(f"../media/data/issue/{nation.NATION}/{(current_date)}/{issue['id']}.txt",
                    f"ISSUE:\n{issue['id']}\nTEXT:\n{issue['text']}\nOPTIONS:\n{options_str}")
        
        if not os.path.exists(f"../media/data/outputs/{nation.NATION}/{(current_date)}"):
            os.makedirs(f"../media/data/outputs/{nation.NATION}/{(current_date)}")
        add_to_file(f"../media/data/outputs/{nation.NATION}/{(current_date)}/{issue['id']}.txt",
                    f"issuecomplete_response:\n{issuecomplete_response}")
        
        if not os.path.exists(f"../media/data/analysis/{nation.NATION}/{(current_date)}"):
            os.makedirs(f"../media/data/analysis/{nation.NATION}/{(current_date)}")
        add_to_file(f"../media/data/analysis/{nation.NATION}/{(current_date)}/{issue['id']}.txt",
                    f"ANALYSIS:\n{analysis}")

        time.sleep(60)

from nations import nations
if __name__ == '__main__':
    #Region: https://www.nationstates.net/region=isles_of_codist_gptesta
    # print the current date and time and year
    print("Current date and time and year is: ", end="")
    print(time.asctime(time.localtime(time.time())))
    for nation in nations:
        print(f"================================ {nation.NATION} ================================")
        issue_list = issues(nation)
        # run_issues(nation, issue_list)



