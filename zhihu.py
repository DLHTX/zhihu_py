import requests
import time
import json
import re
import os
import qrcode_terminal
  
class zhihu(object):
    def __init__(self,page):
        self.headers = {
            'cookie': '_xsrf=INfepq83q0Al4DiVI5YpEXHrmTw2aYQX; _zap=3c5f156a-1f12-4b6a-a4c5-dfb9c483dd02; d_c0="AKCkq6vnFQ-PTkCmHJRYOMG4lFacPnNXB4Q=|1551948054"; __utmv=51854390.100--|2=registration_date=20150930=1^3=entry_date=20150930=1; q_c1=240b7aa11522427e89da414942069fb6|1555311019000|1552528977000; __utma=51854390.2058828186.1552528978.1552528978.1555311044.2; __utmz=51854390.1555311044.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/271643290/answer/525019532; tgw_l7_route=7bacb9af7224ed68945ce419f4dea76d; tst=r; capsion_ticket="2|1:0|10:1559206308|14:capsion_ticket|44:NDMxZjQxNzkxNDVmNDZlMzgyOWVjZDM4YzZiNDhkZjI=|7e87082a85b2184dc6422d666b6cb2bff14ffd05e4aa0247937eba4f09fde590"; z_c0="2|1:0|10:1559206313|4:z_c0|92:Mi4xWnZJa0FnQUFBQUFBb0tTcnEtY1ZEeVlBQUFCZ0FsVk5xZWZjWFFEYmdtazZ6RGR1cy1lalFkLUU0YllTM2kxbXl3|1393e7d5cc9103c3c93c628c830452fe69bf87a4e6ae21d30753e5759abf0c70"',
            'scheme':'https','user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36',
        }
        self.url =  "https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=a82276d267c4432910b2d05e8e72a3f5&desktop=true&page_number=1&limit=5&action=down&after_id=5"
        self.index = 0
        self.isend = False
    def recommend(self): 
        f = requests.get(self.url,headers=self.headers)#Get该网页从而获取该html内容
        res = f.json()#直接返回json字符串 requests的json方法
        self.lenght = len(res['data'])
        # print(f.json())
        # for index,i in enumerate(res['data']): #enumerate为python常用获取下标的方法
        #     if(i.get('target')):
        #         question = i.get('target').get('question').get('title')#使用字典中get方法可以防止报keyerror的错误
        #         html_answer = i['target']['content'].replace('<p>','').replace('</p>','\n').replace('<b>','\033[4;36;40m').replace('</b>','\033[0m').replace('<br>','').replace('</br>','\n')#替换所有标签
        #         answer = re.sub(r'<.*?>','',html_answer) #利用正则去除不必要的标签(视频,图片等)
        #         print('-'*50+'\n' '问题'+ str(index+1) +':\n' + question + '\n' +'\n' + '热评:\n' + answer +'-'*50 + '\n\n')
        #打印出第几个问题
        self.printRecommand(res)
        self.checkInput(res)

    def printRecommand(self,res):
        if(res['data'][self.index].get('target')):
            question = res['data'][self.index].get('target').get('question').get('title')#使用字典中get方法可以防止报keyerror的错误
            html_answer = res['data'][self.index]['target']['content'].replace('<p>','').replace('</p>','\n').replace('<b>','\033[4;36;40m').replace('</b>','\033[0m').replace('<br>','').replace('</br>','\n')#替换所有标签
            answer = re.sub(r'<.*?>','',html_answer) #利用正则去除不必要的标签(视频,图片等)
            os.system('cls')#清除之前的
            print('-'*50 + '\n'+'\033[4;36;40m问题:' +'\n' + question + '\033[0m:\n' +'\n' + '\033[4;36;40m热评\033[0m:\n' + answer +'-'*50 + '\n\n\b\b\b\b')
        else:
            print('该条数据出现问题')
            self.index = 0
            self.recommend()

    def checkInput(self,res): #判断输入的是什么进行翻页等操作
        type = input('\033[1;36;40m翻页输入s 查看当前问题输入e\033[0m:')
        if type == 's':
            if self.index < (self.lenght - 1 ):
                self.index = self.index + 1
                # print('未获取新的数据','当前index为',self.index)
                self.printRecommand(res)
                self.checkInput(res)
            else:
                self.index = 0
                print('正在请求....')
                self.recommend()
                self.printRecommand(res)
                self.checkInput(res)
        elif type == 'e':
            print('查看当前个问题' + '*'*50)
            id = res['data'][self.index].get('target').get('question').get('id')
            url = 'https://www.zhihu.com/api/v4/questions/'+ str(id) +'/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset=&limit=1&sort_by=default&platform=desktop'
            self.question(url)
        else:
            print('输入错误...')
            self.recommend()

    def question(self,url):
        f = requests.get(url,headers=self.headers)#Get该网页从而获取该html内容
        res = f.json()#直接返回json字符串 requests的json方法
        self.qRes = res
        # print(res['data'])
        for index,i in enumerate(res['data']): #enumerate为python常用获取下标的方法
            html_answer = i.get('content').replace('<p>','').replace('</p>','\n').replace('<b>','\033[4;36;40m').replace('</b>','\033[0m').replace('<br>','').replace('</br>','\n')#替换所有标签
            answer = re.sub(r'<.*?>','',html_answer) #利用正则去除不必要的标签(视频,图片等)
            question = i.get('question').get('title')
            author = i.get('author').get('name')
            voteup_count = i.get('voteup_count')
            self.question_id = i.get('question').get('id')
            self.answer_id = i.get('id')
            os.system('cls')#清除之前的
            print('-'*50+'\n'+ '\033[4;36;40m问题:' + question + '\n' +'\033[1;36;40m回答\033[0m'+':\n\b' + '作者:' + author + ' 点赞:' + str(voteup_count) + '\n\b' + answer +'-'*50 + '\n\n')
        if  res['paging']['is_end']:
            self.isend = True
        self.checkQuestion()

    def checkQuestion(self):
        type = input('翻页输入s 返回首页输入q 手机观看输入qr :')
        if type == 's':
            if self.isend == False:
                url = self.qRes['paging']['next']
                self.question(url)
                print('下一个回答'+'*'*50)
            else:
                print('无更多回答!正在返回首页')
                time.sleep(2)
                self.recommend()
        elif type =='q':
            self.recommend()
        elif type =='qr':##打印二维码
            url = 'https://www.zhihu.com/question/'+ str(self.question_id) +'/answer/'+ str(self.answer_id)
            qrcode_terminal.draw(url)
            self.checkQuestion()
        else:
            print('输入错误')
            self.checkQuestion()
if __name__ == "__main__":
    print('cmd知乎\n\n')
    time.sleep(0.3)
    print('版本v0.02\n\n')
    time.sleep(0.4)
    print('正在初始化...\n\n')
    time.sleep(0.5)
    zhihu = zhihu(1) ##实例化findIndex类 传入参数第一页 默认
    zhihu.recommend()

