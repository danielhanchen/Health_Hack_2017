
# coding: utf-8

# In[325]:

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from numpy import arange
import re
from unicodedata import normalize as clean
from pandas import *
remove = '\<.*?\>'

def process(string):
    return clean('NFKD',re.sub(remove, '', string)).lstrip().rstrip().replace('\t','')


data = {}

for rows in arange(0,1000,15):
    site = 'https://www.grants.gov.au/?keyword=&GOID=&startRow={}&orderBy=Close%20Date%20%26%20Time%20-%20Ascending&event=public%2EGO%2Elist'.format(rows)
    
    try:
        html = soup(urlopen(site))
        
        if 'There are no results that match your selection' in str(html):
            print("Finished")
            break
        else:
            text = str(html.find_all('div')).split('<div class="box boxY r9">')[1:]

            text = [x for x in text if len(x)>200]
            for each in text:
                result = {}

                result["Title"] = each.split('</p>')[0].split('>')[-1]
                result["Go_id"] = each.split('</a>')[0].split('>')[-1]
                result["Deadline"] = each.split('\t\t')[1].split('\n')[0].lstrip().rstrip()
                if result["Deadline"] == '':
                    result["Deadline"] = 'NOT SURE'
                    
                result["Agency"] = each.split('inner">')[3].split('</')[0]
                result["Category"] = [each.split('inner">')[4].split('</')[0]]

                details_code = each.split('./?')[1].split('"')[0].split('=')[2]

                full_details = str(soup(urlopen('https://www.grants.gov.au/?event=public.GO.show&GOUUID={}'.format(details_code))).find_all('div'))
                full_details = full_details.split('box boxW r9 listInner')[1]

                try:
                    result["Category"].append(full_details.split('Secondary Category')[1].split('</div')[0].split('-desc-inner">')[1])
                except:
                    pass

                for want in ["Internal Reference ID", "Publish Date"]:
                    try:
                        result[want] = process(full_details.split(want)[1].split('</')[1].split('>')[-1].lstrip().rstrip())
                    except:
                        result[want] = "NULL"

                need = ["Description", "Eligibility", "Instructions for Lodgement"]
                for x,y in zip(need, need[1:]):
                    result[x] = process(full_details.split(x)[1].split(y)[0].split('<div class="list-desc-inner">')[1].split('</div>')[0]                                .replace('<p>','').replace('</p>',' ').rstrip().replace('\n',' '))

                result['Instructions for Lodgement'] = process(full_details.split("Instructions for Lodgement")[1].split('</div>')[0].split('"list-desc-inner">')[1]                        .replace('<p>','').replace('</p>',' ').rstrip().replace('\n',' '))

                try:
                    result['Description'] += "\nGrant Activity Timeframe = "
                    result['Description'] += process(full_details.split("Grant Activity Timeframe")[1].split('</div>')[0].split('"list-desc-inner">')[1]                        .replace('<p>','').replace('</p>',' ').rstrip().replace('\n',' '))
                except:
                    result['Description'] += "NULL"

                try:
                    result['Instructions for Lodgement'] += "\nOther Instructions = "
                    result['Instructions for Lodgement'] += process(full_details.split("Other Instructions")[1].split('</div>')[0].split('"list-desc-inner">')[1]                        .replace('<p>','').replace('</p>',' ').rstrip().replace('\n',' '))
                except:
                    result['Instructions for Lodgement'] += "NULL"

                try:
                    result['Description'] += "\nAddenda Available = "
                    result['Description'] += process(full_details.split("Addenda Available")[1].split('</div>')[0].split('"list-desc-inner">')[1]                        .replace('<p>','').replace('</p>',' ').rstrip().replace('\n',' '))
                except:
                    result['Description'] += "NOT SURE"

                result['Total Grant Amount'] = "NOT SURE"
                try:
                    result['Total Grant Amount'] = process(full_details.split("Total Amount Available")[1].split('</div>')[0].split('"list-desc-inner">')[1]                        .replace('<p>','').replace('</p>',' ').rstrip().replace('\n',' '))
                except:
                    pass

                result['Estimated Grant Value'] = "NOT SURE"
                try:
                    result['Estimated Grant Value'] = process(full_details.split("Estimated Grant Value")[1].split('</div>')[0].split('"list-desc-inner">')[1]                        .replace('<p>','').replace('</p>',' ').rstrip().replace('\n',' '))
                except:
                    pass

                try:
                    result['Email'] = process(full_details.split("Contact Details")[1].split('title')[1].split('>')[1].split('<')[0])
                    result["Site"] = process(full_details.split("Contact Details")[1].split('href')[2].split('="')[1].split('">')[0])
                except:
                    result['Email'] = process(full_details.split("Contact Details")[2].split('href')[1].split('"')[1].split(':')[1])
                    result["Site"] = process(full_details.split("Contact Details")[2].split('href')[2].split('="')[1].split('">')[0])

                data[result["Title"]] = result
    except:
        print("Finished")
        break


