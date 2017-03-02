#coding=utf-8

# -------------------------------------------------------------------- #
# Search Dat for Top Conferences:
#   IEEE conferences: AAAI, IJCAI
#   ACM  conferences: WWW, CIKM, SIGKDD, SIGIR, WSDM
#   ACL  conferences: ACL, EMNLP, NAACL, COLING,
#   ACL  Journals:    TACL, CL
#   ICML NIPS JMLR
# 添加时间： 2016-04-06
# Revise Time: 2017-01-19
# -------------------------------------------------------------------- #

import os
import time
import urllib
import httplib
import sys
import optparse
from AnaConJournalHomapage import LoadDatInfo,xmlAPI,usefulAPI

def initial_search_info(search_word = 'opinion',conference = 'ICML_NIPS_JMLR',year = '2011_2015',out_filefold = './Out/'):
    search_dat_dict = LoadDatInfo.get_search_dat()
    search_dat_dict['search_word'] = search_word.lower()
    search_dat_dict['publish_year'] = year
    search_dat_dict['publish_con'] = conference
    search_dat_dict['out_filefold'] = out_filefold
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
    def __init__(self,search_dat_dict,con_to_org_dict,data_base_file):
        self.search_dat_dict = search_dat_dict
        self.con_to_org_dict = con_to_org_dict
        self.data_base_file = data_base_file
        self.all_paper_info_list = []
        self.paper_id_to_paper_info_dict = {}
        self.res_paper_info_list = []
        self.out_search_paper_info_file = 'search_paper.xml'

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
        if search_dat_dict['publish_year'].find('_') == -1:
            begin_year = int(search_dat_dict['publish_year'])
            end_year = int(search_dat_dict['publish_year'])
        else:
            begin_year = int(self.search_dat_dict['publish_year'].split('_')[0])
            end_year = int(self.search_dat_dict['publish_year'].split('_')[1])
        for year in range(begin_year,end_year+1): search_year_dict[str(year)] = 1
        for paper_info in self.all_paper_info_list:
            if search_year_dict.has_key(paper_info['publish_year']) == False: continue
            if search_con_dict.has_key(paper_info['publish_con']) == False: continue
            paper_title = paper_info['title'].lower()
            if self.detect_title_accord_with_search_words(paper_title,search_dat_dict['search_word']):
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


    def print_top_researchers(self,out_file):
        out_file_con_list = []
        out_file_con_list.append('Author\tPaperNumber\tPaperList')
        author_to_paper_num_dict = {}
        author_to_paper_list_dict = {}
        for paper_info in self.res_paper_info_list:
            author_list = paper_info['author_list']
            con_year = paper_info['publish_con'] + '_' + paper_info['publish_year']
            for author in author_list:
                if author_to_paper_num_dict.has_key(author):
                    author_to_paper_num_dict[author] = author_to_paper_num_dict[author] + 1
                    author_to_paper_list_dict[author].append(con_year)
                else:
                    author_to_paper_num_dict[author] = 1
                    author_to_paper_list_dict[author] = []
                    author_to_paper_list_dict[author].append(con_year)

        author_to_paper_num_pair = sorted(author_to_paper_num_dict.iteritems(), key=lambda d:d[1], reverse = True)
        for author_paper_pair in author_to_paper_num_pair:
            author = author_paper_pair[0]
            paper_num = str(author_paper_pair[1])
            con_list_str = self.get_con_list_str(author_to_paper_list_dict[author])
            out_file_con_list.append('\t'.join([author,paper_num,con_list_str]).encode('utf-8'))

        open(out_file,'w+').write('\n'.join(out_file_con_list))


    def print_out_all_search_paper_info(self):
        xmlAPI.print_out_paper_info(self.res_paper_info_list,self.out_search_paper_info_file)

    def get_paper_file_prefix(self,paper_info):
        #print paper_info['author_list']
        title_name_change = paper_info['title']
        title_name_change = title_name_change.replace('\n','').replace('\t',' ')
        temp_str_list = ['/','\\',':','*','?','"','<','>','|']
        for temp_str in temp_str_list:
            title_name_change = title_name_change.replace(temp_str,'')
        pdf_prefix = paper_info['author_list'][0] + ' - ' + paper_info['publish_con'] \
                    + '_' + paper_info['publish_year'] + ' - ' + title_name_change
        return pdf_prefix

    def get_redirect_url_for_acm_con(self,src_url):
        url_compo_list = src_url.split('&')
        temp_url_compo_list = []
        for url_compo in url_compo_list:
            if url_compo.split('=')[0] == 'CFID' or url_compo.split('=')[0] == 'CFTOKEN': continue
            temp_url_compo_list.append(url_compo)
        temp_url = '&'.join(temp_url_compo_list)
        new_url = temp_url
        temp_url = temp_url.replace('http://dl.acm.org','')
        conn = httplib.HTTPConnection("dl.acm.org")
        conn.request('GET', temp_url)
        for item in conn.getresponse().getheaders():
            if item[0] == 'location':
                new_url = item[1]
        conn.close()
        return new_url

    def get_search_res_str(self,paper_num):
        print 'There are ' + str(paper_num) + ' papers in the search condition:'
        str_list = []
        str_list.append('search_word(' + search_dat_dict['search_word'] + ')')
        str_list.append('publish_year(' + search_dat_dict['publish_year'] + ')')
        str_list.append('publish_con(' + search_dat_dict['publish_con'] + ')')
        print '\t'.join(str_list)

    def download_all_search_paper(self,out_file_fold, sleep_value = 5):
        usefulAPI.mk_dir(out_file_fold)
        self.get_search_res_str(len(self.res_paper_info_list))
        print 'Download search paper info Begin.....'
        max_prefix_len = usefulAPI.get_filefold_max_prefix_len(out_file_fold,file_suffix = '.pdf')
        for j in range(0,len(self.res_paper_info_list)):
            print str(j+1) + ' / ' + str(len(self.res_paper_info_list))
            paper_info = self.res_paper_info_list[j]
            con_year = paper_info['publish_con'] + '_' + paper_info['publish_year']
            out_file = usefulAPI.create_file_name(out_file_fold,self.get_paper_file_prefix(paper_info), '.pdf',max_prefix_len)
            if os.path.exists(out_file) == True: continue
            if self.con_to_org_dict[con_year] == 'ACM':
                url = self.get_redirect_url_for_acm_con(paper_info['download_url'])
            else:
                url = paper_info['download_url']
            self.download_one_paper(url,out_file,sleep_value)
        print 'Download search paper info Done....'

    def download_one_paper(self,url,dst_path,sleep_value = 0):
        if sleep_value != 0:
            print 'Sleep ' + str(sleep_value) + ' seconds.....'
            time.sleep(sleep_value)
            print 'Download paper begin.....'
        try:
            urllib.urlretrieve(url, dst_path,report_hook)
            #urllib.urlretrieve(url, dst_path)
            print 'Download paper end.....'
        except Exception,e:
            print e
            print 'An error is found in get_html_content_from_page()'
            print 'para: url: ' + url
            print 'para: dst_path: ' + dst_path

