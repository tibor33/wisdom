import kivy
kivy.require('1.0.6')

# for user home
#import kivy.app
#import shutil

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

#from random import randint
import random

# need for using handles to labels
from kivy.properties import ObjectProperty, StringProperty

# to work with Json
from os.path import join
import json

# to generate uuid for new wisdom
import uuid

# for dict sorting
from collections import OrderedDict


Builder.load_file('wisdoms.kv')

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.


### Functions definition

def readExistingDictStore():
    data_dir = App().user_data_dir
    with open(join(data_dir, 'wisdoms.json')) as f:
        return json.load(f)
    f.close()

########################



# Declare all screens
class MainScreen(Screen):
    # initialize handle/text of label
    wisdom_text_id = StringProperty()

    def callback_get_wisdom(self):
	# get wisdom ids from json store
	wisdom_uuids = list(store)
	# get random uuid of wisdom
	wisdom_index =  random.choice(wisdom_uuids)
	# update handle of label with text of wisdom
	self.wisdom_text_id = store.get(wisdom_index)['wisdom']
	
	# to use uuid in Good and Bad update
	global wisdom_index	
#        good_text_id = StringProperty()
#        good_text_id = 'List of most implemented wisdoms:' + '\n'


    def callback_update_GOOD(self):
	current_GOOD = int(store.get(wisdom_index)['implemented'] )
	current_GOOD += 1
	temp_wisdom_text = store.get(wisdom_index)['wisdom']
	temp_will_try = store.get(wisdom_index)['will_try']
	# whole entry needs to be reentered to update one field
        store.put(wisdom_index, implemented=current_GOOD, wisdom=temp_wisdom_text, will_try=temp_will_try )
	
    def callback_update_BAD(self):
        current_BAD = int(store.get(wisdom_index)['will_try'] )
        current_BAD += 1
        temp_wisdom_text = store.get(wisdom_index)['wisdom']
        temp_implemented = store.get(wisdom_index)['implemented']
        # whole entry needs to be reentered to update one field
        store.put(wisdom_index, implemented=temp_implemented, wisdom=temp_wisdom_text, will_try=current_BAD )


class MenuScreen(Screen):
    pass
class ImplementedScreen(Screen):
    good_text_id = StringProperty()
    good_text_id = 'List of most implemented wisdoms:' + '\n'

    # load json dict
    dictName = readExistingDictStore()
    # sort dict based on least implemented wisdoms
    tempSortedDict = OrderedDict(sorted(dictName.items(), reverse=True ,key=lambda (x,y): int(y['implemented']))    )

    OrderNum = 1 # number of wisdom in display
    # iterate through ordered dict and print only wisdoms
    for i,j in tempSortedDict.items():
        good_text_id = good_text_id +'\n' + str(OrderNum)  + '.  ' + j['wisdom'] + '       ' + str(j['implemented'])  + '\n'
        OrderNum +=1


class Will_tryScreen(Screen):
    bad_text_id = StringProperty()
    bad_text_id = 'List of least implemented wisdoms:' + '\n'
    # load json dict
    dictName = readExistingDictStore()
    # sort dict based on least implemented wisdoms
    tempSortedDict = OrderedDict(sorted(dictName.items(), reverse=True ,key=lambda (x,y): int(y['will_try']))    )

    OrderNum = 1 # number of wisdom in display
    # iterate through ordered dict and print only wisdoms
    for i,j in tempSortedDict.items():
	bad_text_id = bad_text_id +'\n' + str(OrderNum)  + '.  ' + j['wisdom'] + '       ' + str(j['will_try'])  + '\n'
	OrderNum +=1

class AddWisdomScreen(Screen):
    
    def callback_add_wisdom(self):
        # generate unique random number
        new_uuid = uuid.uuid4().hex
	# use text from kv file based on id from kv file
        new_wisdom = self.ids.new_wisdom.text
	# read existing dict store
	wisdom_dict = Wisdoms().readExistingDictStore()
	# add new entry into dict
	wisdom_dict[new_uuid] = {'implemented': '0', 'will_try': '0', 'wisdom': new_wisdom}
	# save newly edited dict to json file
	Wisdoms().saveChanges(wisdom_dict)
	# get back to main screen
	sm.current = 'main'

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ImplementedScreen(name='implemented'))
sm.add_widget(Will_tryScreen(name='will_try'))
sm.add_widget(AddWisdomScreen(name='add_wisdom'))

class Wisdoms(App):
    def build(self):
        return sm

    # func for loading existing json dict
    def readExistingDictStore(self):
	data_dir = App().user_data_dir
        with open(join(data_dir, 'wisdoms.json')) as f:
            return json.load(f)
        f.close()

    # func for saving edited dict to defioned json file
    def saveChanges(self,dictName):
	data_dir = App().user_data_dir
        f = open(join(data_dir, 'wisdoms.json'),'w')
        json.dump(dictName,f)
        f.close()


if __name__ == '__main__':
    Wisdoms().run()
