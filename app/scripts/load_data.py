import asyncio
import json
import logging
import os.path

from app import config, db
from app.space_agencies.crud import create_space_agency
from app.space_agencies.models import SpaceAgencyBase

LOGGER = logging.getLogger()


async def populate_space_agencies(verbose=True):
    datafile = os.path.join(config.DATA_FIXTURES_PATH, "space_agencies.json")
    space_agency_list = json.loads(open(datafile).read())
    for item in space_agency_list:
        async with db.async_session() as session:
            input_rest = SpaceAgencyBase(**item)
            await create_space_agency(session, input_rest)
            verbose and print("Created space agency %s" % item["name"])


def run():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(populate_space_agencies())


if __name__ == "__main__":
    run()
