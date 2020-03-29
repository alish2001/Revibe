import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pydub import AudioSegment
from pysndfx import AudioEffectsChain

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def vibe_song(name):
    song = AudioSegment.from_mp3(os.path.abspath("./songs/" + name))
    slow_sound = speed_change(song, 0.9)
    slow_sound.export("inter.mp3", format = "mp3")
    fx = (AudioEffectsChain().reverb())
    vibe_url = "/songs/" + name.replace(" ", "_") + "_VIBED" + ".mp3"
    print(os.path.abspath("." + vibe_url))
    print(os.path.abspath("" + vibe_url))
    fx("inter.mp3",  os.path.abspath("." + vibe_url))
    os.remove("inter.mp3")
    
    return vibe_url

def vibeView(request):
    if request.method == 'POST' and request.FILES['song']:
        song = request.FILES['song']
        fs = FileSystemStorage()
        fs.save(song.name, song)
        #uploaded_file_url = fs.url(song.name)
        vibeURL = vibe_song(song.name)
        return render(request, 'revibe.html', {
            'uploaded_file_url': vibeURL
        })
    return render(request, 'revibe.html')