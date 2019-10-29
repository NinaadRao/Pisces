import csv
import json


ndict={}
disc={}
cr={}
be={}
mt={}
comp={}
fte={}

csvfile=open('response.csv','r')
jsonfile=open('nfile.json','w')
fieldnames=("Timestamp","comp","addr","about","sector","SMode",
"ip","JD","DBE","DM","DMCA",
"10th","12th","bcgpa","BEP","mcgpa","MP",
"pos","loc","stat","ftb","ftctc","internship","bond",
"site","deadline","tdate","idate"
)

reader=csv.DictReader(csvfile,fieldnames)
next(reader)
for row in reader:
    ndict['Company']=row['comp']
    ndict['Postal Address']=row['addr']
    ndict["About the Company"]=row["about"]
    ndict["Company Sector"]=row["sector"]
    ndict["Mode of Selection"]=[(row["SMode"])]
    ndict["Interview Process"]=row["ip"]
    ndict["Job Description"]=row["JD"]

    disc["BE/BTech"]=[row['DBE']]
    disc["MTech"]=[row['DM']]
    disc["MCA"]=[row["DMCA"]]

    ndict['Disciplines']=disc

    cr["10th"]=row["10th"]
    cr["12th"]=row["12th"]

    be['CGPA']=row['bcgpa']
    be['Percentage']=row['BEP']

    mt['CGPA']=row['mcgpa']
    mt['Percentage']=row['MP']

    cr['BE/BTech']=be
    cr["MTech/MCA"]=mt

    ndict['Criteria']=cr
    ndict['Position']=row['pos']
    ndict['Location']=row['loc']
    ndict['Job Status']=[row['stat']]

    fte['Base Pay']=row['ftb']
    fte['Total CTC']=row['ftctc']

    comp['Full Time']=fte
    comp['Internship']=row['internship']

    ndict['Compensation']=comp

    ndict['Bond/Service agreement details']=row['bond']
    ndict['Website']=row['site']
    ndict['Registration Deadline']=row['deadline']
    ndict['Test Date']=row['tdate']
    ndict['Interview Date']=row['idate']
    #print(cr)
    #print(ndict)
    #print(disc)
    #ndict['Disciplines']

    json.dump(ndict,jsonfile, indent=4)
    jsonfile.write('\n')