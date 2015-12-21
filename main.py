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
from kivy.storage.jsonstore import JsonStore
from os.path import join

# to generate uuid for new wisdom
import uuid

Builder.load_file('wisdoms.kv')

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.


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
#    print 'prve nbavi'
    good_text_id = StringProperty()
    good_text_id = 'List of most implemented wisdoms:' + '\n'
#    implemented_list = open('wisdoms.txt','r')
#    implemented_list = list(csv.reader(implemented_list,delimiter='|'))
#    sort = sorted(implemented_list,key=operator.itemgetter(1),reverse=True)
#    for eachline in sort:
#	good_text_line = eachline[:][0]
#        good_text_id = good_text_id +'\n' + ' '  + good_text_line + '\n'

class Will_tryScreen(Screen):
#    print 'bavi to'
    bad_text_id = StringProperty()
    bad_text_id = 'List of least implemented wisdoms:' + '\n'
#    will_try_list = open('wisdoms.txt','r')
 #   will_try_list = list(csv.reader(will_try_list,delimiter='|'))
 #   sort = sorted(will_try_list,key=operator.itemgetter(2),reverse=True)
 #   for eachline in sort:
 #       bad_text_line = eachline[:][0]
 #       bad_text_id = bad_text_id +'\n' + ' '  + bad_text_line + '\n'


class AddWisdomScreen(Screen):
    def callback_add_wisdom(self):
#       data_dir = App().user_data_dir
#       store = JsonStore(join(data_dir, 'wisdoms.json'))
        #store = JsonStore('wisdoms.json')
        # generate unique random number
#       import uuid
        new_uuid = uuid.uuid4().hex
	# use text from kv file based on id from kv file
        new_wisdom = self.ids.new_wisdom.text
        store.put( new_uuid, wisdom=new_wisdom, implemented='0', will_try='0')


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ImplementedScreen(name='implemented'))
sm.add_widget(Will_tryScreen(name='will_try'))
sm.add_widget(AddWisdomScreen(name='add_wisdom'))

class Wisdoms(App):
    def build(self):
        data_dir = App().user_data_dir
        store = JsonStore(join(data_dir, 'wisdoms.json'))

	#global data_dir
	global store
        return sm

if __name__ == '__main__':
    Wisdoms().run()
