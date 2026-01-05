import requests
import Chatbot

# pageNum = 2
# endpoint = f"https://api.jikan.moe/v4/anime?genres=1&status=airing&order_by=score&sort=desc&page{pageNum}"
# response = requests.get(endpoint)

def getFullData(endpointStr):
    '''
    pass the endpoint as a normal string but has {pageNum}
    '''
    pagination = requests.get(f"{endpointStr}".format(pageNum = 1)).json()['pagination']
    totalPages = pagination['last_visible_page']
    
    allData = []
    for i in range(1, totalPages+1):
        tempEndpoint = f"{endpointStr}".format(pageNum = i)
        dataInPage = requests.get(tempEndpoint).json()['data']
        allData += dataInPage
    
    return allData
    
def testRun():
    ep = "https://api.jikan.moe/v4/anime?genres=1&status=airing&order_by=score&sort=desc&page{pageNum}"
    r = requests.get(f"{ep}".format(pageNum = 1)).json()['pagination']['items']['total']

    list = getFullData(ep)

    for i in range(len(list)//2):
        print(f'[{i}] {list[i]}\n')
    
def returnGenre(userPrompt):
    sysPrompt = '''
You are a genre classification assistant.
Analyze the user's message describing what they want to watch.

Your task is to infer which genres from the predefined list best match
the vibes, themes, tone, narrative elements, and implied intent of the user's message.
The user does NOT need to explicitly name a genre, and may not consciously know
what genre they are seeking.

Rules:
- Infer genres based on mood, setting, character dynamics, themes, pacing,
emotional tone, and narrative cues.
- Return ALL genres that are clearly and intentionally implied, even if the user
does not explicitly state or realize them.
- Only include a genre if a reasonable human reader would strongly associate
the user's request with that genre.
- Do NOT include weak, incidental, background, or speculative matches.
- Use only genres from the provided list.
- If no genres can be confidently inferred, return exactly: None
- When multiple genres apply, order them from most dominant to least dominant.
- Output only the genre names, separated by commas.
- Capitalization, spelling, and formatting must exactly match the list.
- Do not include explanations, commentary, or any additional text.
    '''
    genreList = getMalGenres()
    sysPrompt += f"\n[Genre List]\n({genreList})"
    return Chatbot.chat(sysPrompt, userPrompt)

def getMalGenres():
    genres = []
    listOfData = requests.get("https://api.jikan.moe/v4/genres/anime").json()['data']
    for i in range(len(listOfData)):
        data = listOfData[i]
        genres.append(data['name'])
    return genres
# print(f"Return Code: {response.status_code}")

# dataDict = response.json()#["data"]
# aniList = dataDict["data"]


userPrompt = input('Type here:\n')
print(returnGenre(userPrompt))




# print(len(aniList))
