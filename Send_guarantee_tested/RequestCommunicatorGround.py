from MyReedSolomon import ReedSolomon
import time
import random
from datetime import datetime

from REQUEST import Requester
from HARDWARE_TRANSFER import SocketDevice, Device

class RequestCommunicatorGround:
	def __init__(self, device: Device):
        self.device = device
        self.fooRS = ReedSolomon() 
        self.error_list = ["retrying last message please", "unable to understand"]
	def request_guarantee(self, input_message, tSize):
		# Декодируем сообщение кодом Рида Соломона для отправки
		encode_message = self.fooRS.RSDecode(list(input_message), tSize)
		# Отправляем декодированное сообщение
		self.device.send(encode_message)
		# Получаем сообщение
		response = self.device.receive()
		# Проверяем, содержит ли полученное сообщение просьбу повторить сообщение
		while True:
			if self.error_list[0] in response:
				# Декодируем сообщение кодом Рида Соломона для отправки
				encode_message = self.fooRS.RSDecode(list(input_message), tSize)
				# Отправляем декодированное сообщение
				self.device.send(encode_message)
				# Получаем сообщение
				response = self.device.receive()
			if self.error_list[1] in response:
				return response
			elif:
				return response
		return response
