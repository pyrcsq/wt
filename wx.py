
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message,WeChatClient
from wechatpy.replies import TextReply,ImageReply
from flask import Flask,session,request,render_template
import json

# user = client.user.get('user id')
# menu = client.menu.get()
# client.message.send_text('user id', 'content')
def uploadimage(filepath):
    import requests
    url = "https://api.weixin.qq.com/cgi-bin/token"
    data = {"grant_type": "client_credential",
            "appid": "xxxxxx",
            "secret": "xxxxxx"}
    # req = requests.post(url,data)
    # print(req.json())
    pu = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=xxxxxxxxX-lFZD_TgGYytW1wbLFvD9HDILibbKhoS-iQ5m4YoxSdlpLZp51jDGLAWbAAAHWS&type=image"
    files = {'file': open(filepath, 'rb')}
    req2 = requests.post(url=pu, files=files)
    return req2.json()["media_id"]
def ltoj(list,filename):#
    import json

    # json.dump()函数的使用，将json信息写进文件
    json_info = list
    file = open("/home/www/"+filename+".json", 'w', encoding='utf-8')
    json.dump(json_info, file)
    return 0
def jtol(filename):
    import json

    # json.load()函数的使用，将读取json信息
    file = open("/home/www/"+filename+".json", 'r', encoding='utf-8')
    info = json.load(file)
    return info
# def storeinfo(inlist):



def genepic(picname, name, type):
    picname="/home/www/"+picname+".png"
    from PIL import Image, ImageDraw, ImageFont
    import time
    if len(name) >= 4:
        name = name[:4]
    dic = {"1": ["120%", "-20%", "山无棱，江水为竭，冬雷震震，", "夏雨雪，天地合，" + name + "才脱单"],
           "2": ["20%", "80%", "遇到" + name + "这么好的男人", "还不快嫁了"],
           "3": ["50%", "90%", name + "，告诉你一个秘密，", "在男生眼中你就是一个大帅哥"],
           "4": ["30%", "60%", "在女生心目中，" + name + "就是", "一个可爱的大叔！"],
           "5": ["120%", "-20%", "山无棱，江水为竭，冬雷震震，", "夏雨雪，天地合，" + name + "才脱单"],
           "6": ["20%", "80%", "遇到" + name + "这么可爱的小姐姐", "还不快嫁了"],
           "7": ["50%", "90%", name + "一直有个梦想，", "那就是成为万人迷!"],
           "8": ["60%", "50%", name + "虽然有着萝莉的外表，", "但是有一颗御姐的心"],
           }
    znzs = "直男指数：" + dic[type][0]
    tdgl = "脱单概率：" + dic[type][1]
    line1 = dic[type][2]
    line2 = dic[type][3]
    # 安装库：pip install Pillow

    header = '001'
    title = name + "于" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    title2 = '参加了直男/女指数测试'
   
    n = 18
    summary_list = [summary[i:i + n] for i in range(0, len(summary), n)]

    # 图片名称
    img = '/home/www/one.png'  # 图片模板
    new_img = picname  # 生成的图片
    # compress_img = 'compress.png'  # 压缩后的font_type = '宋体.ttf'图片

    # # 设置字体样式
    font_type = '/home/www/宋体.ttf'

    font = ImageFont.truetype(font_type, 34)
    color = "#000000"
    grey = "#FFFF00"

    # 打开图片
    image = Image.open(img)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    print(width, height)



    draw.text((90, 300), u'%s' % title, grey, font)
    draw.text((90, 350), u'%s' % title2, grey, font)
    draw.text((90, 450), u'%s' % znzs, color, font)
    draw.text((90, 500), u'%s' % tdgl, color, font)
    draw.text((90, 600), u'%s' % line1, color, font)
    draw.text((90, 650), u'%s' % line2, color, font)



    image.save(new_img, 'png')
    print("success!")




def sendemail(to,code):
    import smtplib
    from email import encoders
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    sender = 'xxx'  #
    passWord = 'xxx'
    mail_host = 'xxx'
    # receivers是邮件接收人，用列表保存，可以添加多个
    receivers = []
    receivers.append(to)
    msg = MIMEMultipart()
    msg['Subject'] = "[验证]验证码是"+code
    # 发送方信息
    msg['From'] = sender
    # 邮件正文是MIMEText:
    msg_content = "您好，您正在参与520心愿卡活动。您的验证码是"+code+",如果不是您本人操作，请忽略"
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
    # # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    # with open(u'/Users/xxx/1.jpg', 'rb') as f:
    #     # 设置附件的MIME和文件名，这里是jpg类型,可以换png或其他类型:
    #     mime = MIMEBase('image', 'jpg', filename='Lyon.png')
    #     # 加上必要的头信息:
    #     mime.add_header('Content-Disposition', 'attachment', filename='Lyon.png')
    #     mime.add_header('Content-ID', '<0>')
    #     mime.add_header('X-Attachment-Id', '0')
    #     # 把附件的内容读进来:
    #     mime.set_payload(f.read())
    #     # 用Base64编码:
    #     encoders.encode_base64(mime)
    #     # 添加到MIMEMultipart:
    #     msg.attach(mime)
    # 登录并发送邮件
    try:
        # QQsmtp服务器的端口号为465或587
        s = smtplib.SMTP_SSL("xxxx", 465)
        s.set_debuglevel(1)
        s.login(sender, passWord)
        # 给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(sender, to, msg.as_string())
            print('Success!')
        s.quit()
        print("All emails have been sent over!")
    except smtplib.SMTPException as e:
        print("Falied,%s", e)


