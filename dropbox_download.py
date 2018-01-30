#!/usr/bin/env python

import asyncio
import aiohttp
import re
import tqdm
import os

# use selenium to run javascript on dropbox page to create links
from selenium import webdriver
driver = webdriver.PhantomJS()

# e.g. DROPBOX_URL ='https://www.dropbox.com/sh/23j4ldkj3jk32m/3lkjdlk3j2k34k4kkdkdjf?dl=0'
DROPBOX_URL = ''
DESTINATION_FOLDER = 'db_data'
MAX_CONCURRENT_DOWNLOADS = 5


def buildurls(urls_raw):
    """ create list of download urls - one for each file """

    # filter list for duplicates - turn it into a set and into a list again
    urls_raw = list(set(urls_raw))

    # very bad performance - n * n * n :( but very pythonic :)
    return [(
                url[:-5].split('/')[6],
                url.replace('dl=0', 'dl=1')
            ) for url in urls_raw]


def writetofile(directory, filename, content):
    """ simple helper method to write files onto the local filesystem """

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, filename), 'wb') as f:
        f.write(content)


async def getrequest(session, url, filetype='text'):
    """ downloads a file specified by url - filetypes are 'text', 'json' or 'binary' """

    async with session.get(url) as resp:
        if filetype is 'text':
            response = await resp.text()
        elif filetype is 'json':
            response = await resp.json()
        else:
            response = await resp.read()

        return response


async def download(url, filename, directory, semaphore):
    """ execute the get request and write the file """

    # use the semaphore to limit the concurrent connections
    with (await semaphore):
        async with aiohttp.ClientSession() as session:
            content = await getrequest(session, url, 'binary')

    writetofile(directory, filename, content)


async def parseresponse(url_overview):
    """ filter the response for all available items via href """
    
    # previous code:
    # async with aiohttp.ClientSession() as session:
    #     url_overview = await getrequest(session, DROPBOX_URL)
    
    # new code runs javascript to generate links
    driver.get(DROPBOX_URL)
    url_overview = driver.page_source
    
    # still much room for optimizations
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', url_overview)
    # only return urls with pattern "/sh/" since others are not files to download (e.g. css)
    urls = [x for x in urls if "/sh/" in x]

    return urls


async def asyncprogressbar(coros):
    """ visualize the progress with progressbar which shows how many files have already been downloaded """
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        await f


def main():
    """ starts download of the given dropbox directory """

    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    # do the preprocessing (parsing the site for urls and extracting the filenames
    urls_raw = loop.run_until_complete(parseresponse(DROPBOX_URL))
    urls_download = buildurls(urls_raw)

    # start the async download manager
    tasks = [download(url, filename, DESTINATION_FOLDER, sem) for filename, url in urls_download]
    loop.run_until_complete(asyncprogressbar(tasks))

    loop.stop()
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
