import requests

#User Details
mail = input("Enter your bits mail address: ")
password = input("Enter your impartus password: ")
#Getting bearer token
url_token = "http://a.impartus.com/api/auth/signin"
payload = {'username' : f"{mail}", 'password' : f"{password}" }
headers_token = {
'Accept' : 'application/json'
}
post = requests.request("POST", url_token, headers=headers_token, data=payload)
post_token = post.json()
token = post_token['token'] #bearer/auth token

#Selecting Subject
url_subjects = "http://a.impartus.com/api/subjects" #api for list of subjects
url_name = "https://a.impartus.com/api/user/profile" #url for name of user
headers = {
'Accept' : 'application/json',
'Authorization' : f'Bearer {token}'
}
#Scraping name of user
req_name = requests.request("GET", url_name, headers=headers, data=payload)
request_name = req_name.json()
print("Hello " + request_name['originalname'] + ",")

#Scraping list of subjects enrolled
req = requests.request("GET", url_subjects, headers=headers, data=payload)
request = req.json()
i = 1
subject_id = []
subject_name = []
for item in request:
    print(f" [{i}]" + item['subjectName'])
    i = i + 1
    subject_id.append(item['subjectId'])
    subject_name.append(item['subjectName'])
subject_number = int(input("Enter the number of the subject: "))

#Total lectures count
url_lecture = f"http://a.impartus.com/api/subjects/{subject_id[subject_number-1]}/lectures/1249"
req_lecture = requests.request("GET", url_lecture, headers=headers, data=payload)
request_lecture = req_lecture.json()
lecture_count = int(request_lecture[0]['seqNo'])
print(f'Lectures detected: {lecture_count}')

#scraping video ids for selected subjects
video_id = []
for id in request_lecture:
    video_id.append(id['videoId'])
video_id.reverse()

#Range of lectures to be scraped
def lecture_range():
    while True:
        try:
            x,y = map(int, input("Enter range of lecture pdfs to download(both inclusive) [ex: 5-11]: ").split("-"))
            return x,y
        except ValueError:
            print("Separate lecture using '-' [ex: 10-23]")
            lecture_range()

x, y = lecture_range()

#scraping pdfs
n = x
for n in range(x,y+1):
    url_pdf = f'http://a.impartus.com/api/videos/{video_id[n-1]}/auto-generated-pdf'
    response = requests.request("GET", url_pdf, headers=headers)
    with open(f"{subject_name[subject_number-1]} Lecture {n}.pdf", "wb") as f:
        f.write(response.content)
        print(f"Lecture {n} downloaded")
        n = n + 1











