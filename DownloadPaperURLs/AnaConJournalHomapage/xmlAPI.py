from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import dump
from xml.etree.ElementTree import Comment
from xml.etree.ElementTree import tostring
import xml.dom.minidom as minidom
import sys
sys.path.append("../UsefulLibs")
import LoadDatInfo

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem

def print_out_xml(out_file = 'book.xml'):
    book = ElementTree()

    purchaseorder = Element('RECORDS')
    book._setroot(purchaseorder)

    purchaseorder2 = Element('RECORD')
    SubElement(purchaseorder2,  'id').text = 'aaaa'
    SubElement(purchaseorder2,  'article').text = 'bbbb'

    purchaseorder3 = Element('RECORD')
    SubElement(purchaseorder3,  'id').text = 'aaaa'
    SubElement(purchaseorder3,  'article').text = 'bbbb'
    purchaseorder.append(purchaseorder2)
    purchaseorder.append(purchaseorder3)

    dump(indent(purchaseorder))
    book.write(out_file,"utf-8")

def load_xml(in_file = 'book.xml'):
    dom = minidom.parse(in_file)
    root = dom.getElementsByTagName("RECORDS") #The function getElementsByTagName returns NodeList.
    print(root.length)

    for node in root:
        print("Root element is %s" %node.tagName)
        records = node.getElementsByTagName("RECORD")
        for record in records:
            print(record.nodeName)
            print(record.tagName)
            print len(record.getElementsByTagName("id"))
            print record.getElementsByTagName("id")[0].childNodes[0].nodeValue


def print_out_paper_info(paper_info_list,out_file = 'book.xml'):
    ele_tree = ElementTree()
    root_paper_tree = Element('PAPERS')
    ele_tree._setroot(root_paper_tree)
    for paper_info in paper_info_list:
        temp_paper_ele = Element('PAPER')
        for key, value in paper_info.items():
            if key == 'author_list': value = '_'.join(value)
            SubElement(temp_paper_ele,  key).text = value
        root_paper_tree.append(temp_paper_ele)
    dump(indent(root_paper_tree))
    ele_tree.write(out_file,"utf-8")

def load_out_paper_info_xml(paper_id_to_paper_info_dict,all_paper_info_list,in_file = 'data_base.xml'):
    dom = minidom.parse(in_file)
    paper_info_node_list = dom.getElementsByTagName("PAPER") #The function getElementsByTagName returns NodeList.
    print 'Before load data, all paper numbers: ' + str(paper_info_node_list.length)
    for paper_info_node in paper_info_node_list:
        paper_info_dict = LoadDatInfo.get_paper_info_dict()
        try:
            paper_info_dict['publish_con'] = paper_info_node.getElementsByTagName("publish_con")[0].childNodes[0].nodeValue
        except:
            print "error in paper_info_dict['publish_con']"
            continue
        try:
            paper_info_dict['title'] = paper_info_node.getElementsByTagName("title")[0].childNodes[0].nodeValue
        except:
            print "error in paper_info_dict['title']"
            continue
        try:
            paper_info_dict['download_url'] = paper_info_node.getElementsByTagName("download_url")[0].childNodes[0].nodeValue
        except:
            print paper_info_dict['title']
            print "error in paper_info_dict['download_url']"
            continue
        try:
            author_str = paper_info_node.getElementsByTagName("author_list")[0].childNodes[0].nodeValue
            while author_str[0] == ' ': author_str = author_str[1:]
            paper_info_dict['author_list'] = author_str.split('_')
        except:
            print paper_info_dict['title']
            print "error in paper_info_dict['author_list']"
            continue
        try:
            paper_info_dict['publish_year'] = paper_info_node.getElementsByTagName("publish_year")[0].childNodes[0].nodeValue
        except:
            print "error in paper_info_dict['publish_year']"
            continue
        try:
            paper_info_dict['paper_id'] = paper_info_node.getElementsByTagName("paper_id")[0].childNodes[0].nodeValue
        except:
            print "error in paper_info_dict['paper_id']"
            continue
        all_paper_info_list.append(paper_info_dict)
        paper_id_to_paper_info_dict[paper_info_dict['paper_id']] = paper_info_dict
    print 'After load data, all paper numbers: ' + str(len(all_paper_info_list)) + '.'

if __name__=="__main__":
    a = 'aaa'
    print len(a.split('_'))
    for t in a.split('_'):
        print t
