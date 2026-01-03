from google import genai
client = genai.Client(api_key="AIzaSyAGPcth99hggClOeQRrMMiOguOrkjaGRcM")

        
def chat(sysPrompt, userPrompt = ""):
    prompt = [
    {"role": "system", "content": sysPrompt},
    ]
    if userPrompt:
        prompt.append({"role": "user", "content": userPrompt})
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", #gemini-2.5-flash also works! but is slower | also can use gemini-2.5-flash-lite
        contents=str(prompt),
    )
    return response.candidates[0].content.parts[0].text

'''
- github/git process to get and save changes. Do type the commands in the terminal:

1) get any new changes to ur device. do this FIRST before coding:
gitpull

2) push your changes to github. do this after making ANY changes
git add .
git commit -m "laptop changes"
git push

'''