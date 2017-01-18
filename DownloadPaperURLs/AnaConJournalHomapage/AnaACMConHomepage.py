
#coding=utf-8
import bs4
import dataInfo
import httplib

'''
    Author: Junjie Li
    Analyze ACM conference homepage
    Input: an ACM conference homepage
    Output: all paper info in the page
    2016/04/06
'''

def get_begin_end_list(tr_bs_list):
    paper_begin_bs_list = []
    paper_end_bs_list = []
    for i in range(0,len(tr_bs_list)):
        td_bs_list = tr_bs_list[i].findAll('td')
        for td_bs in td_bs_list:
            if td_bs.has_attr('colspan'):
                if td_bs['colspan'] == '1':
                    paper_begin_bs_list.append(i)
            if len(paper_begin_bs_list) > len(paper_end_bs_list):
                a_bs = tr_bs_list[i].find('a')
                if a_bs != None:
                    if a_bs.has_attr('name'):
                        if a_bs['name'] == 'FullTextPDF':
                            paper_end_bs_list.append(i)
    return paper_begin_bs_list,paper_end_bs_list

def get_paper_info(begin_place,tr_bs_list):
    temp_paper_info_dict = dataInfo.get_paper_info_dict()

    for con_num in range(0,5):
        tr_bs = tr_bs_list[con_num + begin_place]
        if con_num == 0: # Deal with paper title and paper homepage
            a_bs = tr_bs.find('a')
            if a_bs != None:
                if a_bs.has_attr('href'):
                    temp_paper_info_dict['title'] = a_bs.text

        elif con_num == 1: # Deal with paper's author list
            a_bs_list = tr_bs.findAll('a')
            for a_bs in a_bs_list:
                temp_paper_info_dict['author_list'].append(a_bs.text)

        else:              # Deal with paper's download url
            a_bs = tr_bs.find('a')
            if a_bs != None:
                if a_bs.has_attr('name'):
                    if a_bs['name'] == 'FullTextPDF':
                        temp_paper_info_dict['download_url'] = 'http://dl.acm.org/' + a_bs['href'].replace('&amp;','&')
    return temp_paper_info_dict

def get_download_redict_url(src_url):
    new_url = src_url.replace('http://dl.acm.org/','')
    conn = httplib.HTTPConnection("dl.acm.org")
    conn.request('GET', src_url)
    is_change = False
    #print conn.getresponse().getheaders()
    for item in conn.getresponse().getheaders():
        if item[0]=='location':
            new_url = item[1]
            is_change = True
    conn.close()
    if is_change:
        return new_url
    else:
        return src_url


def get_paper_info_list_from_con_year(con_home_file,con_name_year,all_paper_info_list):
    #out_paper_info_list = []
    con_name = con_name_year.split('_')[0]
    year = con_name_year.split('_')[1]
    url_con = open(con_home_file,'r').read()
    page_content_bs = bs4.BeautifulSoup(url_con)
    tr_bs_list = page_content_bs.findAll('tr')
    paper_begin_bs_list, paper_end_bs_list = get_begin_end_list(tr_bs_list)
    if len(paper_begin_bs_list) == len(paper_end_bs_list) and len(paper_begin_bs_list) != 0:
        for i in range(0,len(paper_begin_bs_list)):
            begin_place = paper_begin_bs_list[i]
            end_place = paper_end_bs_list[i]
            if end_place - begin_place == 4:
                temp_paper_info_dict = get_paper_info(begin_place,tr_bs_list)
                temp_paper_info_dict['publish_con'] = con_name
                temp_paper_info_dict['publish_year'] = year
                temp_paper_info_dict['paper_id'] = '__' + str(len(all_paper_info_list) + 1) + '__'
                #temp_paper_info_dict['download_url'] = get_download_redict_url(temp_paper_info_dict['download_url'])
                all_paper_info_list.append(temp_paper_info_dict)
