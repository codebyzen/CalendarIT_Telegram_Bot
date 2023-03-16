from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import re

class puzzle_image:

	def generate(self,words):
		img = Image.open('assets/puzzle/puzzle.jpg')
		img2 = Image.open('assets/puzzle/puzzle.jpg')
		# img = Image.new('RGB', [600,600], (255,255,255))
		# img2 = Image.new('RGB', [600,600], (255,255,255))
		
		draw = ImageDraw.Draw(img)
		draw2 = ImageDraw.Draw(img2)

		font = ImageFont.truetype('assets/puzzle/droid-sans-mono.ttf', 40)
		
		_, _, widthTextBox, heightTextBox = draw.textbbox((0, 0), " ".join(words), font=font)
		
		# \x1b[32mО\x1b[0m

		color = (0,0,0,0)
		x = 130
		y = 110

		_, _, chrwidth, _ = font.getbbox(words[0])
		
		for char in words:
			result = re.match(r'\x1b\[32m([^\\]+)\x1b\[0m', char)
			if (result is not None):
				color = (255,255,255,0)
				char = result.group(1)
			else:
				color = (0,0,0,0)
		
			if char == "\n":
				y += chrwidth*2
				x = 130
				continue

			# draw.text((0, 0), char, font=font, fill=color ) # BGRA
			draw.text((x, y), char, font=font, fill=(0,0,0,0))
			draw2.text((x, y), char, font=font, fill=color)
			x += chrwidth*2

		# draw.text(((width-widthTextBox)/2, ((height-heightTextBox)/2)), words, font=font, fill=fontColor1)
		
		# img.show()
		# img2.show()
		img.save("assets/puzzle/puzzle_1.jpg")
		img2.save("assets/puzzle/puzzle_2.jpg")


# if __name__ == '__main__':
# 	au = puzzle_image()
# 	au.generate()

