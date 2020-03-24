# -*- coding: utf-8 -*-
import os
import re
import time

class Core():

    def __init__(self):
        pass

    def empty_map(self,map_type):
        self.map_type = map_type
        if self.map_type == 0:
            x = 50
            y = 50
        elif self.map_type == 1:
            x = 100
            y = 100
        elif self.map_type == 2:
            x = 150
            y = 150
        map_file = open ('temp', 'w')
        map_file.writelines(str(x)+'\n'+str(y)+'\n2\n')
        for i in range(y):
            for j in range(x):
                map_file.writelines('('+str(j)+';'+str(i)+';0;0;0)\n')
        map_file.close()
        self.file = 'temp'
        
    def save_file(self,name):
        map_file =open('temp','r')
        final_file = open(name,'w')
        temp = map_file.readlines()
        final_file.writelines(temp)
        final_file.close()
        map_file.close()
        self.file = name
    
    def load_file(self,name):
        self.file = name
        map_file = open(name,'r')
        x_coords = map_file.readline()
        y_coords = map_file.readline()
        map_file.seek(0)
        buff = map_file.readlines()
        map_file.close()
        if x_coords[:-1] == y_coords[:-1] == '50':
            self.map_type = 0
        elif x_coords[:-1] == y_coords[:-1] == '100':
            self.map_type = 1
        elif x_coords[:-1] == y_coords[:-1] == '150':
            self.map_type = 2
        self.file = 'temp'
        map_file = open(self.file,'w')
        map_file.writelines(buff)
        map_file.close()
            
    def change_cell(self,x,y,t,f,id_army):
        map_file = open(self.file,'r')
        lines = map_file.readlines()
        map_file.close()
        l = ''
        for i in range(len(lines)):
            l+=lines[i]
        #print str(x)+'[;]'+str(y)
        a = re.search('[(]'+str(x)+'[;]'+str(y)+'[;][0-9]{1,2}[;][0-2][;][0-9]+[)]',l)
        if a!=None:
            base_line = a.group(0)
        new_line = '('+str(x)+';'+str(y)+';'+str(t)+';'+str(f)+';'+str(id_army)+')' 
        file = open(self.file,'w')
        file.writelines(l.replace(base_line,new_line))
        file.close()
    
    def get_cell_information(self,line):
        #Ололо я індус
        result = []
        x = re.search('[(][0-9]{1,3}[;]', line)
        x = x.group(0)
        len_x = len(x)
        x = x[1:]
        x = x[:-1]
        
        result.append(int(x))
        y = re.search('[(][0-9]{1,3}[;][0-9]{1,3}[;]', line)
        y = y.group(0)
        len_y = len(y)
        y = y[len_x:]
        y = y[:-1]

        result.append(int(y))
        t = re.search('[(][0-9]{1,3}[;][0-9]{1,3}[;][0-9]{1,2}[;]', line)
        t = t.group(0)
        len_t = len(t)
        t = t[len_y:]
        t = t[:-1]

        result.append(int(t))
        f = re.search('[(][0-9]{1,3}[;][0-9]{1,3}[;][0-9]{1,2}[;][0-2][;]', line)
        f = f.group(0)
        temp_len = len(f)
        f = f[len_t:]
        f = f[:-1]

        result.append(int(f))
        id_army = re.search('[(][0-9]{1,3}[;][0-9]{1,3}[;][0-9]{1,2}[;][0-2][;][0-9]+', line)
        id_army = id_army.group(0)
        id_army = id_army[temp_len:]
        result.append(int(id_army))
        return result               

    def get_army_information(self,line):
        #Ололо я індус дубль 2
        #коли буде зайвий час - переробити
        result, x, len_x = []
        for i in range(7):
            x.append('')
            len_x.append(0)
        x[0] = re.search('[(][0-9]{1,3}[;]', line)# id_army
        x[0] = x[0].group(0)
        len_x[0] = len(x[0])
        x[0] = x[0][1:]
        x[0] = x[0][:-1]
        
        result.append(int(x[0]))
        x[1] = re.search('[(][0-9]{1,3}[;][0-9]{1,4}[;]', line)#u_1
        x[1] = x[1].group(0)
        len_x[1] = len(x[1])#len_y
        x[1] = x[1][len_x[0]:]
        x[1] = x[1][:-1]

        result.append(int(x[1]))
        x[2] = re.search('[(][0-9]{1,3}[;][0-9]{1,4}[;][0-9]{1,4}[;]', line)#u_2
        x[2] = x[2].group(0)
        len_x[2] = len(x[2])
        x[2] = x[2][len_x[1]:]
        x[2] = x[2][:-1]

        result.append(int(x[2]))
        x[3] = re.search('[(][0-9]{1,3}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;]', line)#u_3
        x[3] = x[3].group(0)
        len_x[3] = len(x[3])
        x[3] = x[3][len_x[2]:]
        x[3] = x[3][:-1]

        result.append(int(x[3]))
        x[4] = re.search('[(][0-9]{1,3}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;]', line)#u_4
        x[4] = x[4].group(0)
        len_x[4] = len(x[4])
        x[4] = x[4][len_x[3]:]
        x[4] = x[4][:-1]
        
        result.append(int(x[4]))
        x[5] = re.search('[(][0-9]{1,3}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;]', line)#u_5
        x[5] = x[5].group(0)
        len_x[5] = len(x[5])
        x[5] = x[5][len_x[4]:]
        x[5] = x[5][:-1]

        result.append(int(x[5]))
        x[6] = re.search('[(][0-9]{1,3}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,2}', line)#count
        x[6] = x[6].group(0)
        len_x[6] = len(x[6])
        x[6] = x[6][len_x[5]:]
        x[6] = x[6][:-1]
        result.append(int(x[6]))
        return result
    #СВЯТА ДЖИГУРДА! Мені соромно за ті верхні два шматки коду :((((((( 
    
    def load_cells(self,x,y):
        map_file = open(self.file,'r')
        lines = map_file.readlines()
        l = ''
        for i in range(len(lines)):
            l+=lines[i]
        map_file.seek(0)
        max1 = map_file.readline()
        max2 = map_file.readline()
        map_file.close()
        a = int(max1) - x
        b = int(max2) - y
        if (x < 25):
            self.x_coord_start = 0
            self.x_coord_end = 25
        elif(a<25):
            self.x_coord_start = int(max1)-25
            self.x_coord_end = int(max1)
        else:
            self.x_coord_start = x-13
            self.x_coord_end = x+12
        if (y < 25):
            self.y_coord_start = 0
            self.y_coord_end = 25
        elif(b<25):
            self.y_coord_start = int(max2)-25
            self.y_coord_end = int(max2)
        else:
            self.y_coord_start = y-13
            self.y_coord_end = y+12
        list_coords = []
        #print str(self.x_coord_start)+' '+ str(self.x_coord_end)+ ' ' + str(self.y_coord_start)+ ' ' + str(self.y_coord_end)
        for j in range(self.x_coord_start,self.x_coord_end):
            for k in range(self.y_coord_start,self.y_coord_end):
                a = re.search('[(]'+str(k)+'[;]'+str(j)+'[;][0-9]{1,2}[;][0-2][;][0-9]+[)]',l)
                if a!= None:
                    list_coords.append(self.get_cell_information(a.group(0)))
        return list_coords

    def load_cells_for_transparent_textures(self,x,y):
        map_file = open(self.file,'r')
        lines = map_file.readlines()
        l = ''
        for i in range(len(lines)):
            l+=lines[i]
        map_file.seek(0)
        max1 = int(map_file.readline())
        max2 = int(map_file.readline())
        map_file.close()
        result = []
        
        for i in range(0,3):
            for j in range(3):
                #if (((x-1+i)>=0) or ((y-1+j)>=0) or ((x-1+i)<=max1) or ((y-1+j)<=max2)):
                if (((x-1+i)>=0) and ((y-1+j)>=0)) and (((x-1+i)<=max1) and ((y-1+j)<=max2)):
                    a = re.search('[(]'+str(x-1+i)+'[;]'+str(y-1+j)+'[;][0-9]{1,2}[;][0-2][;][0-9]+[)]',l)
                    if a!=None:
                        result.append(self.get_cell_information(a.group(0)))
        return result
           
    def load_minimap_cells(self):
        map_file = open(self.file,'r')
        lines = map_file.readlines()
        l = ''
        for i in range(len(lines)):
            l+=lines[i]
        map_file.seek(0)
        max1 = map_file.readline()
        max2 = map_file.readline()
        map_file.close()
        list_coords = []
        a = re.findall('[(][0-9]{1,3}[;][0-9]{1,3}[;][0-9]{1,2}[;][0-2][;][0-9]+[)]',l)
        for i in range(int(max1)*int(max2)):
           list_coords.append(self.get_cell_information(a[i]))
        return list_coords

    def load_army(self):
        map_file = open(self.file,'r')
        lines = map_file.readlines()
        l = ''
        for i in range(len(lines)):
            l+=lines[i]
        map_file.close()
        list_army = []
        a = re.findall('[(][0-9]{1,3}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,2}[)]',l)
        for i in range(len(a)):
           list_army.append(self.get_army_information(a[i]))
        return list_army          
#[(][0-9]{1,3}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,4}[;][0-9]{1,2}[)]