app=Flask(__name__)
questionlist=["你好啊！参加心愿卡活动吗？请先回答几个问题哦：你是男生还是女生，（回复男或女）","请输入你的名字（假名化名英文名网名也可）","你的微信(对方可见)","希望帮你实现心愿的人是男生还是女生，（回复男或女）","在这许下你的心愿/对ta说的话（对方可见，字数如果超过200我们将截取前200个字）","你的edu邮箱，我们将给你发一条验证码，以验证你的身份为学生，防止社会人士骚扰。匹配时将优先匹配同校学生","验证码已发，请检查邮箱并向我回复验证码","验证成功.现在进行个性化测试：请问你有过几段感情(填阿拉伯数字)","你找伴侣看中对方什么特质:A外貌和身材，B家境，C性格，D才能","你在恋爱中更倾向主动还是被动","测试完成，卷积神经网络（🐶）正在对您的信息进行大数据分析（🐶），回复'结果'查看测试结果\n\nps：匹配成功后我们会通过您预留的邮箱通过邮件告知您匹配结果"]
variables=["boyorgirl","name","wechat","hopesex","wish","mail","code","lovetime","lovefocus","paorpo"]

userdict={"source":{"status":0,"boyorgirl":"","name":"","wechat":"","hopesex":"","wish":"","mail":"","code":"","lovetime":"","lovefocus":"","paorpo":""}}
@app.route("/connect",methods=['GET','POST'])
def reply():
    import os
    ltoj(userdict,"520")
    xml = request.data

    # xml = req.stream.read()
    msg = parse_message(xml)

    if msg.source in userdict:
        info = userdict[msg.source]
        if info["status"]<12:
            if info["status"] == 6:
                if str(msg.content) == str(info["code"]):
                    userdict[msg.source]["status"] += 1
                    reply = TextReply(content=questionlist[info["status"] ], message=msg)
                    xml = reply.render()
                    return xml, 200, {"ContentType": "application"}
                else:
                    reply = TextReply("验证码错误，请重新回答", message=msg)
                    xml = reply.render()
                    return xml, 200, {"ContentType": "application"}
            if info["status"]==5:
                import random
                co = str(random.randint(100000, 999999))
                try:

                   userdict[msg.source][variables[info["status"]]] = msg.content
                   userdict[msg.source][variables[info["status"]+1]] = co
                   sendemail(userdict[msg.source]["mail"], co)
                   userdict[msg.source]["status"] += 1
                   reply = TextReply(content=questionlist[info["status"] ], message=msg)
                   xml = reply.render()
                   return xml, 200, {"ContentType": "application"}
                except:
                    reply = TextReply(content="失败，请重新尝试", message=msg)
                    xml = reply.render()
                    return xml, 200, {"ContentType": "application"}




            if info["status"] <= 5 or info["status"] >= 6:
                if info["status"]==10:
                    #####################
                    if "男" in userdict[msg.source]["boyorgirl"]:
                        if "男" in userdict[msg.source]["hopesex"]:
                            ty=""
                        else:
                            ii=userdict[msg.source]["lovetime"]
                            if "0" in ii or "1" in ii:
                                ty=""
                            else:
                                if "2" in ii or "3" in ii:
                                    ty=""
                                else:
                                    ty=""
                    else:
                        if "女" in userdict[msg.source]["boyorgirl"]:
                            if "女" in userdict[msg.source]["hopesex"]:
                                ty=""
                        else:
                            ii=userdict[msg.source]["lovetime"]
                            if "0" in ii or "1" in ii:
                                ty = ""
                            else:
                                ty=""
                    ############################
                    # client = WeChatClient('wxbc0b84e6fe860f0a', 'faf45c78716f41aaa61c19b7f439af1e')
                    genepic(msg.source.lower()[-10:],userdict[msg.source]["name"],ty)
                    mi=uploadimage("/home/www/"+msg.source.lower()[-10:]+".png")
                    os.remove("/home/www/"+msg.source.lower()[-10:]+".png")
                    reply = ImageReply(media_id=mi, message=msg)
                    xml = reply.render()
                    return xml, 200, {"ContentType": "application"}






                else:
                    userdict[msg.source][variables[info["status"]]] = msg.content  # 0的时候存入是男是女；问姓名
                    userdict[msg.source]["status"] += 1
                    reply = TextReply(content=questionlist[info["status"]], message=msg)
                    xml = reply.render()
                    return xml, 200, {"ContentType": "application"}





    else:
        if msg.content=="520":
            userdict[msg.source] = {"status": 0}
            reply = TextReply(content="你好啊！参加心愿卡活动吗？请先回答几个问题哦：你是男生还是女生，（回复男或女）", message=msg)
            xml = reply.render()
            return xml, 200, {"ContentType": "application"}



    # if msg.type == 'text':
    #     print(msg.content)
    #     reply = TextReply(content=msg.content, message=msg)
    #     xml = reply.render()
    #     return xml, 200, {"ContentType": "application"}
    # if msg.type == 'image':
    #     reply = ImageReply(media_id=msg.media_id, message=msg)
    #     xml = reply.render()
    #     return xml, 200, {"ContentType": "application"}
if __name__=="__main__":
    app.secret_key=b'\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x1b'
    app.run(host="0.0.0.0",port="80",threaded=True)#记得上传服务器的时候把这改成80端口


