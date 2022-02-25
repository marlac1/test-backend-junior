import logging
from os import path

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app import api, dependencies

basedir = path.dirname(__file__)

# # Prepare dependencies
inject = dependencies.BoyAPI()
inject.config.from_ini(path.join(basedir, "config.ini"), required=True)


inject.wire(modules=[dependencies, api])
dependencies.setup_api_backgound()


logging.Logger("main").info("BOY API V2 starting...")

serve = api.run()


serve.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("boy:serve", host="0.0.0.0", port=8000, reload=False)  # nosec
