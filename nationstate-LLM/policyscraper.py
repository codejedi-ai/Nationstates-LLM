from bs4 import BeautifulSoup
import requests
# get the request from http://www.mwq.dds.nl/ns/results/policies.html#Theocracy
request = requests.get('http://www.mwq.dds.nl/ns/results/policies.html#Theocracy')
soup = BeautifulSoup(request.text, 'html.parser')
# print(soup.prettify())
# print(soup.find_all('table'))
policy = soup.find_all('table')[0]
policy_rows = policy.find_all('td')
# get the id of h2
print(policy.find('h2').get('id'))
# print(policy_rows[0])