from dataclasses import replace
from os import remove
import string
from bs4 import BeautifulSoup
from lxml import etree

def create_networks(xml_file, nodes_sheet, edges_sheet):
    # Reading the data inside the xml file to a variable under the name data
    with open(xml_file, "r", encoding="utf-8") as tei:
        data = BeautifulSoup(tei,  features='lxml')

    #CLASS PERSON 
    #creation of a list with all the tags 'persname' of the original tei file
    pers_list=[]
    for paragraph in data.find_all('p'):
        pers = paragraph.find_all('persname')
        for x in pers:
            pers_list.append(x)

    #list with all the values of the attribute 'ref' of the tags 'persname'
    ref_pers_list = []
    for x in pers_list:
        ref_pers_list.append(x.get("ref"))

    #dictionary with as keys the 'ref' of the persname tags and as values the contents of the persname tags
    pers_dict = dict()
    for person in data.find_all('person'):
        pers_ref_from_id = '#'+person.get('xml:id')
        pers_label = person.persname.text
        pers_dict[pers_ref_from_id]=pers_label

    #list with just the contents of the persname tags
    pers_label_list=[]
    for ref in ref_pers_list:
        if ref in pers_dict:
            pers_label_list.append(pers_dict[ref])

    #list of tuples with the values ('ref', 'label', 'type') of each person
    tuples_nodes_pers=[]
    for item in pers_list:
        tuples_nodes_pers.append((item.get('ref'), pers_dict[(item.get('ref'))], "person"))

    #CLASS PLACE
    place_list=[]
    for paragraph in data.find_all('p'):
        place = paragraph.find_all('placename')
        for x in place:
            place_list.append(x)

    ref_place_list = []
    for x in place_list:
        ref_place_list.append(x.get("ref"))

    place_dict = dict()
    for place in data.find_all('place'):
        place_ref_from_id = '#'+place.get('xml:id')
        place_label = place.placename.text
        place_dict[place_ref_from_id]=place_label

    place_label_list=[]
    for ref in ref_place_list:
        if ref in place_dict:
            place_label_list.append(place_dict[ref])

    tuples_nodes_place=[]
    for item in place_list:
        tuples_nodes_place.append((item.get('ref'), place_dict[(item.get('ref'))], "place"))

    #CLASS PROPERTY

    property_list=[]
    for paragraph in data.find_all('p'):
        property = paragraph.find_all('objectname')
        for x in property:
            property_list.append(x)

    ref_prop_list = []
    for x in property_list:
        ref_prop_list.append(x.get("ref"))

    prop_dict = dict()
    for prop in data.find_all('object'):
        prop_ref_from_id = '#'+prop.get('xml:id')
        prop_label = prop.objectname.text
        prop_dict[prop_ref_from_id]=prop_label

    prop_label_list=[]
    for ref in ref_prop_list:
        if ref in prop_dict:
            prop_label_list.append(prop_dict[ref])

    tuples_nodes_prop=[]
    for item in property_list:
        tuples_nodes_prop.append((item.get('ref'), prop_dict[(item.get('ref'))], "property"))



    #CSV - NODES_SHEET
    import csv
    with open(nodes_sheet, 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Id", "Label", "Type"])
        for item_1 in tuples_nodes_pers:
            writer.writerow(item_1)
        for item_2 in tuples_nodes_place:
            writer.writerow(item_2)
        for item_3 in tuples_nodes_prop:
            writer.writerow(item_3)

    #creation of a list with all the tags 'persname', 'placename' and 'objectname' of the original tei file
    #that appear in the same paragraph
    p_list=[]
    for p in data.find_all('p'):
        persons = p.find_all('persname')
        places = p.find_all('placename')
        objects = p.find_all('objectname')
        if persons or places or objects:
            p_list.append([persons + places + objects])
    

    #using list comprehension
    #Removing empty lists from p_list, which is a list of lists
    N = []
    p_list = [[ele for ele in sub if ele != N] for sub in p_list]
    
    #replacement of the tags with their corresponding ref values
    for x in p_list:
        for y in x:
            i = 0
            while i < len(y):
                y[i] = y[i].get("ref")
                i += 1
    
    #creation of a list with tuples containing the ref values of all the nodes that appear in the same paragraph
    tuples_edges=[]
    for x in p_list:
        for y in x:
            if len(y) > 0:
                tuples_edges.append(tuple(y))        
    
    #Create a list of tuples associating two by two the items of each tuple in tuples_edges together
    tpl_lst1 = list()
    for paragraph in tuples_edges:
        for i in range(len(paragraph)):
            tpl1 = tuple((paragraph[0], paragraph[i]))
            tpl_lst1.append(tpl1)


    #CSV - EDGES_SHEET
    import csv
    with open(edges_sheet, 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Target"])
        for item in tpl_lst1:
           writer.writerow(item)

#create_networks("Ignazio_Paolo.xml", "nodes_sheet.csv", "edges_sheet.csv")
    
#create_networks("Vincenzo.xml", "vincenzo_nodes.csv", "vincenzo_edges.csv")
    

