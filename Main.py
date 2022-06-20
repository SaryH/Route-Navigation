import csv
import pandas as pd
import copy
from tkinter import *

# open the csv file (dataset) and read it
data = pd.read_csv('Cities.csv')
data.rename(columns={"Unnamed: 0": ""}, inplace = True)
data.set_index("", inplace=True)

city_names = pd.DataFrame (data.columns, columns = ['City'])

graph = []
for i in data.columns:
    cityList = []
    dataList = []
    for j in data[i]:
        if j.count(',') == 2:
            cityList.append(data.index[data[i] == j][0])
            dataList.append(j)
            #print(data.index[data[i] == j][0])
            #print(j)
    #rint(cityList)
    #rint(dataList)
    city = {'City': cityList, i: dataList}
    city = pd.DataFrame(city)
    #city.set_index('', inplace=True)
    graph.append(city)

def BFS(graph, Start, Goal):
    # print("Running Breath First Search")
    que = list()  # to be used as a stack
    path = list()  # to keep track of the visited nodes
    temp = Start
    que.append(temp)
    while len(que) > 0:
        temp = que.pop(0)  # poping out the top element from stack

        if path.count(temp) < 1:  # ckecking if the node has been visited
            if graph[city_names.query('City == ' + '"' + temp + '"').index[
                0]] is not None:  # checking if the node is a terminal
                for i in graph[city_names.query('City == ' + '"' + temp + '"').index[0]]['City']:
                    que.append(i)  # pushing in to the stack
            path.append(temp)  # enqueing the visited node to the path

        if temp == Goal:  # checking if recently visited is a GOAL
            break  # will break out if reached the GOAL node

    path, cost = checkPath(data, path, Goal)
    route = ""
    if temp == Goal:
        # print("starting search-->", end=" ")
        route = path[0]
        for i in range(len(path) - 1):
            route = route + " --> " + path[i + 1]
            # print(i, "-->", end=" ")
        # print("reached GOAL")
        # print(route)
        # print("Cost = " + str(cost))
        return route

    if len(que) == 0:
        # print("starting search-->", end=" ")
        # print("No path exist")
        route = "No path exist!"
    # print('End')


def checkPath(data, path, Goal):
    newPath = []
    flag = 0
    newPath.insert(0, Goal)
    for i in range(len(path), 0, -1):
        if newPath[0] != path[0]:
            for j in range(i):
                if newPath[0] in graph[city_names.query('City == ' + '"' + path[j] + '"').index[0]]['City'].tolist():
                    newPath.insert(0, path[j])
                    break
    cost = 0
    for i in range(len(newPath) - 1):
        cost += int(data[newPath[i]][newPath[i + 1]].split(',')[1])
    return newPath, cost


def DFS(graph, Start, Goal):
    # print("Running Depth First Search")
    que = list()  # to be used as a queue
    path = list()  # to keep track of the visited nodes
    temp = Start
    que.append(temp)
    while len(que) > 0:
        temp = que.pop()  # dequeueing the top element from the queue

        if path.count(temp) < 1:  # ckecking if the node has been visited
            if graph[city_names.query('City == ' + '"' + temp + '"').index[
                0]] is not None:  # checking if the node is a terminal
                for i in graph[city_names.query('City == ' + '"' + temp + '"').index[0]]['City']:
                    que.append(i)  # enqueing in the queue
            path.append(temp)  # enqueing the visited node to the path

        if temp == Goal:  # checking if recently visited is a GOAL
            break  # will break out if reached the GOAL node

    route = ''
    if temp == Goal:
        # print("starting search-->", end=" ")
        route = path[0]
        for i in range(len(path) - 1):
            route = route + " --> " + path[i + 1]
            # print(i, "-->", end=" ")
        # print("reached GOAL")
        return route

    if len(que) == 0:
        # print("starting search-->", end=" ")
        # print("No path exist")
        route = 'No path exist!'

def Greedy(graph, start,final):
    #print("Running Best First Search")
    path = []
    priorityQueue = [[[start], data[start][final].split(',')[0]]]
    visited = []
    route = ''

    while priorityQueue != []:
        path.append(priorityQueue.pop(0))
        node = path[-1][0][-1]
        visited.append(node)

        if node == final:
            finalPath = copy.deepcopy(path[-1])
            #print("starting search-->", end=" ")
            route = finalPath[0][0]
            for i in range(len(finalPath[0])-1):
                route = route + " --> " + finalPath[0][i+1]
                #print(i, "-->", end=" ")
            #print("reached GOAL")
            return route

        for neighbor in graph[city_names.query('City == ' + '"' + node + '"').index[0]]['City'].tolist():
            if neighbor not in visited:
                newPath = copy.deepcopy(path[-1])
                newPath[0].append(neighbor)
                newPath[1] = data[neighbor][final].split(',')[0]
                priorityQueue.append(newPath)

        priorityQueue.sort(key=lambda x:x[1])

#bestFirstSearch(graph, 'Ramallah','Bethlehem')

