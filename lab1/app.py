from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
  return {
      "message": "Привет! Это моя первая лабораторная работа в Docker.",
      "status": "success",
  }


@app.get("/health")
def health_check():
  return {"status": "healthy"}
