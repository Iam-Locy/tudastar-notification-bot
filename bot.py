import os
import json
import datetime
from time import sleep

import discord
from googleapiclient.discovery import build

YOUTUBE = build('youtube', 'v3', developerKey=os.environ["YOUTUBE_API_KEY"])
TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']


def checkPlaylistChange(playlist):
    request = YOUTUBE.playlists().list(
        part='contentDetails',
        id=playlist["id"]
    )

    response = request.execute()

    etag = response['items'][0]['etag']

    return {"result": playlist["etag"] != etag, "etag": etag}


def writeEtagChange(playlists, playlist, etag, playlistId):

    for index, source in enumerate(playlists[playlist]["sources"]):
        if source["id"] == playlistId:
            playlists[playlist]["sources"][index]["etag"] = etag

    newFile = json.dumps(playlists)

    with open("playlists.json", 'w') as f:
        f.write(newFile)


def getMostRecent(id):
    request = YOUTUBE.playlistItems().list(
        part='contentDetails',
        playlistId=id
    )

    response = request.execute()['items']
    videos = []

    for item in response:

        if 'videoPublishedAt' in item['contentDetails']:
            videos.append(item)

    mostRecentUpload = {
        "date": None,
        "id": ""
    }

    for video in videos:
        if mostRecentUpload['date'] == None:
            mostRecentUpload['date'] = datetime.datetime.fromisoformat(
                video['contentDetails']['videoPublishedAt'][:-1])
            mostRecentUpload['id'] = video['contentDetails']['videoId']

        elif datetime.datetime.fromisoformat(video['contentDetails']['videoPublishedAt'][:-1]) > mostRecentUpload["date"]:
            mostRecentUpload['date'] = datetime.datetime.fromisoformat(
                video['contentDetails']['videoPublishedAt'][:-1])
            mostRecentUpload['id'] = video['contentDetails']['videoId']

    return f'https://www.youtube.com/watch?v={mostRecentUpload["id"]}'

def getSubjectChannels(client, playlists):
    guild = discord.utils.get(client.guilds, name=GUILD)
    channels = list(filter(lambda channel: channel.category !=
                    None and channel.category.name == "Text Channels", guild.channels))
    channels = list(filter(lambda channel: channel.name in playlists, channels))

    return channels

def main():

    client = discord.Client()

    with open('./playlists.json', 'r') as f:
        playlistSources = json.load(f)

    @client.event
    async def on_ready():
        print(f'{client.user.name} has connected to Discord!')

        channels = getSubjectChannels(client, playlistSources)

        while True:

            for channel in channels:

                
                sources = playlistSources[channel.name]

                for playlist in sources["sources"]:

                    if playlist["id"] == "": continue

                    playlistChange = checkPlaylistChange(playlist)

                    if playlistChange["result"]:
                        writeEtagChange(playlistSources, channel.name, playlistChange["etag"], playlist["id"])

                        video = getMostRecent(playlist["id"])

                        await channel.send(f'Bővült a Tudástár {playlist["name"]} tárgyból')
                        await channel.send(video)
            
            sleep(900)

        

    client.run(TOKEN)


if __name__ == "__main__":
    main()