# In[326]:

table = DataFrame(data).T
table.to_json(path_or_buf = "Aus Gov Grants.json", orient = 'table')

table["From where"] = "www.grants.gov.au"


# In[327]:

site = "https://www.dementiaresearchfoundation.org.au/research-grants"

html = soup(urlopen(site))
text = str(html.find_all('div')).split('<div class="field-item even" property="content:encoded">')        [1].split('<h2>')[1:-1]


# In[328]:

table["New Grants"] = 1


# In[329]:

data = {}

for grant in text:
    result = {}

    result["Title"] = process(grant.split('</h2>')[0])
    result['Description'] = process(grant.split('</h2>')[1])
    result["Agency"] = "Dementia Australia Research Foundation"

    result["Category"] = ["231013 - Medical Research",
                          '171004 - Services for People with Disabilities']

    result['Estimated Grant Value'] = result["Description"].split('$')[1].split(' ')[0]

    result['Publish Date'] = result["Title"].split(' ')[0]

    result["Site"] = 'https://www.dementiaresearchfoundation.org.au/research-grants'
    result["From where"] = 'www.dementiaresearchfoundation.org.au'

    result['Internal Reference ID'] = 'NULL'

    result["Go_id"] = "NULL"
    result["Eligibility"] = "NOT SURE"

    result["New Grants"] = 0
    result['Instructions for Lodgement'] = "NOT SURE"
    result['Email'] = "NULL"
    result['Total Grant Amount'] = "NOT SURE"
    result['Deadline'] = "CLOSED"
    
    data[result["Title"]] = result


# In[330]:

revs = []
for x in table['Estimated Grant Value'].values:
    if x != 'NOT SURE':
        ranges = x.split('From')[-1]
        rev = ranges.split('to')[-1].replace(',','').replace('$','')             .replace('.00','')
        revs.append(int(rev.rstrip().lstrip()))
    else:
        revs.append('NOT SURE')

total = []
for u in revs:
    if u != 'NOT SURE':
        if u >= 500000: u = "HIGH"
        elif u >= 100000: u = "MEDIUM"
        else: u = "LOW"
    total.append(u)
    
table["Grant Range"] = total


# In[331]:

table2 = DataFrame(data).T

table = concat([table,table2])

table.to_json(path_or_buf = "Aus Gov Grants.json", orient = 'table')


# In[332]:

site = "https://www.curebraincancer.org.au/page/197/funding-options"

html = soup(urlopen(site))
text = str(html.find_all('div')).split('<div class="cms-inner">')


# In[333]:

text3 = text[1].split('DONATE')[0].split('<h3><a id="')[1:]

text3 = [x.split('name=')[-1] for x in text3]
data ={}

