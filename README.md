# YouTube Crawler

Description

This repo provides with a sample YouTube video crawler written using the YouTube Data API V3. Given a Youtube channel, or playlist the crawler yields the following information:
    
    **Video Id**
    **Title**
    **Url**
    **Duration in seconds**
    **Views count**
    **Thumbnail Image Url**
    **Original Image Url**
    

After running the crawler, the crawled data is saved into a mysql database. The crawler also save thumbnail and original images to the user's downloads directory.

## Usage

Install Python 3.8 and install the dependencies included in the requirements.txt file, using the command "pip install -r requirements.txt". Then, download the repo and open the terminal in root folder. For the input, there are the following method:

    **command line**

For CLI, use command "python run.py -c channel url". This is an example of CLI usage : "python run.py -c https://www.youtube.com/user/AsapSCIENCE/videos"
You can also use the command line interface to find details about videos in a specific playlist. You can use the command "python run.py -p playlist_url". Here's an example of using CLI for gathering playlist details : "python run.py -p https://www.youtube.com/playlist?list=PLvFsG9gYFxY907xODmFk-faD6uO0a3gMh"

The crawler updates the database for new information about the channel videos or those in a playlist using a scheduler that crawls for new updates every weekday at 10 am.
