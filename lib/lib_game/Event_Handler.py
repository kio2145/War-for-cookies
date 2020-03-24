# -*- coding: utf-8 -*-
from pygame import *
from lib.lib_game.Core import Core
from lib.lib_game.Graphical_logic import Graphical_logic
from lib.lib_game.battle import Battle


'''
Created on 22 черв. 2013

@author: antimoskal
'''

class Event_Handler():

    def __init__(self):
        self.core = Core()
        self.graphical_logic = Graphical_logic()
        self.battle = Battle('1')

#Уровень шаманизма - 90! NE ПbTauTeCb ПОНЯТb БЕЗНОГNМ 
    def stage_0(self,event,fraction,days,action_to_map_coords,action_to_minimap_coords,last_x,last_y,filename,x_start,y_start):
        if (event[0]=='map_coords'):
            try:
                x_start,y_start = action_to_minimap_coords(last_x,last_y)# ВОТ ТЫ ГДЕ, СЦУКА!
            except AttributeError:
                #print 'lol'
                x_start,y_start = action_to_minimap_coords(event[2],event[3])# ВОТ ТЫ ГДЕ, СЦУКА!
            ##print 'Coords = '+str(event[2])+' '+str(event[3])
            stage, army_coords,id_army = action_to_map_coords(event[2],event[3],x_start,y_start)
            return stage,last_x,last_y,fraction,days, army_coords,id_army,x_start,y_start
        elif (event[0]=='minimap_coords'):
            x_start,y_start = action_to_minimap_coords(event[2],event[3])# ВОТ ТЫ ГДЕ, СЦУКА!
            stage = event[1]
            last_x = event[2]
            last_y = event[3]
            return stage,last_x,last_y,fraction,days, 0,0,x_start,y_start
        elif (event[0]=='save_mode'):
            stage = event[1]
            return stage,last_x,last_y,fraction,days, 0,0,x_start,y_start
        elif (event[0]=='load_mode'):
            stage = event[1]
            return stage,last_x,last_y,fraction,days, 0,0,x_start,y_start
        elif (event[0]=='end_of_army_steps'):
            #print 'end_of_army_steps'
            return stage,last_x,last_y,fraction,days, 0,0,x_start,y_start
        elif (event[0]=='base_mode'):
            stage = event[1]
            return stage,last_x,last_y,fraction,days, 0,0,x_start,y_start
        elif (event[0]=='end_of_players_steps'):
            if fraction == 1:
                self.graphical_logic.add_resources_for_current_fraction(fraction, filename)
                self.graphical_logic.change_all_armies_steps_for_fraction(fraction, filename)
                if (days+2)%10 == 0:
                    #print ' pivo'
                    self.graphical_logic.troops_generator(fraction, filename)                
                fraction = 2
                return 0,last_x,last_y,fraction,days, 0,0,x_start,y_start
            elif fraction == 2:
                self.graphical_logic.add_resources_for_current_fraction(fraction, filename)
                self.graphical_logic.change_all_armies_steps_for_fraction(fraction, filename)
                if (days+2)%10 == 0:
                    #print 'vodka'
                    self.graphical_logic.troops_generator(fraction, filename)    
                fraction = 1
                days +=1
                return 0,last_x,last_y,fraction,days, 0,0,x_start,y_start

        
    def stage_1(self,event,name_for_saving,filename,action_for_save,reload_window,last_x,last_y):
        action_for_save(name_for_saving)
        #print 'Lol = '+str(len(event))
        stage = event[1]
        if event[3] == 'continue':
            if len(name_for_saving) <10:
                name_for_saving += event[2]
                action_for_save(name_for_saving)
        if event[3] == 'backspace':
            if len(name_for_saving)>0:
                name_for_saving = name_for_saving[:-1]
                action_for_save(name_for_saving)
        if event[3] == 'save':
            if name_for_saving >2:
                self.core.save_file(name_for_saving,filename)
                name_for_saving = ''
                try:
                    reload_window(last_x,last_y)
                except AttributeError:
                    reload_window(0,0)
        if event[3] == 'cancel':
            name_for_saving = ''
            try:
                reload_window(last_x,last_y)
            except AttributeError:
                reload_window(0,0)
        return stage, name_for_saving
    
    def stage_2(self,event,name_for_loading,filename,action_for_load,reload_window,last_x,last_y):
        action_for_load(name_for_loading)
        #print 'Lol = '+str(len(event))
        stage = event[1]
        if event[3] == 'continue':
            if len(name_for_loading) <10:
                name_for_loading += event[2]
                action_for_load(name_for_loading)
        if event[3] == 'backspace':
            if len(name_for_loading)>0:
                name_for_loading = name_for_loading[:-1]
                action_for_load(name_for_loading)
        if event[3] == 'save':
            if name_for_loading >2:
                self.core.load_file(name_for_loading,filename)
                name_for_loading = ''
                try:
                    reload_window(last_x,last_y)
                except AttributeError:
                    reload_window(0,0)
        if event[3] == 'cancel':
            name_for_loading = ''
            try:
                reload_window(last_x,last_y)
            except AttributeError:
                reload_window(0,0)
        return stage, name_for_loading
    
    def stage_3(self,event,stage,moving_army,filename,id_army,last_x,last_y):
        armies_list = 0
        if (event[0] == 'move_army'):
            current_steps = self.graphical_logic.get_current_steps(id_army, filename)
            if current_steps > 0:
                try:
                    move, stage,last_x,last_y,armies_list = moving_army(event[1],event[2],last_x,last_y)
                except TypeError:
                    move = False
                if move == True:
                    self.graphical_logic.change_current_steps(id_army, filename, current_steps, -1)

        elif (event[0] == 'end_of_army_steps'):
            stage = event[1]
            armies_list = 0
        return stage,last_x,last_y,armies_list
    
    
    def stage_6(self,event,battle_dialog,stage,reload_window,last_x,last_y,armies_lists):
        #print event
        list = self.battle.auto_battle(armies_lists[0], armies_lists[1])
        #print list
        if event[0] == 'battle_mode':
            stage = event[1]
            #print stage
            #print event
            return stage
        
        else:
            stage = 6
            return stage
                
'''            

            if self.stage == 3:
                if (event[0] == 'move_army'):
                    self.moving_army(event[1],event[2])
                elif (event[0] == 'end_of_army_steps'):
                    self.stage = event[1]
'''                        