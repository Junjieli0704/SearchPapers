__author__ = 'Jun'
import urllib2
import os

def get_html_content_from_page(url,time_sleep = 0):
    try:
        req = urllib2.Request(url)
        browser='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
        req.add_header('User-Agent',browser)
        response = urllib2.urlopen(req)
        html_content=response.read()
        if time_sleep != 0:
            time.sleep(time_sleep);
        return html_content;
    except Exception,e:
        print e
        print  'An error is found in get_html_content_from_page()' + 'para: url: ' + url

def download_page(url,file):
    url_content = get_html_content_from_page(url);
    open(file,"w+").write(url_content)

def mk_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = os.path.exists(path)
    if not is_exists:
        print path + ' create successfully!'
        os.makedirs(path)
        return True
    else:
        print path + ' is already be there!'
        return False

# Get all file name in the directory
# input:
#    dir: the directory
#    is_contain_dir: determine whether the fileName has the directory (False is default value);
# output: fileNameList
def get_dir_files(dir,is_contain_dir = False):
    file_list = []
    if os.path.exists(dir):
        dir_file_list = os.listdir(dir);
        for dir_file in dir_file_list:
            if is_contain_dir:    file_list.append(dir + dir_file);
            else:     file_list.append(dir_file);
    return file_list;

def get_filefold_max_prefix_len(file_fold,file_suffix = '.pdf'):
    mk_dir(file_fold)
    temp_str = 'a' * 300
    is_create_ok = False
    temp_file_name = file_fold + temp_str + file_suffix
    while is_create_ok == False:
        try:
            with open(temp_file_name, "w+") as f:
                f.close()
                os.remove(temp_file_name)
                is_create_ok = True
        except IOError:
            #temp_file_name = "".join([temp_file_name[:-4],".pdf"])
            temp_str = temp_str[:-1]
            temp_file_name = file_fold + temp_str + file_suffix
    #if len(temp_str) >= 40: return len(temp_str) - 10
    return len(temp_str)



def create_file_name(file_fold,file_prefix,file_suffix = '.pdf',max_prefix_length = 30, is_add_number = '0'):
    #print 'max_prefix_length:' + str(max_prefix_length)
    #print "file_prefix before: "
    #print file_prefix.encode('utf-8')
    if len(file_prefix) >= max_prefix_length:
        file_prefix = file_prefix[0:max_prefix_length-10]
    if is_add_number != '0':
        file_prefix = file_prefix + '_' + is_add_number
    temp_file_name = file_fold + file_prefix + file_suffix
    #try:
    #    print file_prefix
    #except:
    #    print 'ERROR'
    #print "file_prefix after: "
    #print file_prefix.encode('utf-8')
    temp_file_name = temp_file_name
    #print temp_file_name
    return temp_file_name
    '''
    print temp_file_name
    is_create_ok = False
    while is_create_ok == False:
        try:
            with open(temp_file_name, "w+") as f:
                f.close()
                os.remove(temp_file_name)
                is_create_ok = True
        except IOError:
            temp_file_name = "".join([temp_file_name[:-8],".pdf"])
    return temp_file_name
    '''


if __name__ == '__main__':
    download_page('http://www.baidu.com','a.html')

    '''
    print os.getcwd()
    file_list = get_dir_files('./OutFileFold/',False)
    for file in file_list:
        #print os.getcwd() + '/OutFileFold' + file
        temp_file = os.getcwd() + '/OutFileFold' + file
        print temp_file
        print len(temp_file)
        #print file
    '''