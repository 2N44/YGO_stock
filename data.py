import os
import numpy as np
import database as db
import pandas as pd
import ygo_list as ylist

class Data(object):

    def __init__(self,list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'list','all_card.ycd')):

        self.data_raw =[]
        self.db_cardmarket = db.DatabaseCardmarket(os.path.join(os.path.dirname(os.path.abspath(__file__)),'database','database_cardmarket.json'))

        if list_path[-4:]=='.ycd':

            self.card_list = ylist.CodeList(list_path)

        elif list_path[-4:]=='.yid':

            self.card_list = ylist.IdList(list_path)

        elif list_path[-4:]=='.ydk':

            self.card_list = ylist.DeckList(list_path)

        else:

            raise FormatError()

        for code in self.card_list.card_code:

            self.data_raw.append(self.db_cardmarket.loc[code, 'data'])

        self.data = pd.DataFrame()

        for idx_code in range(len(self.card_list.card_code)):

            for data_dict in self.data_raw[idx_code]:

                data_dict['code'] = self.card_list.card_code[idx_code]
                self.data = self.data.append(pd.DataFrame(data_dict))

        self.data.set_index(['code', 'date'], inplace=True)

    def _filter(self, code=None, date=None, location=None, condition=None, language=None, first_ed=None, price=None, num_of_cards=None):

        """
        Create a boolean string from filters
        """

        filter_str = ''

        if code!=None:

            code_str = '(code == '

            if isinstance(code, (list, str)) and  [isinstance(x, str) for x in code if isinstance(code,list)]==[True for x in code if isinstance(code,list)]:

                code_str = code_str + str(code) + ')'

            filter_str += code_str

        if date!=None:

            date_str = '(date == '

            if isinstance(date, (list, str)) and  [isinstance(x, str) for x in date if isinstance(date,list)]==[True for x in date if isinstance(date,list)]:

                date_str = date_str + str(date) + ')'

                if len(filter_str)>0:

                    filter_str += ' and ' + date_str

                else:

                    filter_str+= date_str

        if location!=None:

            location_str = '(location == '

            if isinstance(location, (list, str)) and  [isinstance(x, str) for x in location if isinstance(location,list)]==[True for x in location if isinstance(location,list)]:

                location_str = location_str + str(location) + ')'

                if len(filter_str)>0:

                    filter_str += ' and ' + location_str

                else:

                    filter_str+= location_str

        if condition!=None:

            condition_str = '(condition == '

            if isinstance(condition, (list, str)) and  [isinstance(x, str) for x in condition if isinstance(condition,list)]==[True for x in condition if isinstance(condition,list)]:

                condition_str = condition_str + str(condition) + ')'

                if len(filter_str)>0:

                    filter_str += ' and ' + condition_str

                else:

                    filter_str+= condition_str

        if language!=None:

            language_str = '(language == '

            if isinstance(language, (list, str)) and  [isinstance(x, str) for x in language if isinstance(language,list)]==[True for x in language if isinstance(language,list)]:

                language_str = language_str + str(language) + ')'

                if len(filter_str)>0:

                    filter_str += ' and ' + language_str

                else:

                    filter_str+= language_str

        if first_ed!=None:

            first_ed_str = '(first_ed == '

            if isinstance(first_ed, (list, str)) and  [isinstance(x, str) for x in first_ed if isinstance(first_ed,list)]==[True for x in first_ed if isinstance(first_ed,list)]:

                first_ed_str = first_ed_str + str(first_ed) + ')'

                if len(filter_str)>0:

                    filter_str += ' and ' + first_ed_str

                else:

                    filter_str+= first_ed_str

        if price!=None:

            price_str = '(price == '

            if isinstance(price, (list, str)) and  [isinstance(x, str) for x in price if isinstance(price,list)]==[True for x in price if isinstance(price,list)]:

                price_str = price_str + str(price) + ')'

                if len(filter_str)>0:

                    filter_str += ' and ' + price_str

                else:

                    filter_str+= price_str

        if num_of_cards!=None:

            num_of_cards_str = '(num_of_cards == '

            if isinstance(num_of_cards, (list, str)) and  [isinstance(x, str) for x in num_of_cards if isinstance(num_of_cards,list)]==[True for x in num_of_cards if isinstance(num_of_cards,list)]:

                num_of_cards_str = num_of_cards_str + str(num_of_cards) + ')'

                if len(filter_str)>0:

                    filter_str += ' and ' + num_of_cards_str

                else:

                    filter_str+= num_of_cards_str

        return filter_str

        def filter(self, code=None, date=None, location=None, condition=None, language=None, first_ed=None, price=None, num_of_cards=None):

            """
            Return filtered data, if no filter input the data is reset to the original data
            """

            filter_str = self._filter(code, date, location, condition, language, first_ed, price,num_of_cards)

            self._data = self.data

            if filter_str == '':

                self.data = self._data

            else:

                self.data = self.data.query(filter_str)


            




