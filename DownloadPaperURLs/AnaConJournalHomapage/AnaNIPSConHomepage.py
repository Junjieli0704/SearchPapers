
#coding=utf-8
import bs4
import dataInfo
import xmlTest
'''
    Author: Junjie Li
    Analyze NIPS homepage
    2016/04/11
'''

def get_author_list(paper_bs):
    author_list = []
    author_bs_list = paper_bs.findAll('a')
    for author_bs in author_bs_list:
        if author_bs.has_attr('class'):
            if author_bs['class'][0] == 'author':
                author_list.append(author_bs.text)
    return author_list

def get_title_download_url(paper_bs,homepage_url = 'https://papers.nips.cc'):
    author_list = []
    title_dwnurl_bs = paper_bs.find('a')
    title = title_dwnurl_bs.text
    download_url = homepage_url + title_dwnurl_bs['href'] + '.pdf'
    return title, download_url


def get_paper_info_list_from_con_year(con_home_file,con_name_year,all_paper_info_list):
    con_name = con_name_year.split('_')[0]
    year = con_name_year.split('_')[1]
    url_con = open(con_home_file,'r').read()
    page_content_bs = bs4.BeautifulSoup(url_con)
    paper_bs_list = page_content_bs.findAll('li')
    for paper_bs in paper_bs_list:
        paper_info_dict = dataInfo.get_paper_info_dict()
        paper_info_dict['publish_year'] = year
        paper_info_dict['publish_con'] = con_name
        paper_info_dict['author_list'] = get_author_list(paper_bs)
        paper_info_dict['title'], paper_info_dict['download_url'] = get_title_download_url(paper_bs)
        paper_info_dict['paper_id'] = '__' + str(len(all_paper_info_list) + 1) + '__'
        all_paper_info_list.append(paper_info_dict)


if __name__ == '__main__':
    con_home_file = './Homepage/NIPS_2015.html'
    con_name_year = 'NIPS_2015'
    #con_to_homepage_dict['ICML_2015'] = 'http://jmlr.org/proceedings/papers/v37/'
    all_list = []
    get_paper_info_list_from_con_year(con_home_file,con_name_year,all_list)
    xmlTest.print_out_paper_info(all_list,'ttt.xml')