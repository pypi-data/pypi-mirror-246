"""This module contains server of yol_app."""
from configparser import ConfigParser
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from yol_app.trace_logic import trace_manager
from typing import List
import os
import requests


app = FastAPI()

# Function to parse the version from setup.cfg
def get_current_version():
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '..', 'setup.cfg'))
    return config['metadata']['version']


@app.get("/check-version")
def check_version():
    try:
        current_version = get_current_version()
        response = requests.get(f'https://pypi.org/pypi/yol_app/json')
        latest_version = response.json()['info']['version']

        if current_version != latest_version:
            return JSONResponse(content={
                "message": f"A new version {latest_version} is available. You are currently using {current_version}.",
                "current_version": current_version,
                "latest_version": latest_version
            })
        else:
            return JSONResponse(content={
                "message": "You are using the latest version.",
                "current_version": current_version,
                "latest_version": latest_version
            })
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Version check failed due to PyPI request issue.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


current_directory = os.path.dirname(os.path.abspath(__file__))
static_directory = os.path.join(current_directory, "trace_display", "build", "static")
index_file_path = os.path.join(current_directory, "trace_display", "build", "index.html")


# Serve React build as static files
app.mount("/static", StaticFiles(directory=static_directory), name="static")

trace_output = []

@app.get("/")
def read_root():
  return FileResponse(index_file_path)

@app.get("/trace")
def get_trace():
  output = trace_manager.get_trace_output()
  #trace_manager.reset_trace_output()  # Clear the output once it's been fetched
  return output