def aStarAerial(graph, start, final):
    # print("Running Best First Search")
    path = []
    if len(data[start][final].split(',')) == 3:
        priorityQueue = [[[start], int(data[start][final].split(',')[0]) + int(data[start][final].split(',')[1])]]
    else:
        priorityQueue = [[[start], int(data[start][final].split(',')[1])]]
    visited = []
    route = ''

    while priorityQueue != []:
        path.append(priorityQueue.pop(0))
        node = path[-1][0][-1]
        visited.append(node)

        if node == final:
            finalPath = copy.deepcopy(path[-1])
            # print("starting search-->", end=" ")
            route = finalPath[0][0]
            for i in range(len(finalPath[0]) - 1):
                route = route + " --> " + finalPath[0][i + 1]
                # print(i, "-->", end=" ")
            # print("reached GOAL")
            return route

        if path.count(node) < 1:
            for neighbor in graph[city_names.query('City == ' + '"' + node + '"').index[0]]['City'].tolist():
                if neighbor not in visited:
                    newPath = copy.deepcopy(path[-1])
                    newPath[0].append(neighbor)
                    # print(newPath[0])
                    # print(data[neighbor][final].split(','))
                    newPath[0], cost = checkPath(data, newPath[0], neighbor)
                    # print(cost)
                    if neighbor == final:
                        newPath[1] = cost
                    else:
                        newPath[1] = int(data[neighbor][final].split(',')[0]) + cost
                    # print(newPath[-1])
                    priorityQueue.append(newPath)

        priorityQueue.sort(key=lambda x: x[1])

# aStarAerial(graph, 'Hebron','Yafa')

def aStarWalk(graph, start, final):
    # print("Running Best First Search")
    path = []
    # print(data[start][final].split(','))
    if len(data[start][final].split(',')) == 3:
        priorityQueue = [[[start], int(data[start][final].split(',')[2]) + int(data[start][final].split(',')[1])]]
    else:
        priorityQueue = [[[start], int(data[start][final].split(',')[1])]]
    visited = []
    route = ''

    while priorityQueue != []:
        path.append(priorityQueue.pop(0))
        node = path[-1][0][-1]
        visited.append(node)

        if node == final:
            finalPath = copy.deepcopy(path[-1])
            # print("starting search-->", end=" ")
            route = finalPath[0][0]
            for i in range(len(finalPath[0]) - 1):
                route = route + " --> " + finalPath[0][i + 1]
                # print(i, "-->", end=" ")
            # print("reached GOAL")
            return route

        if path.count(node) < 1:
            for neighbor in graph[city_names.query('City == ' + '"' + node + '"').index[0]]['City'].tolist():
                if neighbor not in visited:
                    newPath = copy.deepcopy(path[-1])
                    newPath[0].append(neighbor)
                    # print(newPath[0])
                    # print(data[neighbor][final].split(','))
                    newPath[0], cost = checkPath(data, newPath[0], neighbor)
                    # print(cost)
                    if neighbor == final:
                        newPath[1] = cost
                    else:
                        if len(data[neighbor][final].split(',')) == 3:
                            newPath[1] = int(data[neighbor][final].split(',')[2]) + cost
                        else:
                            newPath[1] = int(data[neighbor][final].split(',')[1]) + cost
                    # print(newPath[1])
                    priorityQueue.append(newPath)

        priorityQueue.sort(key=lambda x: x[1])

# aStarWalk(graph, 'Hebron','Yafa')

window = Tk()

window.geometry("1000x600")
window.configure(bg="#ffffff")
canvas = Canvas(
    window,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file=f"background.png")
background = canvas.create_image(
    450, 300,
    image=background_img)

entry0_img = PhotoImage(file=f"img_textBox0.png")
entry0_bg = canvas.create_image(
    522, 160,
    image=entry0_img)

entry0 = Entry(
    bd=0,
    bg="#c4c4c4",
    highlightthickness=0)

entry0.place(
    x=455, y=145,
    width=134.0,
    height=33)

entry1_img = PhotoImage(file=f"img_textBox0.png")
entry1_bg = canvas.create_image(
    522, 260,
    image=entry1_img)

entry1 = Entry(
    bd=0,
    bg="#c4c4c4",
    highlightthickness=0)

entry1.place(
    x=455, y=243,
    width=134.0,
    height=33)

entry3_img = PhotoImage(file=f"img_textBox0.png")
entry3_bg = canvas.create_image(
    770, 165,
    image=entry3_img)

entry3 = Entry(
    bd=0,
    bg="#c4c4c4",
    highlightthickness=0)

entry3.place(
    x=700, y=150,
    width=134.0,
    height=33)

entry2_img = PhotoImage(file=f"img_textBox2.png")
entry2_bg = canvas.create_image(
    651, 515,
    image=entry2_img)

entry2 = Entry(
    bd=0,
    bg="#c4c4c4",
    highlightthickness=0)

entry2.place(
    x=470, y=462,
    width=363.0,
    height=104)


def fun():
    entry2.delete(0, 'end')
    if entry3.get().lower() == "bfs":
        entry2.insert(END, BFS(graph, entry0.get(), entry1.get()))
    elif entry3.get().lower() == "dfs":
        entry2.insert(END, DFS(graph, entry0.get(), entry1.get()))
    elif entry3.get().lower() == "greedy":
        entry2.insert(END, Greedy(graph, entry0.get(), entry1.get()))
    elif entry3.get().lower() == "a star 1":
        entry2.insert(END, aStarAerial(graph, entry0.get(), entry1.get()))
    elif entry3.get().lower() == "a star 2":
        entry2.insert(END, aStarWalk(graph, entry0.get(), entry1.get()))
    else:
        entry2.insert(END, "Invalid Choice!")


img0 = PhotoImage(file=f"img0.png")
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=fun,
    relief="flat")

b0.place(
    x=461, y=317,
    width=111,
    height=56)

window.resizable(False, False)
window.mainloop()