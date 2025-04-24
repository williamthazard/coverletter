import ollama
import requests
from bs4 import BeautifulSoup 
from pypdf import PdfReader

name = input("please enter your name: ")

respath = input("please provide a filepath to your cv or resume: ")
resfile = PdfReader(respath,'r')
numpages = len(resfile.pages)

res = ""
for x in range(numpages):
    page = resfile.pages[x]
    text = page.extract_text()
    res = res + text

descpath = input("please provide a link to the job description: ")
html_content = requests.get(descpath).text
soup = BeautifulSoup(html_content, "html.parser")
desc = soup.text

prompt = 'please write a cover letter on the basis of this resume: '
prompt = prompt + res + ' and this job description: ' + desc
prompt = prompt + ' Please make sure this is a cover letter and not a summary of either of the above documents, '
prompt = prompt + 'and please make sure to use the information in the resume within the cover letter.'
prompt = prompt + 'Do not include any extraneous or introductory text, like "Here is a sample cover letter," in your response, '
prompt = prompt + 'and do not include any blanks to be filled, bracketed words or phrases, or filler phrases like "XYZ Corporation" within '
prompt = prompt + 'the body of the cover letter. Get that information from the resume alluded to above.'
prompt = prompt + ' Sign it ' + name + ' at the end. '

response = ollama.chat(model='coverletter', messages=[
  {
    'role': 'user',
    'content':  prompt,
  },
])

letter = response['message']['content']
print(letter)
docpath = open('cover-letters/coverletter.txt','w')
docpath.writelines(letter)