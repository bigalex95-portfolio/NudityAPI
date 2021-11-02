# Import module
from nudenet import NudeClassifier

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, Response

from .utils.img_proccessing import read_imagefile, read_image_from_url
import validators


classifier = None

# initialize app as FastAPI object
app_desc = """
<h2>This app for checking nudity of images</h2>
<h2>Try this app by uploading any image to `/classify/image/` or enter url of image to `/classify/url/`</h2>
<br>
<ul>
  <li>Alibek Erkabayev</li>
  <li>alibek060395@gmail.com</li>
  <li><a href="https://lazylearning.me/">My portfolio</a></li>
</ul>
"""
app = FastAPI(
    title='NSFW checker',
    description=app_desc,
    version="0.3")


# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.on_event("startup")
async def load_model():
    global classifier
    # initialize classifier (downloads the checkpoint file automatically the first time)
    classifier = NudeClassifier()


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.post("/classify/image")
async def classify_image_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return {"ERROR", "Image must be jpg or png format!"}

    image = read_imagefile(await file.read())
    prediction = classifier.classify(image)

    # prediction[0].get("safe")
    return prediction[0]


@app.post("/classify/url/{url:path}")
async def classify_url_api(url: str):
    # print("-"*40)
    # print(url)
    # print("-"*40)
    if not validators.url(url):
        return {"ERROR", "Entered wrong url!"}

    image = read_image_from_url(url)
    prediction = classifier.classify(image)

    # prediction[0].get("safe")
    return prediction[0]

if __name__ == "__main__":
    uvicorn.run(app, debug=True)
