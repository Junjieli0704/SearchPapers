
#coding=utf-8
#import bs4
import os
import time
import urllib
import httplib
import sys

from AnaConJournalHomapage import LoadDatInfo,xmlAPI,usefulAPI

# -------------------------------------------------------------------- #
# Search Dat for Top Conferences:
#   IEEE conferences: AAAI, IJCAI
#   ACM  conferences: WWW, CIKM, SIGKDD, SIGIR, WSDM
#   ACL  conferences: ACL, EMNLP, NAACL, COLING,
#   ACL  Journals:    TACL, CL
#   ICML NIPS JMLR
# 添加时间： 2017-04-06
# Revise Time: 2017-01-19
# -------------------------------------------------------------------- #


def initial_search_info(search_word = 'opinion',conference = 'ICML_NIPS_JMLR',year = '2011_2015'):
    search_dat_dict = LoadDatInfo.get_search_dat()
    search_dat_dict['search_word'] = search_word.lower()
    search_dat_dict['publish_year'] = year
    search_dat_dict['publish_con'] = conference
    if conference == 'AllCon':
        con_list = ['AAAI','IJCAI','WWW','CIKM','KDD','SIGIR','WSDM','ACL','EMNLP','NAACL'
            ,'COLING','TACL','CL','JMLR','NIPS','ICML']
        conference_str = '_'.join(con_list)
        search_dat_dict['publish_con'] = conference_str
    return search_dat_dict

def report_hook(count, block_size, total_size):
    per = 100.0 * count * block_size/ total_size
    if per > 100 :
        per = 100
    print '%.2f%%' % per


class searchPaperForTopCon:
    def __init__(self,search_dat_dict,con_to_org_dict,data_base_file,out_search_paper_info_file = 'search_paper.xml'):
        self.search_dat_dict = search_dat_dict
        self.con_to_org_dict = con_to_org_dict
        self.data_base_file = data_base_file
        self.all_paper_info_list = []
        self.paper_id_to_paper_info_dict = {}
        self.res_paper_info_list = []
        self.out_search_paper_info_file = out_search_paper_info_file

    def load_data_base_file(self):
        print 'Load Data Base Begin......'
        if os.path.exists(self.data_base_file) == False:
            print 'data_base_file is not existed......'
            return False
        xmlAPI.load_out_paper_info_xml(self.paper_id_to_paper_info_dict,
                                        self.all_paper_info_list,self.data_base_file)
        print 'Load Data Base End......'

    def detect_title_accord_with_search_words(self,title_str,search_word_str):
        # search_word_str: _ means and ,  | means or,
        # a_b means the title contains a and b,
        # a|b means the titl contains a or b
        if search_word_str == 'allpaper':
            return True
        or_word_list = search_word_str.split('/')
        for or_word in or_word_list:
            and_word_list = or_word.split('_')
            is_contain_or_word = True
            for word in and_word_list:
                if title_str.find(word) == -1:
                    is_contain_or_word = False
                    break
            if is_contain_or_word:
                return is_contain_or_word
        return False

    def search_paper(self):
        search_con_dict = {}
        search_year_dict = {}
        search_con_list = self.search_dat_dict['publish_con'].split('_')
        for con in search_con_list: search_con_dict[con] = 1
        if self.search_dat_dict['publish_year'].find('_') == -1:
            begin_year = int(self.search_dat_dict['publish_year'])
            end_year = int(self.search_dat_dict['publish_year'])
        else:
            begin_year = int(self.search_dat_dict['publish_year'].split('_')[0])
            end_year = int(self.search_dat_dict['publish_year'].split('_')[1])
        for year in range(begin_year,end_year+1): search_year_dict[str(year)] = 1
        for paper_info in self.all_paper_info_list:
            if search_year_dict.has_key(paper_info['publish_year']) == False: continue
            if search_con_dict.has_key(paper_info['publish_con']) == False: continue
            paper_title = paper_info['title'].lower()
            if self.detect_title_accord_with_search_words(paper_title,self.search_dat_dict['search_word']):
                self.res_paper_info_list.append(paper_info)

    def get_con_list_str(self,con_list):
        con_year_to_num_dict = {}
        for con_year in con_list:
            if con_year_to_num_dict.has_key(con_year):
                con_year_to_num_dict[con_year] = con_year_to_num_dict[con_year] + 1
            else:
                con_year_to_num_dict[con_year] = 1

        con_list = list(set(con_list))
        year_to_con_dict = {}
        for con_year in con_list:
            con, year = con_year.split('_')
            year = int(year)
            if year_to_con_dict.has_key(year) == False:
                year_to_con_dict[year] = []
            year_to_con_dict[year].append(con)
        year_to_con_pair = sorted(year_to_con_dict.iteritems(), key=lambda d:d[0], reverse = True)
        temp_list = []
        for year_to_con in year_to_con_pair:
            year = str(year_to_con[0])
            con_list = year_to_con[1]
            for con in con_list:
                con_year = con + '_' + year
                temp_str = con_year + '_' + str(con_year_to_num_dict[con_year])
                temp_list.append(temp_str)
        return '/'.join(temp_list)

    def print_out_all_search_paper_info(self):
        xmlAPI.print_out_paper_info(self.res_paper_info_list,self.out_search_paper_info_file)


def detect_con_year_para(con_year):
    con_year_list = con_year.split('_')
    if len(con_year_list) == 2:
        begin_year = con_year_list[0]
        end_year = con_year_list[1]
        if int(begin_year) > int(end_year): return False
    return True


def set_search_dict(search_word,year,con):
    search_dict = initial_search_info(search_word = search_word,
                                      year = year,
                                      conference = con)
    return search_dict


def search_papers(search_word='sentiment',year='2016',con = 'ACL',out_search_file = 'search_paper.xml'):
    con_to_homepage_dict,con_to_org_dict = LoadDatInfo.load_con_to_homepage_org_dict()
    search_dat_dict = set_search_dict(search_word=search_word, year=year, con=con)

    data_base_file = './Data/dat_base.xml'
    search_paper_for_top_con = searchPaperForTopCon(search_dat_dict,con_to_org_dict,
                                                    data_base_file = data_base_file,
                                                    out_search_paper_info_file = out_search_file)
    search_paper_for_top_con.load_data_base_file()
    search_paper_for_top_con.search_paper()
    search_paper_for_top_con.print_out_all_search_paper_info()


if __name__ == '__main__':
    search_word = 'sentiment'
    year = '2016'
    con = 'ACL'
    out_search_file = 'search_paper.xml'
    search_papers(search_word,year,con,out_search_file)




