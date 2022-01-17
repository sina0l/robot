from requests import get
from re import findall
from rubika.client import Bot
from rubika.tools import Tools
from rubika.encryption import encryption
import time

bot = Bot(input("Please enter your Auth:"))
target=input("group guid: ")
answered = [bot.getGroupAdmins]
retries = {}
sleeped = False
# Creator = shayan Heydari (snipe4Kill)
plus= True

while True:
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]
		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue
		
		open("id.db","w").write(str(messages[-1].get("message_id")))

		for msg in messages:
			if msg["type"]=="Text" and not msg.get("message_id") in answered:
				if not sleeped:
					if msg.get("text") == "ربات آنلاینی؟" and msg.get("author_object_guid") in admins :
						bot.sendMessage(target, "آره عشقم فعالم😉❤", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("add") :
						bot.invite(target, [bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]])
						bot.sendMessage(target, "کاربر مورد نظر افزوده شد!", message_id=msg.get("message_id"))

					elif msg.get("text") == "دستورات":
						bot.sendMessage(target, "لیسـت دستـــورات ربـات 🤖:\n\n●🤖 !bot : فعال یا غیر فعال بودن بات\n\n●❎ !stop : غیر فعال سازی بات\n\n●✅ !start : فعال سازی بات\n\n●🕘 !time : ساعت\n\n●📅 !date : تاریخ\n\n●📋 !del : حذف پیام با ریپ بر روی ان\n\n●🔒 !lock : بستن چت در گروه\n\n●🔓 !unlock : باز کردن چت در گروه\n\n●❌ !ban : حذف کاربر با ریپ زدن\n\n●✉ !send : ارسال پیام با استفاده از ایدی\n\n●📌 !add : افزودن کاربر به گپ با ایدی\n\n●📜 !info : لیست دستورات ربات\n\n●🆑 !cal :ماشین حساب\n\n●🔴 !user : اطلاعات کاربر با ایدی\n\n●😂 !jok : ارسال جک\n\n●🔵 !font : ارسال فونت\n\n●🔴 !ping : گرفتن پینگ سایت\n\n●🔵 !tran : مترجم انگلیسی")
					elif msg.get("text").startswith("cal"):
						msd = msg.get("text")
						if plus == True:
							try:
								call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
								if call[1] == "+":
									am = float(call[0]) + float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
									plus = False
							
								elif call[1] == "-":
									am = float(call[0]) - float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							
								elif call[1] == "*":
									am = float(call[0]) * float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							
								elif call[1] == "/":
									am = float(call[0]) / float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							except IndexError:
								bot.sendMessage(target, "لطفا دستور را به طور صحیح وارد کنید ❌" ,message_id=msg.get("message_id"))
						plus= True
					elif msg.get("text").startswith("send") :
						bot.sendMessage(bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"], "شما یک پیام ناشناس دارید:\n"+" ".join(msg.get("text").split(" ")[2:]))
						bot.sendMessage(target, "پیام ناشناستو ارسال کردم😉👌", message_id=msg.get("message_id"))

					elif msg.get("text") == "سلام":
						bot.sendMessage(target, "هــای😍🌹", message_id=msg.get("message_id"))

					if  msg.get("text").startswith('user @'):
						try:
							user_info = bot.getInfoByUsername( msg.get("text")[7:])
							if user_info['data']['exist'] == True:
								if user_info['data']['type'] == 'User':
									bot.sendMessage(target, 'Name User:\n ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nBio User:\n ' + user_info['data']['user']['bio'] + '\n\nGuid:\n ' + user_info['data']['user']['user_guid'] ,  msg.get('message_id'))
									print('sended response')
								else:
									bot.sendMessage(target, 'این که ایدی کاناله😐' ,  msg.get('message_id'))
									print('sended response')
							else:
								bot.sendMessage(target, "این حساب کاربری وجود نداره :/" ,  msg.get('message_id'))
								print('sended response')
						except:
							print('server bug6')
							bot.sendMessage(target, "خطا" ,message_id=msg.get("message_id"))
							

					elif msg.get("text") == "پایان" and msg.get("author_object_guid") in admins :
						sleeped = True
						bot.sendMessage(target, "ربات با موفقیت خاموش شد!", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("پینگ"):
						
						try:
							responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])

					elif msg.get("text").startswith("trans"):
						
						try:
							responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
							al = [responser["result"]]
							bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
							bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])

					elif msg.get("text").startswith("فونت"):
						#print("\n".join(list(response["result"].values())))
						try:
							response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
							bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
							bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])



					elif msg.get("text").startswith("جوک"):
						
						try:
							response = get("https://api.codebazan.ir/jok/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])

					elif msg.get("text") == "ساعت":
						bot.sendMessage(target, f"Time : {time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}", message_id=msg.get("message_id"))

					elif msg.get("text") == "تاریخ میلادی":
						bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))

					elif msg.get("text") == "پاک" and msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("reply_to_message_id")])
						bot.sendMessage(target, "پیام مورد نظر پاک شد...", message_id=msg.get("message_id"))


					elif msg.get("text") == "بستن گروه" and msg.get("author_object_guid") in admins :
						print(bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","AddMember"]).text)
						bot.sendMessage(target, "گروه بسته شد!", message_id=msg.get("message_id"))

					elif msg.get("text") == "باز کردن گروه" and msg.get("author_object_guid") in admins :
						bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","SendMessages","AddMember"])
						bot.sendMessage(target, "گروه باز شد!", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("بن") and msg.get("author_object_guid") in admins :
						try:
							guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							if not guid in admins :
								bot.banGroupMember(target, guid)
								bot.sendMessage(target, f"کاربر مورد نظر بن شد !", message_id=msg.get("message_id"))
							else :
								bot.sendMessage(target, f"خطا", message_id=msg.get("message_id"))
								
						except IndexError:
							a = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
							if a in admins:
								bot.sendMessage(target, f"خطا", message_id=msg.get("message_id"))
							else:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								bot.sendMessage(target, f"کاربر مورد نظر بن شد !", message_id=msg.get("message_id"))

				else:
					if msg.get("text") == "شروع" and msg.get("author_object_guid") in admins :
						sleeped = False
						bot.sendMessage(target, "ربات شروع به فعالیت کرد!", message_id=msg.get("message_id"))

			elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
				name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
				data = msg['event_data']
				if data["type"]=="RemoveGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"اگه قوانین رو رعایت میکردی حذف نمیشدی !", message_id=msg["message_id"])
				
				elif data["type"]=="AddedGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"های {user} به گروه {name} خوش اومدی😍❤️\nلطفا قوانین رو رعایت کن👌🙁\n\nکانال ما : @TGGAMES", message_id=msg["message_id"])
				
				elif data["type"]=="LeaveGroup":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"موفق باشی 👋", message_id=msg["message_id"])
					
				elif data["type"]=="JoinedGroupByLink":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"های {user} به گروه {name} خوش اومدی😍❤️\nلطفا قوانین رو رعایت کن👌🙁\n\nکانال ما : @TGGAMES", message_id=msg["message_id"])

			answered.append(msg.get("message_id"))

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
