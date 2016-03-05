import kivy
kivy.require('1.0.6')

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


# testing button lists
from kivy.uix.listview import ListItemButton
from kivy.properties import ListProperty, NumericProperty


Builder.load_file('wisdoms.kv')

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

### Functions definition

def readExistingDictStore():
    data_dir = App().user_data_dir
    f = open(join(data_dir, 'wisdoms.json'),'r')
    return json.load(f)
    f.close()

# func for saving edited dict to defined json file
def saveChanges(dictName):
    data_dir = App().user_data_dir
    f = open(join(data_dir, 'wisdoms.json'),'w')
    json.dump(dictName,f)
    f.close()

########################

# Declare all screens
class MainScreen(Screen):
    # initialize handle/text of label
    wisdom_text_id = StringProperty()

    def callback_get_wisdom(self):
	# load json dict
        tempDict = readExistingDictStore()
	# randomly choose one hashkey from all keys
	wisdom_index = random.choice(tempDict.keys()[:])
	# get only one random wisdom
	self.wisdom_text_id = tempDict.get(wisdom_index)['wisdom']
        # set global to use uuid in Good and Bad update
        global wisdom_index

    def callback_update_GOOD(self):
	tempDict = readExistingDictStore()
	current_GOOD = int(tempDict.get(wisdom_index)['implemented'])
	current_GOOD += 1
	# we must retrieve all values and put them back (that's how dict is updated)
	tempWillTry = tempDict.get(wisdom_index)['will_try']
	tempWisdomText = tempDict.get(wisdom_index)['wisdom']
	tempDict[wisdom_index] = {'implemented': str(current_GOOD), 'will_try': tempWillTry, 'wisdom': tempWisdomText}
	saveChanges(tempDict)

	
    def callback_update_BAD(self):
	tempDict = readExistingDictStore()
	current_BAD = int(tempDict.get(wisdom_index)['will_try'])
	current_BAD += 1
	# we must retrieve all values and put them back (that's how dict is updated)
	tempImplemented = tempDict.get(wisdom_index)['implemented']
	tempWisdomText = tempDict.get(wisdom_index)['wisdom']
	tempDict[wisdom_index] = {'implemented': tempImplemented, 'will_try': str(current_BAD), 'wisdom': tempWisdomText}
	saveChanges(tempDict)

#	current_BAD = int(store.get(wisdom_index)['will_try'] )
#        current_BAD += 1
#        temp_wisdom_text = store.get(wisdom_index)['wisdom']
#        temp_implemented = store.get(wisdom_index)['implemented']
#        # whole entry needs to be reentered to update one field
#        store.put(wisdom_index, implemented=temp_implemented, wisdom=temp_wisdom_text, will_try=current_BAD )
#

class MenuScreen(Screen):
    pass



class ImplementedScreen(Screen):
    good_text_id = StringProperty()
    def callback_show_ordered_GOOD(self):    
        print "function is being called"
	#good_text_id = StringProperty()
        self.good_text_id = 'List of most implemented wisdoms:' + '\n'
        # load json dict
        tempDict = readExistingDictStore()
        # sort dict based on least implemented wisdoms
        tempSortedDict = OrderedDict(sorted(tempDict.items(), reverse=True ,key=lambda (x,y): int(y['implemented']))    )
        OrderNum = 1 # number of wisdom in display
        # iterate through ordered dict and print only wisdoms
        for i,j in tempSortedDict.items():
            self.good_text_id = self.good_text_id +'\n' + str(OrderNum)  + '.  ' + j['wisdom'] + '       ' + str(j['implemented'])  + '\n'
            OrderNum +=1



class Will_tryScreen(Screen):
    bad_text_id = StringProperty()


#>>>
#    task_input = ObjectProperty()
#    task_list = ObjectProperty()
    my_list = StringProperty()
#<<<

    def callback_show_ordered_BAD(self):
        self.bad_text_id = 'List of least implemented wisdoms:' + '\n'
        # load json dict
        dictName = readExistingDictStore()
        # sort dict based on least implemented wisdoms
        tempSortedDict = OrderedDict(sorted(dictName.items(), reverse=True ,key=lambda (x,y): int(y['will_try']))    )
        OrderNum = 1 # number of wisdom in display
        # iterate through ordered dict and print only wisdoms
        for i,j in tempSortedDict.items():
            self.bad_text_id = self.bad_text_id +'\n' + str(OrderNum)  + '.  ' + j['wisdom'] + '       ' + str(j['will_try'])  + '\n'
    	    OrderNum +=1


#>>>
	self.my_list = self.bad_text_id
        #self.my_list = "aleho"
    
#	text = "abc"
#        self.task_list.adapter.data.extend([self.task_input.text])
#

#    task_input = ObjectProperty()
#    task_list = ObjectProperty()
#
#    def add_task(self):
#        self.task_list.adapter.data.extend([self.task_input.text])
#        self.task_list._trigger_reset_populate()


#<<<



class AddWisdomScreen(Screen):
    
    def callback_add_wisdom(self):
        # generate unique random number
        new_uuid = uuid.uuid4().hex
	# use text from kv file based on id from kv file
        new_wisdom = self.ids.new_wisdom.text
	# read existing dict store
	wisdom_dict = readExistingDictStore()
	# add new entry into dict
	wisdom_dict[new_uuid] = {'implemented': '0', 'will_try': '0', 'wisdom': new_wisdom}
	# save newly edited dict to json file
	#Wisdoms().saveChanges(wisdom_dict)
	saveChanges(wisdom_dict)
	# get back to main screen
	sm.current = 'main'


###############
# define button to display in list and tied it with kv file
class MenuButton(ListItemButton):
    index = NumericProperty(0)

    def on_menu_selection(self):
        print "olala"
#        sm.current = 'main'



#in order to listview work thsi must be somehow registered and tied together
from kivy.factory import Factory
Factory.register('MenuButton', cls=MenuButton)

##############


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ImplementedScreen(name='implemented'))
sm.add_widget(Will_tryScreen(name='will_try'))
sm.add_widget(AddWisdomScreen(name='add_wisdom'))

# main class for building app
class Wisdoms(App):

#    data = ListProperty(["Item #{0}".format(i) for i in range(50)])

    def build(self):
        return sm




if __name__ == '__main__':
    Wisdoms().run()