for grant in text3:
    result = {}
    result["Title"] = grant.split('"')[1]

    result["Deadline"] = grant.split('ff0000">')[1].split('</')[0]
    result['Agency'] = "Cure Brain Cancer Org"

    result['Category'] = ['231013 - Medical Research', '231004 - Cancer']

    result['Description'] = grant.split('</p>\n<p>')[1].split('</p>')[0]

    result['Eligibility'] = process(grant.split('Eligibility')[1].split('underline">')[1])

    result['Estimated Grant Value'] = grant.split('Funding Details')[1].split('">')[1].split('</p>')[0]

    result["Site"] = 'https://www.curebraincancer.org.au/page/197/funding-options'
    result["From where"] = 'www.curebraincancer.org.au'

    result["Go_id"] = "NULL"
    result['Internal Reference ID'] = "NULL"
    result['Instructions for Lodgement'] = "NULL"
    result['New Grants'] = (1-('Deadline passed' in grant)*1)

    result['Publish Date'] = text[1].split('Opportunities')[0].split('<h1>')[-1].lstrip().rstrip()

    result['Total Grant Amount'] = "NOT SURE"
    
    data[result['Title']] = result


# In[334]:

totals = []
table3 = DataFrame(data).T

for y in table3['Estimated Grant Value']:
    try:
        totals.append(sum([int(x.split(' ')[0].replace(',','')) 
                       for x in y.split('$')[1:]]))
    except:
        totals.append('NOT SURE')
table3['Estimated Grant Value'] = totals

total = []
for u in totals:
    if u != 'NOT SURE':
        if u >= 500000: u = "HIGH"
        elif u >= 100000: u = "MEDIUM"
        else: u = "LOW"
    total.append(u)
    
table3["Grant Range"] = total

table = concat([table,table3])

table.to_json(path_or_buf = "Aus Gov Grants.json", orient = 'table')


# In[362]:

site = 'https://www.business.gov.au/assistance/results?q='

html = soup(urlopen(site))
text = str(html.find_all('div')).split(
    '<div class="search-result-card__content">')[1:][0:-1]


# In[414]:

data = {}

for grant in text:
    result = {}
    result["Title"] = grant.split('<a href="/')[1].split('">')[1].split('</')[0]

    result["Description"] = process(grant.split('Open')[1].split('<h3>')[0])

    parra = grant.split('Who can apply')
    if len(parra) != 1:
        parra = process(parra[-1]).replace(':','').replace('\n\n','\n')
        result['Eligibility'] = parra
    else:
        result['Eligibility'] = "NOT SURE"

    result['Deadline'] = "2017"

    result['Agency'] = "Australian Government - Department for Business"

    result['Category'] = "Startups and Innovation"

    try:
        result['Estimated Grant Value'] = int(result["Description"].split("$")[-1].replace(' million',',000,000')        .split(' ')[0].replace(',',''))
    except:
        result['Estimated Grant Value'] = 'NOT SURE'
        
    result["From where"] = 'https://www.business.gov.au/assistance/results?q='

    result['Go_id'] = 'NULL'

    result['Internal Reference ID'] = "NULL"

    result['New Grants'] = 1
    result["Publish Date"] = '2017'

    result["Site"] = 'www.business.gov.au'

    result['Total Grant Amount'] = result['Estimated Grant Value']
    
    data[result["Title"]] = result

table4 = DataFrame(data).T
totals = table4["Estimated Grant Value"]

total = []
for u in totals:
    if u != 'NOT SURE':
        if u >= 500000: u = "HIGH"
        elif u >= 100000: u = "MEDIUM"
        else: u = "LOW"
    total.append(u)
    
table4["Grant Range"] = total


# In[416]:

table = concat([table,table4])

table.to_json(path_or_buf = "Aus Gov Grants.json", orient = 'table')


# In[336]:

lists = []
for u in table["Category"]:
    if len(u) != 1:
        for x in u:
            lists.append(x)
    else:
        lists.append(u[0])
        
Series(lists).unique()

