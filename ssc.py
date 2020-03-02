from bs4 import BeautifulSoup
import requests
import time
import json

web_hook_url = 'API KEY HERE'


# courseNum, sectionNum, campusName, subjectNam

def run(courseNum, sectionNumOG, campusName, subjectName,tag):
    try:
        sectionNum = "{0:0=3d}".format(sectionNumOG)  
        #url = "https://courses.students.ubc.ca/cs/courseschedule?campuscd=UBCO&pname=subjarea&tname=subj-section&course=108&section=001&dept=GEOG"
        url = "https://courses.students.ubc.ca/cs/courseschedule?tname=subj-section&course=%s&section=%s&campuscd=%s&dept=%s&pname=subjarea" % (str(courseNum), str(sectionNum), campusName, subjectName)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h4')
        title = title.get_text()
        table = soup.find_all('table')[3]
        all_text = ''.join(table.findAll(text=True))
        all_text = all_text.splitlines()
        newText = all_text[2] + "\n" + all_text[3] + "\n" + all_text[4] + "\n" + all_text[5] + "\n"
        getSeat = int(''.join(filter(lambda x: x.isdigit(), all_text[4])))
        #raise Exception
        slack_msg = {
            'text': '<@%s>%s' % (tag,title + "\n" + newText)
        }
        print(title)  # print(newText)
        if getSeat != 0:
            requests.post(web_hook_url, data=json.dumps(slack_msg))
        else: 
            print("SEAT IS FULL")
    except Exception as e:
      s,r = getattr(e, 'message', str(e)), getattr(e, 'message', repr(e))
      print ('s:', s, 'len(s):', len(s))
      print ('r:', r, 'len(r):', len(r))

while (1):
    for x in range(1, 9):
        #run(courseNum,campus,courseName,slackID);
        run(150, x, "UBCO", "ENGL","weejiaquan1234" )
time.sleep(10)
