import pandas as pd
import numpy as np
import os

class FormatError(Exception):

	pass

class ArgError(Exception):

	pass



def cm_id_2_set_code(cm_id):

	"""
	Return set code from a "card_code (rarity)" string
	"""

	if not('-' in cm_id and ' (' in cm_id and ')' in cm_id) or len(cm_id)<10:

		raise FormatError()

	else:

		set_code = ''

		for char in cm_id:

			if char=='-':

				break

			set_code += char

		return set_code



def cm_id_2_rarity(cm_id):

	"""
	Return rarity from a "card_code (rarity)" string
	"""

	if not('-' in cm_id and ' (' in cm_id and ')' in cm_id) or len(cm_id)<10:

		raise FormatError()

	else:

		pos_open = cm_id.find('(')
		pos_close = cm_id.find(')')

		return cm_id[pos_open+1:pos_close]



def cm_id_2_card_code(cm_id):

	"""
	Return rarity from a "card_code (rarity)" string
	"""

	if not('-' in cm_id and ' (' in cm_id and ')' in cm_id) or len(cm_id)<10:

		raise FormatError()

	else:

		pos_space = cm_id.find(' ')
		

		return cm_id[:pos_space]



class Database(object):

	"""
	Database of YGO cards, stored as JSON
	"""

	def __init__(self,path):

		self.path = path
		self.db = pd.read_json(path, orient='index')

	def add(self, index, dico):

		"""
		Add a row with dico={'column_1': values_1, column_2: values_2} as values and index
		"""

		try:

			len(index)
			self.db = self.db.append(dico, index)

		except TypeError:

			for key in dico:

				dico[key] = [dico[key]]

			self.db = self.db.append(dico, [index])

	def remove(self, index):

		"""
		Remove row with index from database
		"""

		self.db = self.db.drop(index)

	def find(self, key, column=None):

		"""
		Find and return rows with key value in column, by default search with key value as index
		"""

		result = pd.DataFrame( columns=self.db.columns)
		index_list = [];

		if column==None:

			for index in self.db.index:

				if index==key:

					result = result.append(self.db.loc[index,:])


		else:

			for index in self.db.index:

				if self.db.loc[index, column]==key:

					result = result.append(self.db.loc[index,:])

		return result

	def exist(self, index):

		"""
		Raise KeyError if the row with index is not in the database
		"""
		try:

			len(index)
			for idx in index:

				self.db.loc[idx, :]

		except TypeError:

			self.db.loc[index, :]



	def mod(self, data, index):

		"""
		Replace the field of the column with data input

		data - dictionnary of data ({column_1: data_1, column_2: data_2})
		index - index of the row to be modified
		"""

		for column in data:

			self.db.loc[index, column] = data[column]

	def save(self):

		self.db.to_json(self.path, orient='index')



class DatabaseCard(Database):

	def __init__(self, path):

		super().__init__(path)
		self.db_card = Database(os.path.join(os.path.dirname(os.path.abspath(__file__)),'database','db_card.json'))
		self.db_set = Database(os.path.join(os.path.dirname(os.path.abspath(__file__)),'database','db_set.json'))

	def _create_dico(self, index, card_id, set_code_cardmarket=None, set_name=None, name=None):

		"""
			create a dicoionary with input
		"""

		dico = {
			'set_code':[],
			'set_code_cardmarket':[],
			'set_name': [],
			'card_code': [],
			'rarity': [],
			'card_id': [],
			'name': []
			}

		try:

			len(index)	#test if we have list or just a string

			for idx in index:

				dico['set_code'].append(cm_id_2_set_code(idx))
				dico['set_code_cardmarket'].append(cm_id_2_set_code(idx))
				dico['card_code'].append(cm_id_2_card_code(idx))
				dico['rarity'].append(cm_id_2_rarity(idx))

			for c_id in card_id:

				dico['card_id'].append(c_id)

			if set_code_cardmarket!=None:

				for set_code_cm in set_code_cardmarket:

					dico['set_code_cardmarket'].append(set_code_cm)

			if set_name!=None and name!=None:

				for set_name_idx in set_name:

					dico['set_name'].append(set_name_idx)

				for name_idx in name:

					dico['name'].append(name_idx)

			else:

				if name== None:

					for c_id in card_id:

						dico['name'].append(self.db_card.loc[c_id, 'name'])

				else:

					for name_idx in name:

						dico['name'].append(name_idx)

				if set_name==None:

					for code in dico['set_code']:

						dico['set_name'].append(self.db_set.loc[code, 'name'])

				else:

					for set_name_idx in set_name:

						dico['set_name'].append(set_name_idx)


		except TypeError:

			dico = {
			'set_code':cm_id_2_set_code(index),
			'set_code_cardmarket':cm_id_2_set_code(index),
			'set_name':'',
			'card_code':cm_id_2_card_code(index),
			'rarity':m_id_2_rarity(index),
			'card_id':card_id,
			'name':''
			}

			if set_code_cardmarket!=None:

				dico['set_code_cardmarket'] = set_code_cardmarket

			if set_name!=None and name!=None:

				dico['set_name'] = set_name
				dico['name'] = name

			else:

				if name==None:

					dico['name'] = self.db_card.loc[card_id, 'name']

				else:

					dico['name'] = name


				if set_name==None:

					dico['set_name'] = self.db_set.loc[dico['set_code'], 'name']

				else:

					dico['set_name'] = set_name

		return dico



