import datetime

class app_pronounce:

	config = {
		'ln': 'ru'
	}

	ln = {
		'ru': {
			'months': ('Января','Февраля','Марта','Апреля','Мая','Июня','Июля','Августа','Сентября','Октября','Ноября','Декабря'),
			'years': ('год','года','лет'),
			'total_dates': 'Всего дат в календаре',
			'add_date': 'Добавить дату',
			'press': 'Для прессы и рекламодателей',
			'title': 'Календарь IT дат',
			'404': 'Нет такого слова =)'
		},
		'en': {
			'months': ('January','February','March','April','May','June','July','August','September','October','November','December'),
			'years': ('year','years','years'),
			'total_dates': 'Total dates',
			'add_date': 'Add date',
			'press': 'For press and adverts',
			'title': 'IT dates calendar',
			'404': 'Page error 404 - not found!'
		}
	}

	def getAlready(day,month):
		already = ['Исполнится', 'Исполнилось']
		if (day==None):
			day = 0
		if (month==None):
			month = 0
		datenow = datetime.datetime.now()
		dayNow = int(datenow.strftime("%d").lstrip("0"))
		monthNow = int(datenow.strftime("%m").lstrip("0"))


		if (dayNow>=day and monthNow>=month):
			return already[1] 
		else:
			return already[0]
	

	
	def getYearsPronounce(self, int):
		
		years = int
		int = int % 10


		if (years >= 11 and years<= 20):
			return [years, self.ln[self.config['ln']]['years'][2]]

		if (int==1):
			return [years, self.ln[self.config['ln']]['years'][0]]

		if (int>1 and int<5):
			return [years, self.ln[self.config['ln']]['years'][1]]

		if (int==0 or (int>=5 and int<=21)):
			return [years, self.ln[self.config['ln']]['years'][2]]

	

	def decoratePronounceWithHTML(self, pronounceArray):
		return pronounceArray[0]+' '.pronounceArray[1]

