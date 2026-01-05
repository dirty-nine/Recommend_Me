
# GPT-4 Free API Request
import requests

def chat(prompt):
    try:
        url = "https://xyris.vercel.app/api/llm-models/openai/gpt-4/"
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(
            url, 
            json={"query": prompt}, 
            headers=headers
        )
        response.raise_for_status()
        
        return response.json().get("content", "")
    except requests.RequestException as e:
        print(f"API Request Error: {e}")
        return ""
      
def dialogue(SYS_PROMPT):
    chats = [{'role':'system', 'content':SYS_PROMPT}]
    while True:
        uP = input("Type Here:\n")
        sP = f"[Chat History]\n{str(chats)}\n[User Prompt]\n{uP}"
        response = chat(sP)
        chats.append({'role':'user', 'content':uP})
        chats.append({'role':'system', 'content':response})
        print(response)
    
if __name__ == '__main__':
    """
    dialogue with chatbot engaged when file run directly
    """
    
    SYS_PROMPT = "you are a chatbot"
    
    chats = [{'role':'system', 'content':SYS_PROMPT}]
    while True:
        uP = input("Type Here:\n")
        sP = f"[Chat History]\n{str(chats)}\n[User Prompt]\n{uP}"
        response = chat(sP)
        chats.append({'role':'user', 'content':uP})
        chats.append({'role':'system', 'content':response})
        print(response)
    
    
    

'''
[ ] github/git process to get and save changes. Do type the commands in the terminal:

step 0) get the repo onto your decice
- go to the git tab on vscode
- click clone repository on vscode
- file explore will open. select the destination folder for your device where you want the repository to go
- select ok in file explorer
- vuwala

step 1) get any new changes to ur device. do this FIRST before coding:
gitpull

step 2) push your changes to github. do this after making ANY changes
git add . | or | git add fileName.txt
git commit -m "laptop changes"
git push
'''