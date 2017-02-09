This project is used to search papers in top conferences or journals.

Conferences and Journals contain:
   IEEE Conferences:            AAAI, IJCAI
   ACM  Conferences:            WWW, CIKM, SIGKDD, SIGIR, WSDM
   ACL  Conferences:            ACL, EMNLP, NAACL, COLING,
   ACL  Journals:               TACL, CL
   Machine Learning Conference: ICML NIPS JMLR
   from 2011 to 2016 (partly)
all supported conferences and journals are in ./Data/con_org_homepage.txt

All dependent libraries:
	optparse:         parse command
	beautifulsoup:    parse html files
	xml:              parse xml files and store search result in xml files

   
Q: How to use the project?
A: Run ./SearchForTopConference.py and you can get the help information.

Q: Can you give me an example?
A: ./SearchForTopConference.py -s sentiment -y 2016 -c ACL -o ./DDD/
   After run the above command, our system first search all papers from ACL_2016 conference, find papers whose title contain the search word 'sentiment', and then download all the papers being discovered in './DDD/'.
   
Date: 2017-02-09
Author: JunjieLi@CASIA