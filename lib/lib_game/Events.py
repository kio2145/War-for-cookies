# -*- coding: utf-8 -*-
'''
Created on 15 черв. 2013

@author: antimoskal
'''
import pygame,re
import sys, lib.lib_game.Window

class Events():
  
    def __init__(self):
        pygame.init()
        pass
    
    def get_map_coords(self,click_coords,step):        
            x_coord = (click_coords[0]-20)//step
            y_coord = (click_coords[1])//step
            return x_coord, y_coord
    
    def get_minimap_coords(self,click_coords,step):
            minimap_x = (click_coords[0]-800)//step
            minimap_y = (click_coords[1])//step
            return minimap_x, minimap_y
    
    def get_battle_mode(self,click_coords):
        mode = (click_coords[0]-300)//100
        return mode
    
    def get_buttons_type(self,stage,click_coords):
            type = (click_coords[1])//175
            if ((type == 0) and (stage == 3)):
                return ['end_of_army_steps',0]            
            elif type == 1:
                return ['base_mode',4]
            elif type == 2:
                pass
            elif type == 3:
                return ['end_of_players_steps',stage]
                
    def move_coords(self):
        if self.event.key ==pygame.K_DOWN:
            return ['move_army', 1, 0]
        
        if self.event.key ==pygame.K_UP:
            return ['move_army', -1, 0]
        
        if self.event.key ==pygame.K_LEFT:
            return ['move_army', 0, -1]
        
        if self.event.key ==pygame.K_RIGHT:
            return ['move_army', 0, 1]
    
    def mousebuttondown_terms(self, stage, click_coords,big_step,step_p):
        if (click_coords[0]>=1150):
            return self.get_buttons_type(stage, click_coords)     
        if stage == 0:
            if ((click_coords[0] > 20) and (click_coords[1] > 0) and (click_coords[0] < 720) and (click_coords[1] < 700)):        
                x, y = self.get_map_coords(click_coords,big_step)
                return ['map_coords', stage, x, y]
            elif ((click_coords[0] > 800) and (click_coords[1] > 0) and (click_coords[0] < 1100) and (click_coords[1] < 300)):
                x, y = self.get_minimap_coords(click_coords,step_p)
                return ['minimap_coords',stage,x,y]           
            else:
                return None
        if stage == 6:
            if (click_coords[1]>450 and click_coords[1]<500):
                mode = self.get_battle_mode(click_coords)
                if mode == 0:
                    stage = 7
                if mode == 1:
                    stage = 8
                if mode == 2:
                    stage = 3

                return ['battle_mode',stage]

    def keydown_terms(self,stage):
        if stage == 0:
            if self.event.key == pygame.K_F5:
                stage = 1
                return ['save_mode', stage]
            if self.event.key == pygame.K_F7:
                stage = 2
                return ['load_mode', stage]
        if (stage == 1) or (stage == 2):
            if (stage == 1):
                mode = 'save_mode'
            if (stage == 2):
                mode = 'load_mode'
            if self.event.key == pygame.K_ESCAPE:
                stage = 0
                return [mode, stage, '', 'cancel']
            elif self.event.key == pygame.K_RETURN:
                if stage == 1:
                    text = 'save'
                elif stage ==2:
                    text = 'load'
                stage = 0
                return [mode, stage, '', text]
            elif self.event.key == pygame.K_BACKSPACE:
                return [mode, stage, '', 'backspace']
            else:
                name_key =(re.search('[a-z,_,0-9]',pygame.key.name(self.event.key)))
                if name_key != None:
                    text = (name_key).group(0) 
                    return [mode, stage, text, 'continue']
                else:
                    return [mode, stage, '', 'continue']
        if (stage == 3):
            return self.move_coords() 
        
    def get_event(self,stage,big_step,step_p):#,flag):
        for self.event in pygame.event.get():
            if self.event.type == pygame.MOUSEBUTTONDOWN:
                if self.event.button == 1:
                    click_coords = self.event.pos
                    return self.mousebuttondown_terms(stage, click_coords, big_step, step_p)
            if self.event.type == pygame.QUIT:
                sys.exit()
            if self.event.type == pygame.KEYDOWN:
                return self.keydown_terms(stage)
                    #self.event_scan_keyes()
