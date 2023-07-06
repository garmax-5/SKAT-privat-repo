#!!
from MyReedSolomon import ReedSolomon
import time
import random
from datetime import datetime

from REQUEST import Requester
from HARDWARE_TRANSFER import SocketDevice, Device

class RequestCommunicatorPlaner:
	def __init__(self, request, on_request, timeout, on_timeout):
		self.request = request
		self.on_request = on_request
		self.timeout = timeout
		self.on_timeout = on_timeout
		# Очередь для отправленных на землю сообщений
		self.queue = []
		# переменная, показывающая что функция уже запустила timeout
		self.on_timeout_value = False
		# Текущее время timeout
		self._timeout = 0

	def get_on_request_guaranteed_func(self,on_request_nonguaranteed_func):
		def on_request_guaranteed_func(self,input_message,tSize):
			try:
				fooRS = ReedSolomon()
				# Получаем тело запроса 	
				data = input_message	
				# декодирование (получаем исправленный массив, содержащий номера символов ascii)
				decode_data = fooRS.RSDecode(list(data), tSize)
				# проверяем на наличие неисправимых ошибок
				# Если неисправимых ошибок нет, то возвращаем полученное значение
				if decode_data != "ERROR TO DECODE":
					message = ''.join([chr(i) for i in decode_data])[0:-tSize]
					# Добавляем наше нормальное сообщение в очередь, если оно отправилось в течении времени timeout'a
					if self.on_timeout_value:
						self.queue.append(message)
					return message
				# Если неисправимые ошибки есть, просим источник повторить отправку в течении времени timeout
				else:
					
					# Если это первая ошибка, которая находится в очереди, то просим землю повторить последнее сообщение
					if (len(self.queue) == 0) and (not self.on_timeout_value):
						print("-----Первая ошибка")
						self.on_timeout_value = True
						self._timeout = time.time() + self.timeout
					self.queue.append("retrying last message please")
					# Если время timeoutа превышает допустимое и в течении всего этого срока сообщение так и не было распознано
					if (time.time() > self._timeout) and (self.on_timeout_value) and len(set(self.queue)) == 1:
						print("Превышение timeout")
						self.on_timeout_value = False
						self.queue = []	
						# Вызываем исключение Exception, после чего в finally сообщаем земле о том, что не удалось распознать сообщение
						raise Exception("unable to understand")
					if (time.time() > self._timeout) and (self.on_timeout_value):
						self.queue = []
					#return "retrying last message please"
					#return f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} {__file__} retrying last message please" 
					return f"{on_request_nonguaranteed_func(input_message)} {__file__} retrying last message please"
			except Exception as e:
				print("ERROR ---> ",e)
				#return f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} {__file__} unable to understand"
				return f"{on_request_nonguaranteed_func(input_message)} {__file__} unable to understand"
			#finally:
		return on_request_guaranteed_func


