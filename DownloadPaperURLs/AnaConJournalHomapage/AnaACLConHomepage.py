
#coding=utf-8
import bs4
import dataInfo
import xmlTest
'''
    Author: Junjie Li
    Analyze ACL conference and journal homepage
    Input: an ACL conference homepage
    Output: all paper info in the page
    2016/04/07
'''

def detect_href(href_file,con_name):
    href_file = href_file.replace('.','-')
    href_file_list = href_file.split('-')
    if len(href_file_list) == 3:
        temp_value = int(href_file_list[1])
        if con_name != 'CL':
            if temp_value == 2000: return False
            elif temp_value > 1000 and temp_value < 3000: return True
        else:
            return True
    return False

def get_paper_info_list_from_con_year(homepage_url,con_home_file,con_name_year,all_paper_info_list):
    #out_paper_info_list = []
    con_name = con_name_year.split('_')[0]
    year = con_name_year.split('_')[1]
    url_con = open(con_home_file,'r').read()
    page_content_bs = bs4.BeautifulSoup(url_con)
    p_bs_list = page_content_bs.findAll('p')
    for p_bs in p_bs_list:
        if p_bs.find('a') != None and  p_bs.find('b') != None and  p_bs.find('i') != None:
            paper_info_dict = dataInfo.get_paper_info_dict()
            temp_href = p_bs.find('a')['href']
            paper_info_dict['publish_year'] = year
            paper_info_dict['publish_con'] = con_name
            if detect_href(temp_href,con_name):
                paper_info_dict['download_url'] = homepage_url + temp_href
                author_str = p_bs.find('b').text
                author_list = author_str.split('; ')
                paper_info_dict['author_list'] = author_list
                title = p_bs.find('i').text
                paper_info_dict['title'] = title
                paper_info_dict['paper_id'] = '__' + str(len(all_paper_info_list) + 1) + '__'
                all_paper_info_list.append(paper_info_dict)

if __name__ == '__main__':
    con_home_file = './Homepage/NAACL_2016.html'
    con_name_year = 'NAACL_2016'
    all_list = []
    get_paper_info_list_from_con_year('',con_home_file,con_name_year,all_list)
    xmlTest.print_out_paper_info(all_list,'ttt.xml')