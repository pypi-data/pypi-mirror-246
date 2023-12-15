import json
import csv
import os

def jsoncreat (name):
    file_mame=name+".json"
    open(file_mame,"x")

def jsonwrite (name ,added_value):
    file_mame=name+".json"
    file=open(file_mame,"w")
    json.dump(added_value, file)

def Jsonappand (name, added_value):
    file_mame=name+".json"
    file=open(file_mame,"r+")
    data=json.load(file)
    data_added=added_value
    for cle in data_added.keys():
        data[cle]=data_added[cle]
    jsonwrite(name,data)

def jsonread (name):
    file_mame=name+".json"
    file=open(file_mame,"r")
    print(json.load(file))

def Jsondelet (name):
    file_mame=name+".json"
    os.remove(file_mame)



def Csvcreat (name):
    file_mame=name+".csv"
    open(file_mame,"x")

def Csvwrite (name ,added_value):
    file_mame=name+".csv"
    file=open(file_mame,"w")
    ecriture = csv.writer(file)
    ecriture.writerows(added_value)

def Csvappand (name,added_value):
    file_mame=name+".csv"
    file=open(file_mame,"a")
    ajouter = csv.writer(file)
    ajouter.writerows(added_value)

def Csvread (name):
    file_mame=name+".csv"
    file=open(file_mame,"r")
    lecteur = csv.reader(file)
    for line in lecteur:
        print(line)

def Csvdelet (name):
    file_mame=name+".csv"
    os.remove(file_mame)



def Txtcreat (name):
    file_mame=name+".txt"
    open(file_mame,"x")

def Txtwrite (name ,added_value):
    file_mame=name+".txt"    
    file=open(file_mame,"w")
    file.write(added_value)

def Txtappand (name,added_value):
    file_mame=name+".txt"
    file=open(file_mame,"a")
    file.write(added_value)

def Txtread (name):
    file_mame=name+".txt"
    file=open(file_mame,"r")
    print(file.read())

def Txtdelet (name):
    file_mame=name+".txt"
    os.remove(file_mame)





