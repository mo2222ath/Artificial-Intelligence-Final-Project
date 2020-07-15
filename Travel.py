# -*- coding: utf-8 -*-
"""
Created on Tue May 19 9:24:19 2020

@author: Moaaz - Yageen - Aya - Sara - Nadia
PID23868220
"""

import pandas as pd
import math

excel_file_name = 'C:\\Users\Moaaz\Desktop\AI_Project\Travel Agent2.xlsx'
travelAgent = pd.read_excel(excel_file_name)
travelAgent2 = pd.read_excel(excel_file_name , sheet_name='Cities')
Source = travelAgent['Source'].values.tolist()
Destination = travelAgent['Destination'].values.tolist()
DepartureTime = travelAgent['Departure Time'].values.tolist()
ArrivalTime = travelAgent['Arrival Time'].values.tolist()
FlightNumber = travelAgent['Flight Number'].values.tolist()
ListofDays = travelAgent['List of Days']
Cities = travelAgent2['City'].values.tolist()
Latitude = travelAgent2['Latitude'].values.tolist()
Longitude = travelAgent2['Longitude'].values.tolist()
days = ['sat','sun', 'mon','tue','wed','thu','fri']

# to remove all spaces in Source and Destination
for s in range(len(Source)):
    Source[s] = Source[s].replace(" ","")
for d in range(len(Destination)):
    Destination[d] = Destination[d].replace(" ","")


# to claculate the G
def claculate_g(D,A):
    H = abs(D.hour - A.hour)
    M = abs(D.minute - A.minute)
    return H + (M/60)

# to claculate the H
def calculate_h(x,y,parent):
    if parent == None:
        return math.sqrt((x - 0)**2 + (y-0)**2)
    else:
        return math.sqrt((x - parent.x)**2 + (y - parent.y)**2)

# Node for take info about the city
class Node:
    def __init__(self, name , parent , index):
        self.name = name
        self.parent = parent
        self.Arrival = ArrivalTime[index]
        self.Departure = DepartureTime[index]
        self.FN = FlightNumber[index]
        self.Days = ListofDays[index][1:-1].split(',')
        index2 = Cities.index(self.name.replace(" ",""))
        self.x = Latitude[index2]
        self.y = Longitude[index2]
        if parent is None:
            self.g = 0
        else:
            self.g = parent.g + claculate_g(self.Departure,self.Arrival)
        self.h = calculate_h(self.x ,self.y,parent)
        self.f = self.g + self.h

    # To print node object with name and f value
    def __repr__(self):
        return str(self.name) + ' ,' + str(self.f)
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f

# to get the index of the city to get info for it take the source  and destination
def get_Index(s,d):
    SIndex = -1
    DIndex = -1

    for x in range(len(Source)):
        if s == Source[x]:
            SIndex = x
            break
    for y in range(SIndex , len(Destination)):
        if d == Destination[y]:
            DIndex = y
            break
    return DIndex , DIndex

# to get all cities that connect with source city
def getChaildern(name):
    child = []
    for x in range(len(Source)):
        if Source[x] == name:
            child.append(Destination[x])
    return child

# if found the gole city so it's get all path from gole to the start node by parent node
def getPath(current_node , start_node):
    path = []
    while current_node != start_node:
        path.append(current_node)
        current_node = current_node.parent
    path.append(start_node)
    # take the reverse path from start to gole
    NewPath = path[::-1]
    s, d = get_Index(NewPath[0].name,NewPath[1].name)
    New_node = Node(NewPath[0].name, None , s)
    NewPath[0] = New_node
    return NewPath

# check if node in open
def check_open(open, child):
    for node in open:
        if (child.name == node.name and child.f >= node.f):
            return False
        if (child.name == node.name):
            open.remove(node)
    return True

# check if node is visted
def check_visted(visted, child):
    for node in visted:
        if (child.name == node.name):
            return False
    return True

