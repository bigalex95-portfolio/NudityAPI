# Import module
from nudenet import NudeClassifier

import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse

from utils import read_imagefile


classifier = None
# initialize app as FastAPI object
app_desc = """
<h2>This app for checking nudity of images</h2>
<h2>Try this app by uploading any image to `/classify/image` or enter url of image to `/classify/url`</h2>
<br>
<ul>
  <li>Alibek Erkabayev</li>
  <li>alibek060395@gmail.com</li>
  <li><a href="https://lazylearning.me/">My portfolio</a></li>
</ul>
"""
app = FastAPI(title='NSFW checker', description=app_desc)


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
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    prediction = classifier.classify(image)
    # prediction.get("0").get("safe")
    return prediction

"""
TODO: write /classify/url function
"""

# if __name__ == "__main__":
#     uvicorn.run(app, debug=True)
