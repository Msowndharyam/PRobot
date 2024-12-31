from fastapi import FastAPI, Request
import asyncio
import json
from analysis.static_analysis import analyze_code
import httpx

app =  FastAPI()

GITHUB_TOKEN = "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s"

@app.get("/")
async def read_root():
    return{"message":"initiate"}

@app.post("/webhook")
async def handle_wenhook(request:Request):
    payload = await request.json()
    action = payload.get("action")
    pull_request = payload.get("pull_request")

    if action=="opened" and pull_request:
        pr_title= pull_request.get("title")
        pr_url= pull_request.get("html_url")
        pr_files_url= pull_request.get("_links", {}).get("self",{}).get("href")

        print(f"PR Opened: {pr_title}({pr_url})")
        print(f"Files URL:{pr_files_url}")
        asyncio.create_task(process_pull_request(pr_files_url))
    return{"status":"webhook received"}    

async def process_pull_request(files_url):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(files_url, headers=headers)

    if response.status_code == 200:
        pr_files = response.json()
        for file in pr_files:
            file_name = file.get("filename")
            raw_url = file.get("raw_url")

            #fetch the file content
            print(f"Fetching {file_name}")
            async with httpx.AsyncClient() as client:
                file_response = await client.get(raw_url)
            
            if file_response.status_code == 200:
                file_content = file_response.text

                #save the file locally(for now)
                with open(f"downloaded/{file_name}", "w") as f:
                    f.write(file_content)

                #run static analysis
                analyze_code(f"downloaded/{file_name}")
            else:
                print(f"Failed to fetch {file_name}")
    else:
        print(f"Failed to fetch files from PR: {response.status_code}")