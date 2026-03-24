import requests
import Chatbot

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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def match_genre_from_prompt(userPrompt = ""): 
    """
    Uses the chatbot to identify which official MAL genres match the user's request.

    Args:
        user_prompt (str): The user's description of what they want to watch.

    Returns:
        str: A list or description of matching genres identified by the chatbot.
    """
    sysPrompt = ""
    with open('system_prompt.txt', 'r') as fh:
        sysPrompt = fh.read()

    genreList = _fetch_mal_genres()
    if not userPrompt:
        userPrompt = input("what would you like to watch:\n")
    sysPrompt += f"\n[Genre List]\n({', '.join(genreList)})"
    return Chatbot.chat(f"{sysPrompt}\n{userPrompt}").split(", ")

genre_to_id = {
    "action": 1, "adventure": 2, "avant garde": 5, "award winning": 46,
    "boys love": 28, "comedy": 4, "drama": 8, "fantasy": 10,
    "girls love": 26, "gourmet": 47, "horror": 14, "mystery": 7,
    "romance": 22, "sci-fi": 24, "slice of life": 36, "sports": 30,
    "supernatural": 37, "suspense": 41, "ecchi": 9, "erotica": 49,
    "hentai": 12, "adult cast": 50, "anthropomorphic": 51, "cgdct": 52,
    "childcare": 53, "combat sports": 54, "crossdressing": 81,
    "delinquents": 55, "detective": 39, "educational": 56, "gag humor": 57,
    "gore": 58, "harem": 35, "high stakes game": 59, "historical": 13,
    "idols (female)": 60, "idols (male)": 61, "isekai": 62, "iyashikei": 63,
    "love polygon": 64, "magical sex shift": 65, "mahou shoujo": 66,
    "martial arts": 17, "mecha": 18, "medical": 67, "military": 38,
    "music": 19, "mythology": 6, "organized crime": 68, "otaku culture": 69,
    "parody": 20, "performing arts": 70, "pets": 71, "psychological": 40,
    "racing": 3, "reincarnation": 72, "reverse harem": 73, "love status quo": 74,
    "samurai": 21, "school": 23, "showbiz": 75, "space": 29,
    "strategy game": 11, "super power": 31, "survival": 76, "team sports": 77,
    "time travel": 78, "vampire": 32, "video game": 79, "visual arts": 80,
    "workplace": 48, "urban fantasy": 82, "villainess": 83, "josei": 43,
    "kids": 15, "seinen": 42, "shoujo": 25, "shounen": 27
}

def get_genre_ids(lis = ""):
    """
    Convert a comma-separated string of genre names into a list of their corresponding genre mal IDs by matching genre names against the `genre_to_id` dictionary (case-insensitive).

    If no input string is provided, the function attempts to retrieve genres by calling `match_genre_from_prompt()`. 

    Args:
        list (str, optional): A string containing genre names separated by 
            ", ". Defaults to an empty string.

    Returns:
        list[int]: A list of integer IDs corresponding to the found genres.
    """
    if isinstance(lis, list) and all(isinstance(i, int) for i in lis):
        return lis
    if not lis:
        lis = match_genre_from_prompt()
    if isinstance(lis, str):
        lis = lis.split(", ")
    result = [genre_to_id[entry.lower()] for entry in lis if entry.lower() in genre_to_id.keys()]
    # print(f"genres: {lis}\ngenre ids: {result}")
    return result


def _fetch_mal_genres():
    """
    Fetches anime genre names from the MyAnimeList database via the Jikan API.
    
    Returns:
        list: A list of strings representing anime genres.
    """
    response = requests.get("https://api.jikan.moe/v4/genres/anime")

    listOfData = response.json()['data']
    genres = []
    for i in range(len(listOfData)):
        data = listOfData[i]
        genres.append(data['name'])
    return genres


def stream_fetch_mal_genres(): #Generator function of above function
    """
    Fetches anime genres from the Jikan API and yields each genre name.

    Yields:
        str: The name of an anime genre (e.g., 'Action', 'Sci-Fi').
    """
    listOfData = requests.get("https://api.jikan.moe/v4/genres/anime").json()['data']
    for i in range(len(listOfData)):
        data = listOfData[i]
        yield data['name']

# dataDict = response.json()#["data"]
# aniList = dataDict["data"]


# userPrompt = input('Type here:\n')
# print(returnGenre(userPrompt))



def fetch_user_anime(username):
    """
    Fetches the full anime list for a specific MyAnimeList user via their public JSON endpoint where each entry is the anime id

    Args:
        userName (str): The MyAnimeList username to fetch data for.

    Yields:
        str: The anime id of each anime in the user's list.
    """
    ani_list_url = "https://myanimelist.net/animelist/{user}/load.json?status=2&offset={offset}"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'
    }
    offset_counter = 0
    while True:
        url = ani_list_url.format(user = username, offset = offset_counter)
        batch = requests.get(url, headers=headers).json()

        if not batch:
            break

        for item in batch:
            yield item['anime_id']
            

        offset_counter += 300

def fetch_anime(genre = ""):
    endpoint = "https://api.jikan.moe/v4/anime?page={page}&limit=25&genres={genres_list}&order_by=score&sort=desc&status=complete"
    page = 1
    while True:
        data = requests.get(endpoint.format(page = page, genres_list = ",".join(map(str, get_genre_ids(genre) if genre else genre)))).json()

        for i in range(len(data['data'])):
            yield data['data'][i]

        if data['pagination']['has_next_page']:
            page += 1
        else:
            break
        






def recommend_by_genre(username = "-Nuance"):
    # get user anime list
    while True:
        user_list_ids = [] #a list of ints representing anime id's
        for ani_id in fetch_user_anime(username):
            user_list_ids.append(ani_id)

        # get user desired genre
        genre_ids = get_genre_ids()
        genre_ids.remove("Hentai") if 'Hentai' in genre_ids or 'hentai' in genre_ids else None
        all_anime = fetch_anime(genre_ids)

        while True:
            ani_suggestion = next(all_anime)
            while ani_suggestion["mal_id"] in user_list_ids:
                ani_suggestion = next(all_anime)
            print(f"{ani_suggestion['title_english'] if ani_suggestion['title_english'] else ""}{f'/{ani_suggestion['title']}' if ani_suggestion['title'] != ani_suggestion['title_english'] else ""}")
            if input("\nget another anime?\n").lower() == "no":
                break

        if input("Get another recommendation?\n") not in ["yes", "Yes", "y"]:
            break

#when printing the title, can instead put into a chatbot, saying "recomend me this anime: "

recommend_by_genre()