# the A star algorithem that get the shortest path from start node to gole
def A_search(start,gole):

    open = []
    visted = []

    # get the index of the start node to creat all info of it
    i = Source.index(start)
    start_node = Node(start, None , i)

    # add start node to open list
    open.append(start_node)

    # loop until the open list is empty thats tell us there is no path
    while len(open) > 0:

        # sort the open list depend on cost of F to take the lowest cost
        open.sort()
        current_node = open.pop(0)

        # add the current node to visted list
        visted.append(current_node)

        # here if found the gole path will return it
        if current_node.name == gole:
            return getPath(current_node , start_node)

        # get all childerns of the current node
        childs = getChaildern(current_node.name)

        # loop to all childs to check if in open list or is visted
        for child in childs:
            i1 , i2 = get_Index(current_node.name , child )
            Child  = Node(child, current_node ,i2)

            if(not check_visted(visted , Child)):
                continue

            if(check_open(open, Child) == True):
                open.append(Child)

    return None

# check if there is one day of the source city in the avalibale range of days
def Check_Days(list1,list2):
    for n in range(len(list1)):
        list1[n] = list1[n].replace(" ","")
    for s in range(len(list2)):
        list2[s] = list2[s].replace(" ","")

    for i in list1:
        if i in list2:
            return True
    return False

# to create the range of days
def rangeDays(listDays):
    i = days.index(listDays[0])
    j = days.index(listDays[1])
    return days[i:j+1]

# check if the path that founded is allowed in range of days or no
def printPath(path, allowedDays):
    i ,j = get_Index(path[0].name,path[1].name)
    notFound = True
    NewDays = []
    isDayExist = False
    allowedDays = rangeDays(allowedDays)
    # check days of the source path is allowed
    if Check_Days(allowedDays , path[0].Days):
        print('\n\nOutput:')
        print('Path is allowed in the departure days range of source: ', path[0].Days)
        print('Allowed path:')
        for p in range(len(path)):
            if p > 0:
                print('step ',p ,':' ,'Use flight ',path[p].FN, ' Form ', path[p].parent.name , 'to ', path[p].name , ' ,Departure Time :', path[p].Departure , ' , Arrival time :' , path[p].Arrival  )
    # if not allowed in source path I will check if there is a soucned flight number is allowed with it's days
    else:
        while True:
            isDaysInNewFN = True
            isSourceNotEqualDestination = True

            if Source[i] == path[0].name and Destination[j] == path[1].name:
                isSourceNotEqualDestination = False
                if path[0].FN == FlightNumber[j]:
                    isDaysInNewFN = False
                    isSourceNotEqualDestination = True
                    i = i+1
                    j = j+1
            if isDaysInNewFN:
                NewFN = FlightNumber[i]
                NewDays = ListofDays[i][1:-1].split(',')
                isDayExist = Check_Days( allowedDays , NewDays )
            if isDayExist:
                path[0].FN = NewFN
                path[0].Days = NewDays
                print('\n\nOutput:')
                print('Path is allowed in the departure days range of another Flight Number: ', path[0].Days)
                print('Allowed path:')
                for p in range(len(path)):
                    if p > 0:
                        print('step ',p ,':' ,'Use flight ',path[p-1].FN, ' Form ', path[p].parent.name , 'to ', path[p].name , ' ,Departure Time :', path[p].Departure , ' , Arrival time :' , path[p].Arrival  )
                break
            if isSourceNotEqualDestination:
                notFound = False
                break

        # if there is no flight number is allowed I will check day after and before the range
        if not notFound:
            indexS = days.index(allowedDays[0])
            indexE = days.index(allowedDays[-1])
            if indexS > 0 and indexS < 6:
                indexS = indexS - 1
            if indexE > 0 and indexE < 6:
                indexE = indexE + 1
            allowedDays = days[indexS:indexE+1]
            isDayExist = Check_Days( allowedDays , path[0].Days  )
            if isDayExist:
                print('\n\nOutput:')
                print('Path is allowed in the departure days of after and before the range available: ',allowedDays)
                print('Allowed path:')
                for p in range(len(path)):
                    if p > 0:
                        print('step ',p ,':' ,'Use flight ',path[p].FN, ' Form ', path[p].parent.name , 'to ', path[p].name , ' ,Departure Time :', path[p].Departure , ' , Arrival time :' , path[p].Arrival  )
            # if is not allowed after and before ranges I will print the path with available days
            else:
                print('No path avalaibal in allowed days !!')



def main():

    source = input("Please enter the source city: ")
    destination = input("Please enter the destination city: ")
    allowedDays = input("Please enter two days allowed for range (example Format: sun tue): ").split(' ')

    path = A_search(source, destination)
    if path != None:
        printPath(path , allowedDays)
    else:
        print('No Path avalaibe !!')

if __name__ == "__main__": main()

