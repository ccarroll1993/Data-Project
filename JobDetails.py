import bs4
import urllib.request
import re

soup = bs4.BeautifulSoup
uReq = urllib.request.urlopen

f = open("linkedin_skill.txt", "r")
linkedin_skill = f.read().lower().splitlines()
f.close()


def tag_removal(text):
	while(">" in text):
		text = text.replace(text[text.find("<"):text.find(">")+1], " ")

	for x in text:
		if(x.endswith(",") or x.endswith(".") or x.endswith(":") or x.endswith("!")):
			text = text.replace(x, "")

	return text


def experience(web_url):
	# opening url connection
	webConnect = uReq(web_url)
	# creating url page refernce for parsing
	webPage = webConnect.read()
	# closing url connection
	webConnect.close()

	# parsing webpage
	job1 = soup(webPage, "html.parser")

	# capturing job description
	job_skill = str(job1.find("div", class_="jobsearch-JobComponent-description icl-u-xs-mt--md"))

	job_skill = tag_removal(job_skill)

	exp = []
	experience_list = [" 0"," 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", " 10", " 11", " 12", " 13", " 14", " 15"]
	
	for match in re.finditer(" year", job_skill):
		for xp in experience_list:
			if(xp in job_skill[match.start()-10:match.end()+10:]):
				exp.append(xp)
				exp.sort()
	return exp


def skills(web_url):
	# opening url connection
	webConnect = uReq(web_url)
	# creating url page refernce for parsing
	webPage = webConnect.read()
	# closing url connection
	webConnect.close()

	# parsing webpage
	job1 = soup(webPage, "html.parser")

	# capturing job description
	job_skill = str(job1.find("div", class_="jobsearch-JobComponent-description icl-u-xs-mt--md"))
	

	job_skill = tag_removal(job_skill)

	skill_list = []

	for skill in linkedin_skill:
		if(skill in job_skill.lower()):
			skill_list.append(skill.upper())
	return skill_list



"""TESTING

myURL = 'https://www.indeed.com/viewjob?cmp=Central-Freight-Management&t=Business+Intelligence+Analyst&jk=eb879ad783703ee1&sjdu=QwrRXKrqZ3CNX5W-O9jEvYFcACbv-DthnUj_IRiMl_gPCfrvA2_A0Xmvupg8JlPB1DUHLD4qLciSFLJReZYf4vYTmxiTWJ283iTaapsIEeM&tk=1evveqrahu4qc801&adid=363780960&ad=-6NYlbfkN0BenEI0mhvOW30YqivFOKkPaF_YEjVM0ICCxB7OP_L76lMBRAF7Ea_sJAs42umGwOzEQFFj-CmgWPJjL_jdQS6way4-3be604FbZqYjXzgW6IFRd-5aGrpRjIFy-cI9Wt2N27TAuOpDtLeU941Vkf1nPf9XYTjnivatfpWAceaVPCQE6HnKc1rB0jkEiTbj5Mlyp0SQdRdoj9u_fI7c5FXEN23cDUVix0u-MLpMwVTbrBQ9FqW4QB2H1j0td2XwvO4HtYTTj2ln-5vZLGJCcITQkLi-csuQIMvT-hScMNAUU-H3ftf5J8clu4ajhK0xeDG6kblgiwKzwHM-0-cD508y&pub=4a1b367933fd867b19b072952f68dceb&vjs=3'

# skills(myURL)
# print(experience(myURL)[0][1::])
# print(experience(myURL))

TESTING"""