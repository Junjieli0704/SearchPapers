#coding=utf-8

# -------------------------------------------------------------------- #
# 描述： 导入会议主页和会议类型数据文件
# 添加时间： 2017-04-06
# Revise Time: 2017-01-19
# -------------------------------------------------------------------- #

def get_paper_info_dict():
    paper_info_dict = {}
    paper_info_dict['author_list'] = []
    paper_info_dict['publish_year'] = ''
    paper_info_dict['publish_con'] = ''
    paper_info_dict['download_url'] = ''
    paper_info_dict['title'] = ''
    paper_info_dict['paper_id'] = ''
    return paper_info_dict

def get_search_dat():
    search_info_dict = {}
    search_info_dict['search_word'] = ''
    search_info_dict['publish_year'] = ''
    search_info_dict['publish_con'] = ''
    search_info_dict['out_filefold'] = ''
    return search_info_dict

class searchData:
    def __init__(self):
        self.search_word = ''
        self.year = ''
        self.con_name = ''

def load_con_to_homepage_org_dict(con_to_homepage_org_file = './Data/con_org_homepage.txt'):
    con_to_homepage_dict = {}
    con_to_org_dict = {}
    line_con_list = open(con_to_homepage_org_file,'r').readlines()
    for line_con in line_con_list:
        line_con = line_con.strip()
        word_con_list = line_con.split('\t')
        if len(word_con_list) != 3: continue
        if word_con_list[0] == 'Conference': continue
        con_to_homepage_dict[word_con_list[0]] = word_con_list[2]
        con_to_org_dict[word_con_list[0]] = word_con_list[1]
    return con_to_homepage_dict,con_to_org_dict

