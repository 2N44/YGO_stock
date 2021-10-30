import pandas as pd
import database
import os

class YGOList(object):

	def __init__(self, path):

		self.path = path
		self.card_code = []
		self.url = []
		self.db_cardmarket = database.DatabaseCardmarket(os.path.join(os.path.dirname(os.path.abspath(__file__)),'database','database_cardmarket.json'))

	def get_url(self):

		"""
		Return cardmarket url list from card list
		"""

		for  code in self.card_code:

			self.url.append(self.db_cardmarket.get_url(code))

	def add_line(self, line):

		"""
		Add a line to the YGOlist
		"""

		with open(self.path, 'a') as f:

			f.write(line+'\n')

	def add_lines(self, lines):

		"""
		Add a list of lines to the YGOlist
		"""

		with open(self.path, 'a') as f:

			for line in lines:

				f.write(line+'\n')		



class IdList(YGOList):

	def __init__(self, path):

		super().__init__(path)

		with open(self.path, 'r') as f:

			lines = f.readlines()
			self.lines = lines

			for line_idx in range(len(lines)):

				lines[line_idx] = int(lines[line_idx])

			self.id_list = lines

		for card_id in self.id_list:
			
			for code in self.db_cardmarket.find(card_id, column='card_id').index:

				self.card_code.append(code)

		self.number = len(self.id_list)

	def add_line(self, card_id):

		"""
		Add a line to YDKlist
		"""

		super().add(str(card_id))

		for code in self.db_cardmarket.find(card_id, column='card_id').index:

			self.card_code.append(code)

	def add_lines(self, card_id_list):

		"""
		Add all ID in the list input to ydk file
		"""

		card_id_list_str = [str(x) for x in card_id_list]

		super().add_lines(card_id_list_str)

		for card_id in card_id_list:

			for code in self.db_cardmarket.find(card_id, column='card_id').index:

				self.card_code.append(code)



class DeckList(YGOList):

	def ___init__(self, path):

		super().__init__(path)

		with open(self.path, 'r') as f:

			lines = f.readlines()
			self.lines = lines
			lines.remove('#main\n')
			lines.remove('#extra\n')
			lines.remove('!side\n')

			for line in lines:

				if '#' in line:

					lines.remove(line)

			for line_idx in range(len(lines)):

				lines[line_idx] = int(lines[line_idx])

			self.id_list = lines

		for card_id in self.id_list:
			
			for code in self.db_cardmarket.find(card_id, column='card_id').index:

				self.card_code.append(code)

		self.number = len(self.id_list)

		self.number_main = self.lines.index('#extra\n') - self.lines.index('#main\n') - 1
		self.number_extra = self.lines.index('#extra\n') - self.lines.index('!side\n') - 1
		self.number_side = len(self.lines) - self.lines.index('!side\n')

	def add_line(self, card_id, deck='main'):

		"""
		Add Card ID to the file

		card_id - id of card (int)
		deck - By default 'main', can take the value 'extra' et 'side'
		"""

		self.id_list.append(card_id)

		with open(self.path, 'w') as f:

			for line in self.lines:

				if deck in line:

					self.lines.insert(lines.index(line)+1, str(card_id)+'\n')

			f.writelines(self.lines)

	def add_lines(self, card_id_list, deck='main'):

		"""
		Add list of Card ID to the file

		card_id - list of int
		deck - By default 'main', can be 'extra' or 'side'
		"""

		card_id_list_str = [str(x) for x in card_id_list]

		with open(self.path, 'w') as f:

			for line in self.lines:

				if deck in line:

					for idx_card_id in range(len(card_id_list_str)):

						self.lines.insert(lines.index(line)+idx_card_id+1, card_id_str[idx_card_id]+'\n')
						self.id_list.append(card_id_list[idx_card_list])

			f.writelines(self.lines)



class CodeList(YGOList):

	def __init__(self, path):

		super().__init__(path)

		with open(self.path, 'r') as f:

			lines = f.readlines()

			for line in lines:

				line = line[:-2]

			self.card_code = lines

		self.number = len(card_code)