class DatabaseMyCard(DatabaseCard):

	def add(self, index, number=None, card_id=None, set_code_cardmarket=None, set_name=None, name=None):

		"""
		Add a card to the database
		"""
		try:

			super().exist(index)

			if number==None:

				self.db.loc[index, 'num'] += 1

			else:

				self.db.loc[index, 'num'] += number


		except KeyError:

			if card_id==None:

				raise ArgError()

			dico = super()._create_dico(self, index, card_id, set_code_cardmarket, set_name, name)
			
			if number==None:

				dico['num'] += 1

			else:

				dico['num'] += number

			super().add(index, dico)



class DatabaseCardmarket(DatabaseCard):

	def get_url(self, index):

		"""
		Return Cardmarket URL of card with index
		"""

		return 'https://www.cardmarket.com/en/YuGiOh/Products/Singles/' + self.db.loc[index, 'set_url_name'] + '/' + self.db.loc[index, 'url_name']

	def _create_dico(self, index, card_id, set_code_cardmarket=None, set_name=None, name=None, set_url_name=None, url_name=None):

		"""
		Create a dictionnary with input
		"""

		dico = {
			'set_code':[],
			'set_code_cardmarket':[],
			'set_name':[],
			'set_url_name':[],
			'card_code':[],
			'rarity':[],
			'card_id': [],
			'name':[],
			'url_name':[],
			'price':[]
		}
		dico_og = super()._create_dico(index, card_id, set_code_cardmarket, set_name, name)

		for key in dico_og:

			dico[key] = dico_og[key]

		try:

			len(index)	#test if input is a list of string or a string

			if set_url_name!=None and url_name!=None:

				for set_url in set_url_name:

					dico['set_url_name'].append(set_url)

				for url in url_name:

					dico['url_name'].append(url)

			else:

				if set_url_name==None:

					for code in dico['set_code']:

						dico['set_url_name'].append(self.db_set.loc[code, 'set_url_name'])

				else:

					for set_url in set_url_name:

						dico['set_url_name'].append(set_url)

				if url_name==None:

					for c_id in card_id:

						dico['url_name'].append(self.db_card.loc[c_id, 'url_name'])

				else:

					for url in url_name:

						dico['url_name'].append(url)

		except TypeError:

			if set_url_name==None:

				dico['set_url_name'] = self.db_set.loc[dico['set_code'], 'set_url_name']

			else:

				dico['set_url_name'] = set_url_name

			if url_name==None:

				dico['url_name'] = self.db_card.loc[card_id, 'url_name']

			else:

				dico['url_name'] = url_name

		return dico



	def add(self, index, card_id=None, set_code_cardmarket=None, set_name=None, set_url_name=None, name=None, url_name=None):

		"""
		Add a card to the cardmarket database
		WIP
		"""

		super().exist(index)

		if card_id==None:

			raise ArgError()

		dico = super()._create_dico(self, index, card_id, set_code_cardmarket, set_name, name)
			
		if number==None:

			dico['num'] += 1

		else:

			dico['num'] += number

		super().add(index, dico)

	def add_data(self, index, data):

		"""
		Add data to cardmarket database
		"""

		self.db.loc[index, 'data'].append(data)

	def pop_data(index):

		"""
		Pop last data of row with index
		"""

		self.db.loc[index, 'data'].pop(-1)

# db_cardmarket = DatabaseCardmarket(os.path.join(os.path.dirname(os.path.abspath(__file__)),'database','database_cardmarket.json'))