#coding=utf-8

import os
from AnaConJournalHomapage import LoadDatInfo,AnaACMConHomepage,AnaACLConHomepage
from AnaConJournalHomapage import AnaIEEEConHomepage,AnaJMLRConHomepage,AnaNIPSConHomepage
from AnaConJournalHomapage import xmlAPI,usefulAPI

# -------------------------------------------------------------------- #
# Download paper homepages from all top conferences:
#   IEEE conferences: AAAI, IJCAI
#   ACM  conferences: WWW, CIKM, SIGKDD, SIGIR, WSDM
#   ACL  conferences: ACL, EMNLP, NAACL, COLING,
#   ACL  Journals:    TACL, CL
# 添加时间： 2016-04-06
# Revise Time: 2017-01-19
# -------------------------------------------------------------------- #



class downloadPaperInAllCon:
    def __init__(self,con_to_homepage_dict,con_to_org_dict,
                 data_base_file = './Data/dat_base.xml',
                 bad_data_file = './Data/dat_base_bad.xml'):
        self.con_to_homepage_dict = con_to_homepage_dict
        self.con_to_org_dict = con_to_org_dict
        self.con_to_homepage_file_dict = {}
        self.all_paper_info_list = []
        self.paper_info_bad_good_list = []
        self.data_base_file = data_base_file
        self.bad_data_file = bad_data_file

    def download_all_homepage(self,homepage_filefold = './Data/Homepage/'):
        print 'DownLoad all conference homepages......'
        i = 0
        for con_name_year, url in self.con_to_homepage_dict.items():
            i = i + 1
            print str(i) + ' / ' + str(len(self.con_to_homepage_dict)) + ' --> ' + con_name_year
            download_file = homepage_filefold + con_name_year + '.html'
            if os.path.exists(download_file) == False:
                usefulAPI.download_page(url,download_file)
            self.con_to_homepage_file_dict[con_name_year] = download_file
        print 'DownLoad all conference homepages Done.'

    def analyze_conference(self,home_page_file,con_name_year):
        homepage_url = self.con_to_homepage_dict[con_name_year]
        if self.con_to_org_dict[con_name_year] == 'ACL':
            AnaACLConHomepage.get_paper_info_list_from_con_year(homepage_url,home_page_file,con_name_year,self.all_paper_info_list)
        elif self.con_to_org_dict[con_name_year] == 'ACM':
            AnaACMConHomepage.get_paper_info_list_from_con_year(home_page_file,con_name_year,self.all_paper_info_list)
        elif self.con_to_org_dict[con_name_year] == 'IEEE':
            AnaIEEEConHomepage.get_paper_info_list_from_con_year(home_page_file,con_name_year,self.all_paper_info_list)
        elif self.con_to_org_dict[con_name_year] == 'JMLR':
            AnaJMLRConHomepage.get_paper_info_list_from_con_year(homepage_url,home_page_file,con_name_year,self.all_paper_info_list)
        elif self.con_to_org_dict[con_name_year] == 'NIPS':
            AnaNIPSConHomepage.get_paper_info_list_from_con_year(home_page_file,con_name_year,self.all_paper_info_list)

    def analyze_all_conference(self):
        print 'Analyze all conference homepages......'
        i = 0
        for con_name_year, url in self.con_to_homepage_dict.items():
            i = i + 1
            print str(i) + ' / ' + str(len(self.con_to_homepage_dict)) + ' --> ' + con_name_year
            home_page_file = self.con_to_homepage_file_dict[con_name_year]
            self.analyze_conference(home_page_file,con_name_year)
        print 'Analyze all conference homepages Finished.'

    def get_bad_good_paper_info_list(self):
        for paper_info in self.all_paper_info_list:
            temp_bad_good_str = 'good'
            for key, value in paper_info.items():
                #if key == 'title' and value == 'A Whole Page Click Model to Better Interpret Search Engine Click Data':
                #    print paper_info
                #    print paper_info['download_url']
                #    print paper_info['download_url'] == ''
                if key == 'author_list':
                    if len(value) == 0:
                        temp_bad_good_str = 'lack_of_author'
                    else:
                        is_has_author = False
                        for author in value:
                            if author != '': is_has_author = True
                        if is_has_author == False:
                            temp_bad_good_str = 'lack_of_author'
                elif value == '':
                    temp_bad_good_str = 'lack_of_' + key
            self.paper_info_bad_good_list.append(temp_bad_good_str)

    def print_out_all_paper_info(self):
        print 'print_out_all_paper_info......'
        self.get_bad_good_paper_info_list()
        good_paper_info_list = []
        bad_paper_info_list = []
        for i in range(0,len(self.all_paper_info_list)):
            if self.paper_info_bad_good_list[i] == 'good':
                good_paper_info_list.append(self.all_paper_info_list[i])
            else:
                bad_paper_info_list.append(self.all_paper_info_list[i])
        xmlAPI.print_out_paper_info(good_paper_info_list,self.data_base_file)
        xmlAPI.print_out_paper_info(bad_paper_info_list,self.bad_data_file)
        print 'print_out_all_paper_info finished......'



if __name__ == '__main__':

    con_to_homepage_dict,con_to_org_dict = LoadDatInfo.load_con_to_homepage_org_dict()
    data_base_file = './Data/dat_base.xml'
    bad_data_file = './Data/dat_base_bad.xml'
    down_paper_in_AllCon = downloadPaperInAllCon(con_to_homepage_dict,
                                                 con_to_org_dict,
                                                 data_base_file=data_base_file,
                                                 bad_data_file=bad_data_file)
    down_paper_in_AllCon.download_all_homepage()
    down_paper_in_AllCon.analyze_all_conference()
    down_paper_in_AllCon.print_out_all_paper_info()




