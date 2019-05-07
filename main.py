#Author: Thomas Nguyen

import csv
import bs4
import numpy

#########################################################################
## Import and enter txt file name here                                  # 
#                                                                       #
fn='NASDAQ' #.txt                                                       #
#                                                                       #
#########################################################################

with open('%s.txt' % fn) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    count=0
    ticker=[]
    ticker_description=[]
    
    for row in csv_reader:
        ticker.append(row[0])
        ticker_description.append(row[1])
        count+=1
    #print(ticker,len(ticker))
    #print(ticker_discription,len(ticker_discription))

def analyse_ticker (x):
#retrieve data from statistic tab
    import requests
    code= x
    r1= requests.get('https://ca.finance.yahoo.com/quote/'+code+'/key-statistics')
    #print( r.text[0:5000])
    from bs4 import BeautifulSoup
    soup1 = BeautifulSoup(r1.text, 'html.parser')

    #select all <td>
    td_tag=soup1.find_all('td')
    #len(td_tag) = const = 118
    if (len(td_tag) !=118):
        print('fail to get data')
        return [0,0,0,0,0,0,0,0]
    beta_result1= td_tag[63].contents
    if isinstance(beta_result1[0], bs4.element.Tag):
        print('fail to get beta')
        return [0,0,0,0,0,0,0,0]
    beta_result=float(beta_result1[0].replace(',',''))

    forward_PE_result1= td_tag[7].contents
    #print(type(forward_PE_result1[0]))
    if isinstance(forward_PE_result1[0], bs4.element.Tag):
        print('fail to get forward_PE')
        return [0,0,0,0,0,0,0,0]
    if (forward_PE_result1[0] =='∞'):
        print('fail to get forward_PE')
        return [0,0,0,0,0,0,0,0]
    forward_PE_result = float(forward_PE_result1[0].replace(',',''))

    dy_result1 = td_tag[101].contents
    if isinstance(dy_result1[0], bs4.element.Tag):
      print('fail to get dividend yield')
      return [0,0,0,0,0,0,0,0]
    dy_result = float(dy_result1[0].replace('%',''))/100

    PB_result1 = td_tag[13].contents
    if isinstance(PB_result1[0], bs4.element.Tag):
      print('fail to get PB')
      return [0,0,0,0,0,0,0,0]
    PB_result = float(PB_result1[0].replace(',',''))

    #for i in td_tag:
    #    print(td_tag.index(i), i, '\n')
    
    #print('beta_result:',beta_result,'\n',
    #     'forward_PE_result:',forward_PE_result,'\n',
    #     'dy_result:',dy_result,'\n',
    #     'PB_result:',PB_result)

    #retrieve data from analysis tab
    r3=requests.get('https://ca.finance.yahoo.com/quote/'+code+'/analysis')
    soup3 = BeautifulSoup(r3.text, 'html.parser')

    #select all <td>
    td_tag_ana=soup3.find_all('td')
    #print(len(td_tag_ana))
    #length test: 150
    #for i in td_tag_ana:
    #    print(td_tag_ana.index(i),i,'\n')

    growth1 = td_tag_ana[141].contents
    if (growth1[0] =='N/A'):
        #print('fail to get growth')
        return [0,0,0,0,0,0,0,0]
    growth_result = float(growth1[0].replace('%',''))/100
    #print('growth_result:',growth_result)

    #MCR = dy +g
    MCR1= dy_result + growth_result
    #print('MCR1:',MCR1)

    #E/BVE = (P/BVE)/(P/E)
    E_BVE = PB_result/forward_PE_result

    #MCR2 = (E/BVE-g)/(P/B) + g
    MCR2= (E_BVE-growth_result)/(PB_result) + growth_result
    #print('MCR2:',MCR2)

    #MCR3 = E/BVE + (1-P/B)*dy
    MCR3= E_BVE + (1-PB_result)*dy_result
    #print('MCR3:',MCR3)
    res=[beta_result,forward_PE_result,dy_result,PB_result,growth_result,MCR1,MCR2,MCR3,code]
    for i in range(len(res)-1):
      res[i]=round(res[i],2)
    #print('beta:', beta_result)
    print('retrieve data successfully')
    #print(res)
    return res

ans=[]
for i in range(1,len(ticker)):
    print(i, ticker[i])
    result = analyse_ticker(ticker[i])
    #print(result)
    if ((result[0] <= 1) and ((result[5]>0.2) or (result[6]>0.2) or (result[7]>0.2))):
        ans.append(result)
        numpy.savetxt("%s.csv" % fn, ans, delimiter=",", fmt='%s')
        #print(result[5],result[6],result[7])

#print(ans)


