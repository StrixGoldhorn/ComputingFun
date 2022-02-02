import requests
import json

def gatherData(roomHash, playerId, _id):
    url = "https://game.quizizz.com/play-api/v5/rejoinGame"
    r = requests.post(url, json = {"roomHash":roomHash,"playerId":playerId,"type":"async","state":"running","startSource":"rejoin|gameOver","powerupInternalVersion":"13","soloApis":"v2", "mongoId":_id})
    try:
        d = json.loads(r.text.strip())
        return d
    except:
        return r.text

def quickOverview(roomHash, playerId, _id = None):
    d = gatherData(roomHash, playerId, _id)
    try:
        print(
            f'Name: {d["room"]["name"]}' +'\n'+ \
            f'Attempts: {d["room"]["options"]["limitAttempts"]}' +'\n'+ \
            f'Correct/Total: {d["room"]["totalCorrect"]}/{d["room"]["totalQuestions"]}' +'\n'+ \
            f'Total Players: {d["room"]["totalPlayers"]}' +'\n'+ \
            f'Game Settings: {d["room"]["options"]}'
        )
    except:
        print("Error. rejoinGame POST response dump below:")
        print(d)
    return

def capturePlayers(roomHash, playerId, _id = None):
    d = gatherData(roomHash, playerId, _id)
    try:
        for i in range(len(d["room"]["players"])):
            p = d["room"]["players"][i]
            print(
                '-'*50 +'\n'+ \
                f'RANK #{p["rank"]}' +'\n'+ \
                f'Name: {p["id"]}' +'\n'+ \
                f'Platform: {p["origin"]}' +'\n'+ \
                f'UserAgent: {p["metadata"]["ua"]["family"]} {p["metadata"]["ua"]["version"]}' +'\n'+ \
                f'OS: {p["metadata"]["os"]["family"]} {p["metadata"]["os"]["version"]}' +'\n'+ \
                f'Score: {p["score"]} | {p["totalCorrect"]}/{p["totalAttempt"]}'
            )
    except:
        print("Error. rejoinGame POST response dump below:")
        print(d)
    return

def getAnswers(roomHash, playerId, _id = None):
    d = gatherData(roomHash, playerId, _id)
    try:
        qHashes = d["room"]["questions"]
        for q in qHashes:
            print("-"*50)
            qText = d["room"]["questions"][q]["structure"]["query"]["text"]
            print("Q:", qText)
            for i in range(len(d["room"]["questions"][q]["structure"]["options"])):
                print(i, d["room"]["questions"][q]["structure"]["options"][i]["text"])
            correct = d["room"]["questions"][q]["structure"]["answer"]
            print("Correct answer:", d["room"]["questions"][q]["structure"]["options"][correct]["text"])
    except:
        print("Error. rejoinGame POST response dump below:")
        print(d)
    return