def detect_con_year_para(con_year):
    con_year_list = con_year.split('_')
    if len(con_year_list) == 2:
        begin_year = con_year_list[0]
        end_year = con_year_list[1]
        if int(begin_year) > int(end_year): return False
    return True


def load_search_para():
    p = optparse.OptionParser()
    p.add_option('-s','--search_word',dest='search_word',
                 help='Input the search words, our system is case-insensitive and '
                      'uses "_" (means and) or "/" (means or) to split two or more '
                      'search words (e.g. sentiment_analysis), ALLPAPER is used to '
                      'get all papers from the specical conference and year.'
                      'Default Value (sentiment)',
                 default='sentiment',type = 'string')
    p.add_option('-y','--year',dest='year',
                 help='Input the search year, from begin year(2011) to(_) end year(2015) or just one year(2012). (e.g. 2011_2013, 2012) Default Value (2015)',
                 default='2015',type = 'string')
    p.add_option('-c','--con',dest='con',
                 help='Input conferences or journals to search. The conferences contain: ACL, EMNLP, COLING, NAACL, IJCAI, AAAI, KDD, '
                      'SIGIR, WWW, WSDM, CIKM, NIPS, ICML. The journals contain: JMLR, CL, TACL. (e.g. ACL_EMNLP). '
                      '"AllCon" means all the conferences and journals. Default Value (ACL)'
                 ,default='ACL',type = 'string')
    p.add_option('-o','--outfilefold',dest='outfilefold',
                 help='Input the filefold to record pdf files (e.g. ./Sent/) Default Value(./OutFileFold/)'
                 ,default='./OutFileFold/',type = 'string')
    options, args = p.parse_args()
    if options.search_word == '':
        print "Error: seachch_word can't be empty string"
        sys.exit(0)
    elif options.year == '':
        print "Error: year can't be empty string"
        sys.exit(0)
    elif options.con == '':
        print "Error: con can't be empty string"
        sys.exit(0)
    if detect_con_year_para(options.year) == False:
        print 'Error input for parameter year, please input again......'
        sys.exit(0)
    search_dict = initial_search_info(search_word = options.search_word,
                                      year = options.year,
                                      conference = options.con,
                                      out_filefold=options.outfilefold)
    print options
    return search_dict

def set_search_dict(search_word,year,con,outfilefold):
    search_dict = initial_search_info(search_word = search_word,
                                      year = year,
                                      conference = con,
                                      out_filefold=outfilefold)
    return search_dict

if __name__ == '__main__':
    con_to_homepage_dict,con_to_org_dict = LoadDatInfo.load_con_to_homepage_org_dict()
    search_dat_dict = load_search_para()
    #search_dat_dict = set_search_dict(search_word='aspect',year='2015_2016',con = 'AllCon',
    #                                  outfilefold='./Test/')
    search_paper_for_top_con = searchPaperForTopCon(search_dat_dict,con_to_org_dict,'./Data/dat_base.xml')
    search_paper_for_top_con.load_data_base_file()
    search_paper_for_top_con.search_paper()
    search_paper_for_top_con.print_out_all_search_paper_info()
    #search_paper_for_top_con.print_top_researchers('top_researchers.txt')
    search_paper_for_top_con.download_all_search_paper(out_file_fold = search_dat_dict['out_filefold'])

