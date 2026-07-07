from gtts import gTTS
from discord.ext import commands
import discord
import os
from pydub import AudioSegment
from random import randint
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials

TOKEN = "-"

bot = commands.Bot(command_prefix = "!")

@bot.command(name='dajglos',pass_context=True)
async def dajglos(ctx):
    print("Daje głos")
    tts = gTTS('Dobrze ', lang='pl', slow=False)
    tts.save('dobrze.mp3')
    sound = AudioSegment.from_mp3("dobrze.mp3")
    sound.export("dobrze.mp3")
    user=ctx.message.author
    voice_channel=user.voice.channel
    if voice_channel!= None:
        channel=voice_channel.name
        await ctx.send('Użytkownik na kanale: '+ channel)
        channel=voice_channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('dobrze.mp3'), after= lambda e: print("Odtworzyłem"))
        while vc.is_playing():
            None
        vc.stop()
        await vc.disconnect()
    else:
        await ctx.send("Nie ma go na kanale")

@bot.command(name='song',pass_context=True)
async def song(ctx):
    print("Song")
    user=ctx.message.author
    voice_channel=user.voice.channel
    if voice_channel!= None:
        channel=voice_channel.name
        channel=voice_channel
        vc = await channel.connect()
        lz_uri = 'spotify:artist:159qqlGwzE04xyqpfAwRLo'
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="96d29a2590ae462ab47200c9559dc754",client_secret="4f8f90eab49b4c1cb24dab12fce1295f"))
        results = spotify.artist_top_tracks(lz_uri)
        print(results)
        value = 9
        for track in results['tracks'][:10]:
            if value == 0:
                await ctx.send('Tytuł: '+ track['name'])
                print('track    : ' + track['name'])
                print('audio    : ' + track['preview_url'])
                r = requests.get(track['preview_url'],allow_redirects=True)
                open('track.mp3', 'wb').write(r.content)
                vc.play(discord.FFmpegPCMAudio('track.mp3'), after= lambda e: print("Done"))
                print('cover art: ' + track['album']['images'][0]['url'])
                print()
            value -= 1
        while vc.is_playing():
            None
        vc.stop()
        await vc.disconnect()
    else:
        await ctx.send("Nie ma go na kanale")

bot.run(TOKEN)
