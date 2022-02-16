from django.shortcuts import render
from django.http import  HttpResponse
from bs4 import  BeautifulSoup
from django.shortcuts import redirect
import  requests
data = {};
sub_cn = 0
not_sub_cn = 0
f = 1
def fun(uname , ind):
    global data,sub_cn,not_sub_cn,f
    url = "https://takeuforward.org/interview-experience/strivers-cp-sheet/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content , "html.parser")
    implementation = soup.find_all('details')
    title = implementation[ind].find('b')
    t = title.text
    data['links'] = []
    url_main = f"https://codeforces.com/api/user.status?handle={uname}&from=1&count=5000"
    page1  = requests.get(url_main)
    data1 = page1.json()
    if (data1['status']  == "FAILED"):
        f = 0
        return
    links = implementation[ind].find_all('li');
    for i in links:
        url = i.text

        str1 = ""
        l = list(url.split('/'))
        c = 0
        chr =''
        for x in l[::-1]:
            if(c==2):
                break
            if x.isdigit():
                str1+=x;c+=1;str1+=chr
            if len(x) == 1:
                c+=1
                chr+=x;

        dic = {}
        for y in data1['result']:
            s = str(y['contestId']) + y['problem']['index']
            if(dic.get(s) == None):
                dic[s] = y['verdict']
            elif dic[s]!="OK":
                    dic[s] = y['verdict']
        if(dic.get(str1)!=None):
            data['links'].append([i.text,"SUBMITTED"])
            sub_cn+=1
        else:
            data['links'].append([i.text,"NOT SUBMITTED"])
            not_sub_cn+=1
    data['title'] = t;
    data['sub_cn'] = sub_cn
    data['not_sub_cn'] = not_sub_cn
topics = ["Implementation","Math ","Binary Search","Prime","Bit","Stack","String","BFS","Tree's",
            "LCA","Graph","ME","Trie","DP","DISJOINT","Mos","fenwick","Segment"

]
def home(request):
    if request.method == 'POST':
        global data ,f
        global sub_cn ,not_sub_cn
        sub_cn =0
        not_sub_cn=0
        for i in  topics:
            if (request.POST.get(i)!=None):
                data['u'] = request.POST.get("uname")
                data['plink'] = 'https://codeforces.com/profile/' + data['u']
                ind = int(request.POST.get(i))
                fun(data['u'] ,ind )
                break;
        if(f == 0):
            f = 1
            return redirect('invalid_username/')
        else:
            return render(request,'tracker/home.html',data)
def invalid_username(request):
    return render(request , 'tracker/invalid.html')
