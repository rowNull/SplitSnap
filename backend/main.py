from fastapi import FastAPI

# creating the app obj so that every route have one place to attach
app =  FastAPI()

# adding a health check route to confirm that the server is running
# before adding any features
@app.get("/health")
def health():
    return { "status": "ok" }