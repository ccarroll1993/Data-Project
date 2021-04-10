import bs4
import urllib.request
import csv
import JobDetails

soup = bs4.BeautifulSoup
uReq = urllib.request.urlopen


web_url = 'https://www.indeed.com/jobs?q=business+intelligence&l=Santa+Clara,+CA&limit=50'
# opening url connection
webConnect = uReq(web_url)
# creating url page refernce for parsing
webPage = webConnect.read()
# closing url connection
webConnect.close()

#parsing webpage
webPage_soup = soup(webPage, "html.parser")

#Creating list of job selection\
jobList = webPage_soup.findAll("div", class_="jobsearch-SerpJobCard unifiedRow row result")

#setup csv file
with open('./JobSearch.csv', 'w', newline = '') as JobSearch:
	headers = ['Title', 'Company', 'Company Rating', 'Location', 'Indeed Estimated Salary', 'Keywords', 'Min Experience', 'Max Experience', 'Days Posted', 'Remote?', 'New?', 'Urgently Hiring?', 'Job Posting']
	jobwriter = csv.DictWriter(JobSearch, fieldnames=headers)


	jobwriter.writeheader()
	for jobs in jobList:

		#Title
		job_title = jobs.h2.a['title']

		#Company
		try:
			job_company = jobs.find("span", class_='company').a.contents[0][1::]
		except:
			job_company = jobs.find("span", class_='company').contents[0][1::]

		#Company's rating
		try:
			job_rating = jobs.find("span", class_='ratingsDisplay').a['aria-label'][15::].split()[0]
		except:
			job_rating = ""

		#Location
		try:
			job_location = jobs.find("div", class_="location accessible-contrast-color-location").contents[0]
		except:
			job_location = jobs.find("span", class_="location accessible-contrast-color-location").contents[0]

		# Indeed Estimated Salary:
		try:
			job_salary = jobs.find("span", class_="salaryText").contents[0][1::]
		except:
			job_salary = ""

		# Days Posted:
		job_days = jobs.find("span", class_="date").contents[0]

		# Remote?:
		try:
			job_remote = jobs.find("span", class_="remote").contents[0]
		except:
			job_remote = ""

		# new?:
		try:
			job_new = jobs.find("span", class_="new").contents[0]
		except:
			job_new = ""

		# Urgently hiring?:
		try:
			urgHire = jobs.find("td", class_="jobCardShelfItem urgentlyHiring").contents[0]
			if urgHire:
				job_Hire = "Urgent"
		except:
			job_Hire = ""

		# Job Posting:
		job_posting = "https://www.indeed.com" + jobs.h2.a["href"]

		# Keywords:
		job_keywords = JobDetails.skills(job_posting)

		# Minimum Experience:
		try:
			job_MinExperience = JobDetails.experience(job_posting)[0]
		except:
			job_MinExperience = ""

		# Maximum Experience:
		try:
			job_MaxExperience = JobDetails.experience(job_posting)[-1]
		except:
			job_MaxExperience = ""

		# Defining Dictionary
		job_dict = {
			'Title': job_title,
			'Company': job_company,
			'Company Rating': job_rating,
			'Location': job_location,
			'Indeed Estimated Salary': job_salary,
			'Keywords': job_keywords,
			'Min Experience': job_MinExperience,
			'Max Experience': job_MaxExperience,
			'Days Posted': job_days,
			'Remote?': job_remote,
			'New?': job_new,
			'Urgently Hiring?': job_Hire,
			'Job Posting': job_posting
			}

		jobwriter.writerow(job_dict)
