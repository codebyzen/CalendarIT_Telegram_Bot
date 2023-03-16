from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime

class avatar_update:

	def generate(self):
		img = Image.open('assets/avatar_update/channel_avatar.jpg')
		width, height = img.size
		
		I1 = ImageDraw.Draw(img)

		font1 = ImageFont.truetype('assets/avatar_update/Arial Black.ttf', 125)
		fontColor1 = (0, 0, 0)
		
		font2 = ImageFont.truetype('assets/avatar_update/Arial.ttf', 50)
		fontColor2 = (255, 255, 255)
		

		dt = datetime.now()
		message_day = str(dt.day)
		month_num = dt.month
		months = [
			"январь","февраль","март","апрель",
			"май", "июнь","июль","август",
			"сентябрь","октябрь","ноябрь","декабрь"
		]
		message_month = months[month_num-1].upper()

		# message_month = datetime.strptime(dt, u'[ %d-%b-%y  %H:%M ]')

		_, _, widthTextBox, heightTextBox = I1.textbbox((0, 0), message_day, font=font1)
		I1.text(((width-widthTextBox)/2, ((height-heightTextBox)/2)+30), message_day, font=font1, fill=fontColor1)
		
		_, _, widthTextBox, heightTextBox = I1.textbbox((0, 0), message_month, font=font2)
		I1.text(((width-widthTextBox)/2, ((height-heightTextBox)/2)-80), message_month, font=font2, fill=fontColor2)

		# img.show()
		img.save("assets/avatar_update/channel_avatar_date.jpg")


# if __name__ == '__main__':
# 	generate()

