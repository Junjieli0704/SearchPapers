import web
        
urls =(
   '/searchpapers','SearchPapers'
)

class SearchPapers:
    def GET(self):
        i = web.input(con = 'acl',year = '2015',key = 'sentiment', outfile = 'out.txt')
        web.header("Content-Type","text/html; charset=utf-8")
        file_name = i.outfile
        temp_str = 'attachment;filename=' + file_name
        web.header("Content-Disposition",temp_str)
        line_con_list = []
        line_con_list.append(i.con)
        line_con_list.append(i.year)
        line_con_list.append(i.key)
        line_con_list.append(i.outfile)
        return_str = '\r\n'.join(line_con_list)
        return return_str


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()