import requests
import json
import recon
import argparse

def checkRoom(roomCode, _id = None):
    # this function gets the roomHash which is required to get more info about the ongoing game
    url = "https://game.quizizz.com/play-api/v5/checkRoom"
    r = requests.post(url, json = {"roomCode":roomCode, "mongoId":_id})
    try:
        d = json.loads(r.text.strip())
        roomHash = d["room"]["hash"]
    except:
        print(r.text)
    return roomHash

def addRequiredArgs(parser):
    # argparse add required arguements roomCode, playerId
    required = parser.add_argument_group('Required arguments')

    required.add_argument(
        "ROOM",
        help = "Code to join game",
        type = str
    )

    required.add_argument(
        "PLAYER",
        help = "Player's username",
        type = str
    )
    return

def addOptionalArgs(parser):
    # argparse add optional arguement _id and functions to call
    optional = parser.add_argument_group('Optional arguments')

    optional.add_argument(
        "-i",
        "--id",
        help = "Unique ID assigned to each player\nCan be found in source code, varname = _id",
        type = str
    )

    optional.add_argument(
        "-o",
        "--overview",
        help = "Prints a quick overview of the game",
        action = "store_true"
    )

    optional.add_argument(
        "-p",
        "--players",
        help = "Prints a list of players in the game\n(Only works if game does not require login)",
        action = "store_true"
    )

    optional.add_argument(
        "-a",
        "--answers",
        help = "Prints a list of questions and correct answers\n(Only works if game does not require login)",
        action = "store_true"
    )    

    optional.add_argument(
        "-h",
        "--help",
        action = "help",
        help = "Show this help message and exit"
    )
    return

def main():
    parser = argparse.ArgumentParser(
        description = "Quizizz Tool\nFinds room hash for given room",
        add_help = False,
        formatter_class = argparse.RawTextHelpFormatter
        )
    parser.add_help = True

    addRequiredArgs(parser)
    addOptionalArgs(parser)

    args = parser.parse_args()

    roomCode = args.ROOM
    playerId = args.PLAYER
    _id = args.id

    roomHash = checkRoom(roomCode, _id)
    print(f"Room Hash: {roomHash}")

    if args.overview:
        print("\n\n\n----- Overview -----")
        recon.quickOverview(roomHash, playerId, _id)
    if args.players:
        print("\n\n\n----- Players -----")
        recon.capturePlayers(roomHash, playerId, _id)
    if args.answers:
        print("\n\n\n----- Questions & Answers -----")
        recon.getAnswers(roomHash, playerId, _id)
    return

if __name__ == "__main__":
    main()

