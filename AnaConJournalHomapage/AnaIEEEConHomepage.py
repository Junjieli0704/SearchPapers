
#coding=utf-8
import bs4
import LoadDatInfo
import sys
import xmlAPI

'''
    Author: Junjie Li
    Analyze IEEE conference homepage
    Input: an IEEE conference homepage
    Output: all paper info in the page
    2016/04/07
'''

def detect_href(href_file):
    href_file = href_file.replace('.','-')
    href_file_list = href_file.split('-')
    if len(href_file_list) == 3:
        temp_value = int(href_file_list[1])
        if temp_value == 2000: return False
        elif temp_value > 1000 and temp_value < 3000: return True
    return False


def get_paper_info_list_from_con_year(con_home_file,con_name_year,all_paper_info_list):
    #out_paper_info_list = []
    con_name = con_name_year.split('_')[0]
    year = con_name_year.split('_')[1]
    url_con = open(con_home_file,'r').read()
    page_content_bs = bs4.BeautifulSoup(url_con)
    p_bs_list = page_content_bs.findAll('p')
    for p_bs in p_bs_list:
        if p_bs.has_attr('class'):
            if p_bs.find('a') != None and p_bs.find('i') != None:
                author_str = p_bs.find('i').text
                author_list = author_str.split(', ')
                title_str =  p_bs.find('a').text
                href_str = ''
                for temp_str in str(p_bs).split('</a>'):
                    if temp_str.find('PDF') != -1:
                        href_str = temp_str.split('"')[1].replace('view','download')
                paper_info_dict = LoadDatInfo.get_paper_info_dict()
                paper_info_dict['publish_year'] = year
                paper_info_dict['publish_con'] = con_name
                paper_info_dict['author_list'] = author_list
                paper_info_dict['title'] = title_str
                paper_info_dict['download_url'] = href_str
                paper_info_dict['paper_id'] = '__' + str(len(all_paper_info_list) + 1) + '__'
                if title_str != 'Books':
                    all_paper_info_list.append(paper_info_dict)

if __name__ == '__main__':
    con_home_file = '../Data/Homepage/IJCAI_2015.html'
    con_name_year = 'IJCAI_2015'
    all_list = []
    get_paper_info_list_from_con_year(con_home_file,con_name_year,all_list)
    xmlAPI.print_out_paper_info(all_list,'ttt.xml')