# Import module
from nudenet import NudeClassifier

import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse

from utils.img_proccessing import read_imagefile


classifier = None
# initialize app as FastAPI object
app_desc = """
<h2>Try this app by uploading any image with `predict/nudity`</h2>
<br>`by Alibek Erkabayev`
<br>`alibek060395@gmail.com`
<br>`https://lazylearning.me/`
"""
app = FastAPI(title='NudeNET FastAPI deployment ready', description=app_desc)


@app.on_event("startup")
async def load_model():
    global classifier
    # initialize classifier (downloads the checkpoint file automatically the first time)
    classifier = NudeClassifier()


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.post("/classify")
async def classify_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    prediction = classifier.classify(image)
    # prediction.get("0").get("safe")
    return prediction


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
