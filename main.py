from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from github import Github

app = FastAPI()

# CORS 配置
origins = [
    "http://localhost:3000",  # 如果你的前端運行在這個端口
    "http://127.0.0.1:3000",  # 如果使用不同的本機地址
    "http://127.0.0.1:8000",  # 如果需要允許自己測試
    # 添加其他允許的前端來源（如你的正式域名）
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 允許的來源
    allow_credentials=True,     # 是否允許發送憑據（如 Cookies）
    allow_methods=["*"],        # 允許的 HTTP 方法（如 GET、POST）
    allow_headers=["*"],        # 允許的標頭
)

# GitHub 配置
GITHUB_TOKEN = "****"
REPO_NAME = "eddieyen8453/thebinder"  # 替換成你的 GitHub 儲存庫
FILE_PATH = "thebinder/thebe.ipynb"  # 你要更新的 Notebook 路徑

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

class CodeRequest(BaseModel):
    code: str

@app.post("/submit_code")
async def submit_code(request: CodeRequest):
    try:
        file = repo.get_contents(FILE_PATH)
        updated_code = file.decoded_content.decode('utf-8').replace("## User Code Here ##", request.code)
        repo.update_file(file.path, "Update user code", updated_code, file.sha)
        return {"message": "Code submitted successfully! You can now run it on Binder."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
