from flask import Flask, request, render_template
import json
import os
import random
import ItemClass
from pydub import AudioSegment
from pprint import pprint

app = Flask(__name__)
sound = AudioSegment.from_mp3("TrumpSpeech.mp3")

@app.route('/load')
def JsonReader():
    # print os.listdir("./")

    with open("align.json") as json_data:
        d = json.load(json_data)
        wordList = {}
        for x in d["words"]:
            # pprint(x)
            if x["case"] == "success":
                word = x["alignedWord"]
                start = x["start"]
                end = x["end"]
                # item = ItemClass.Item()
                item = ItemClass.Item(word,start,end)
                wordList[word] = item
                AudioSplice(item)
    # pprint(wordList)
    return render_template("index.html")

@app.route('/')
def home():
    return render_template("index.html")


def AudioSplice(item):
    # print(str(item.s) + " : " + str(item.e))
    segment = sound[item.s*1000:item.e*1000]
    print(segment)
    segment.export("soundbyte/"+item.w+".mp3",format="mp3")

@app.route('/speak', methods=["POST"])
def trumpSpeak():
    sentence = request.form['sentence']
    sentenceList = sentence.split(" ")
    speechList = []
    for each in sentenceList:
        print each
        songPath = "soundbyte/" + each + ".mp3"
        speechList.append(songPath)

    combined = AudioSegment.empty()
    print speechList
    try:
        for song in speechList:
            Audio = AudioSegment.from_file(song, "mp3")
            combined += Audio
    except:
        return "FAKE NEWS."
        # combined =combined.append(song)
    output = "output"+str(random.randint(0,10))+".mp3"
    combined.export(output, format="mp3")

    return "<h1>GREAT SUCCESS!</h1>"


if __name__ == '__main__':
    app.run(debug = True)
