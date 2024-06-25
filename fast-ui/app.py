from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import polars as pl
from typing import Dict

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/dataframe/{input_string}")
async def get_dataframe(input_string: str) -> Dict:
    # Create a sample DataFrame based on the input string
    # In a real application, you might do more complex processing here
    df = pl.DataFrame({
        'input': [input_string],
        'length': [len(input_string)],
        'uppercase': [input_string.upper()],
        'reverse': [input_string[::-1]]
    })
    print(df)
    
    result = df.to_dicts()
    logger.info(f"Returning result: {result}")
    return {"data": result} 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
