from fastapi import FastAPI
from src.helper.llm_call import ensure_llm_ready
from src.router import query

app = FastAPI()
app.include_router(query.router)


@app.on_event("startup")
def warm_up_llm() -> None:
    ensure_llm_ready()

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



