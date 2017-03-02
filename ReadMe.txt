This project is used to search papers in top conferences or journals.

Conferences and Journals contain:
   IEEE Conferences:             AAAI, IJCAI
   ACM  Conferences:             WWW, CIKM, SIGKDD, SIGIR, WSDM
   ACL  Conferences:             ACL, EMNLP, NAACL, COLING,
   ACL  Journals:                TACL, CL
   Machine Learning Conferences: ICML NIPS
   Machine Learning Journal:     JMLR
   from 2011 to 2016 (partly)

All supported conferences and journals are in ./Data/con_org_homepage.txt

All dependent libraries:
	optparse:         parse command
	beautifulsoup:    parse html files
	xml:              parse xml files and store search result in xml files

   
Q: How to use the project?
A: Run ./SearchForTopConference.py and you can get the help information.

Q: Can you give me an example?
A: ./SearchForTopConference.py -s sentiment -y 2016 -c ACL -o ./DDD/
   After run the above command, our system first search all papers from ACL_2016 conference, find papers whose title contain the search word 'sentiment', and then download all the papers being discovered in './DDD/'.

Q: How to add new conference (for example add ACL_2017)?
A: Two steps:
	1. You should add a row in ./Data/con_org_homepage.txt, the row contains three columns: conference_year, org and homepage, each column is split by '\t'.
        -- conference_year: such as ACL_2017 
        -- org: each conference associated to a org, you can get the org for your         conference from file ./Data/con_org_homepage.txt 
        -- homepage: paper page in the specical conference, such as http://aclweb.org/anthology/N/N16/ is to NAACL_2016
	2. Run ./DownloadAllPaperInfo.py to store new conference content
	Then you can search files in the new conference.   
   
Date: 2017-02-09
Author: JunjieLi@CASIA
Contact Email: junjie.li@nlpr.ia.ac.cn

