
#coding=utf-8
import bs4
import LoadDatInfo
import sys
import xmlAPI
'''
    Author: Junjie Li
    Analyze ICML and JMLR homepage
    2016/04/11
'''

def get_author_list(author_bs):
    return author_bs.text.replace('\r','').replace('\n','').replace('\t','').split(',')

def get_download_url(link_bs,homepage_url):
    href_bs_list = link_bs.findAll('a')
    for href_bs in href_bs_list:
        if href_bs.text == 'pdf':
            if href_bs.has_attr('href'):
                #print homepage_url + href_bs['href']
                return homepage_url + href_bs['href']
    return 'error'


def get_paper_info_list_from_con_year(homepage_url,con_home_file,con_name_year,all_paper_info_list):
    con_name = con_name_year.split('_')[0]
    year = con_name_year.split('_')[1]
    url_con = open(con_home_file,'r').read()
    page_content_bs = bs4.BeautifulSoup(url_con)
    paper_bs_list = page_content_bs.findAll('div',{'class':'paper'})
    for paper_bs in paper_bs_list:
        title_bs = paper_bs.find('p',{'class':'title'})
        authors_bs = paper_bs.find('span',{'class':'authors'})
        link_bs = paper_bs.find('p',{'class':'links'})
        if title_bs != None and authors_bs != None and link_bs != None:
            paper_info_dict = LoadDatInfo.get_paper_info_dict()
            paper_info_dict['publish_year'] = year
            paper_info_dict['publish_con'] = con_name
            paper_info_dict['author_list'] = get_author_list(authors_bs)
            paper_info_dict['title'] = title_bs.text
            paper_info_dict['download_url'] = get_download_url(link_bs,homepage_url)
            if paper_info_dict['download_url'] == 'error': continue
            paper_info_dict['paper_id'] = '__' + str(len(all_paper_info_list) + 1) + '__'
            all_paper_info_list.append(paper_info_dict)

if __name__ == '__main__':
    con_home_file = '../Data/Homepage/ICML_2015.html'
    con_name_year = 'ICML_2015'
    #con_to_homepage_dict['ICML_2015'] = 'http://jmlr.org/proceedings/papers/v37/'
    all_list = []
    get_paper_info_list_from_con_year('http://jmlr.org/proceedings/papers/v37/',con_home_file,con_name_year,all_list)
    xmlAPI.print_out_paper_info(all_list,'ttt.xml')