# Intro

A brief analysis of Quizizz.com

Quizizz uses /play-api/ for all the game-related api needs. (Filtering for game.quizizz.com in BurpSuite also helps to reduce the clutter of requests)

In this brief writeup, we dive into how an endpoint can be exploited to earn more points than intended.

Obligatory disclaimer: This is purely for research purposes, do not use for any malicious purposes, etc.

# Table Of Contents

- [Intro](#intro)
- [Table Of Contents](#table-of-contents)
- [Functions in /play-api/](#functions-in-play-api)
  - [/v5/checkRoom](#v5checkroom)
    - [Request](#request)
    - [Response](#response)
  - [/v5/rejoinGame](#v5rejoingame)
    - [Request](#request-1)
    - [Response](#response-1)
  - [/v4/proceedGame](#v4proceedgame)
    - [Request](#request-2)
    - [Response](#response-2)
  - [/v4/soloProceed](#v4soloproceed)
    - [Request](#request-3)
    - [Response](#response-3)
- [Big No-No](#big-no-no)
  - [Proof of concept](#proof-of-concept)
  - [Notes](#notes)


# Functions in /play-api/

## /v5/checkRoom

Sending a POST request with the roomCode as the param will return JSON of room details, such as but not limited to, questionIds, game options, etc. Nothing too revealing. Example of request and response shown below.

### Request
<details>
  <summary>Head</summary>
  
  ```
POST /play-api/v5/checkRoom HTTP/1.1
Host: game.quizizz.com
Connection: close
Content-Length: 23
sec-ch-ua: ******
Accept: application/json
experiment-name: main_main
X-CSRF-TOKEN: ******
sec-ch-ua-mobile: ?0
User-Agent: ******
Content-Type: application/json
Origin: https://quizizz.com
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://quizizz.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: _gid=******; _ga_N10L950FVL=******; _ga=******
  ```

</details>

<details>
  <summary>Body</summary>
  
  ```json
{"roomCode":"40******"}
  ```

</details>

<br/>

### Response
<details>
  <summary>Head</summary>
  
  ```
HTTP/1.1 200 OK
Date: ******
Content-Type: application/json; charset=utf-8
Content-Length: 1676
Connection: close
X-Powered-By: Express
Access-Control-Allow-Origin: https://quizizz.com
Vary: Origin
Access-Control-Allow-Credentials: true
ETag: ******
  ```
  
</details>

<details>
  <summary>Body</summary>
  
  ```json
{
    "__cid__": null,
    "room": {
        "hash": "61f555496b2e4c001d******",
        "type": "async",
        "expiry": ******,
        "createdAt": 1643468******,
        "version": [{
            "type": "MCQ",
            "version": 2
        }],
        "code": "40******",
        "assignments": null,
        "deleted": false,
        "experiment": "recommAdm_exp",
        "hostId": "61f552ccbecace001d******",
        "hostSessionId": "",
        "hostOccupation": "other",
        "canvas": {
            "host": false,
            "player": false
        },
        "options": {
            "groupIds": null,
            "jumble": true,
            "jumbleAnswers": true,
            "limitAttempts": 0,
            "loginRequired": false,
            "memes": true,
            "showAnswers": true,
            "showAnswers_2": "always",
            "studentLeaderboard": true,
            "studentMusic": true,
            "studentQuizReview": true,
            "studentQuizReview_2": "yes",
            "timer": true,
            "timer_3": "classic",
            "redemption": "yes",
            "powerups": "yes",
            "nicknameGenerator": false,
            "adaptive": false,
            "questionsPerAttempt": 0,
            "memeset": "5c65cf51a7d584001a******"
        },
        "questions": ["61f5538dfb7262001d******", "61f554fbc04a6f001d******"],
        "groupIds": [],
        "groupsInfo": {
            "mode": "check",
            "create": {},
            "gcl": [],
            "assigned": [],
            "hasGCL": false,
            "assignedTo": {},
            "data": {
                "title": null,
                "description": null
            },
            "grading": {
                "isGraded": true,
                "maxPoints": 100
            }
        },
        "startedAt": 1643468******,
        "state": "running",
        "totalCorrect": 8,
        "totalPlayers": 6,
        "totalQuestions": 10,
        "assignmentTitle": null,
        "versionId": "61f553674f136f001d******",
        "collectionId": null,
        "unitId": null,
        "replayOf": null,
        "courseId": null,
        "reopenable": true,
        "reopened": true,
        "soloApis": null,
        "subscription": {
            "playerLimit": 500,
            "trialEndAt": null,
            "adsFree": false,
            "branding": false
        },
        "simGame": false,
        "metadata": {},
        "responseLink": "shard",
        "totalAnswerableQuestions": 2,
        "traits": {
            "isQuizWithoutCorrectAnswer": false,
            "totalSlides": 0
        },
        "organization": "",
        "isShared": false,
        "createGroup": null
    },
    "player": {
        "isAllowed": true,
        "loginRequired": false,
        "attempts": []
    }
}
  ```
  
</details>

<br/><br/><br/>

## /v5/rejoinGame
Sending a POST request to the above will result in a response with details of the room, including questions and their respective options, and scoreboard. Example of request and response below.

### Request
<details>
  <summary>Head</summary>
  
  ```
POST /play-api/v5/rejoinGame HTTP/1.1
Host: game.quizizz.com
Connection: close
Content-Length: 176
sec-ch-ua: ******
Accept: application/json
experiment-name: main_main
X-CSRF-TOKEN: ******
sec-ch-ua-mobile: ?0
User-Agent: ******
Content-Type: application/json
Origin: https://quizizz.com
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://quizizz.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: _gid=******; _ga_N10L950FVL=******; _ga=******
  ```
  
</details>

<details>
  <summary>Body</summary>
  
  ```json
{
	"roomHash": "61f555496b2e4c001d******",
	"playerId": "************",
	"type": "async",
	"state": "running",
	"startSource": "rejoin|gameOver",
	"powerupInternalVersion": "13",
	"soloApis": "v2"
}
  ```
  
</details>

<br/>

### Response
<details>
  <summary>Head</summary>
  
  ```
HTTP/1.1 200 OK
Date: ******
Content-Type: application/json; charset=utf-8
Content-Length: 11105
Connection: close
X-Powered-By: Express
Access-Control-Allow-Origin: https://quizizz.com
Vary: Origin
Access-Control-Allow-Credentials: true
ETag: ******
  ```
  
</details>

<details>
  <summary>Body</summary>
  
  ```json
{
	"__cid__": null,
	"room": {
		"db": "redis",
		"code": "40******",
		"assignments": null,
		"createdAt": 1643468105531,
		"deleted": false,
		"experiment": "recommAdm_exp",
		"hash": "61f555496b2e4c001d******",
		"hostId": "61f552ccbecace001d******",
		"hostSessionId": "",
		"hostOccupation": "other",
		"canvas": {
			"host": false,
			"player": false
		},
		"name": "testing",
		"options": {
			"groupIds": null,
			"jumble": true,
			"jumbleAnswers": true,
			"limitAttempts": 0,
			"loginRequired": false,
			"memes": true,
			"showAnswers": true,
			"showAnswers_2": "always",
			"studentLeaderboard": true,
			"studentMusic": true,
			"studentQuizReview": true,
			"studentQuizReview_2": "yes",
			"timer": true,
			"timer_3": "classic",
			"redemption": "yes",
			"powerups": "yes",
			"nicknameGenerator": false,
			"adaptive": false,
			"questionsPerAttempt": 0,
			"memeset": "5c65cf51a7d584001a******"
		},
		"questions": {
			"61f554fbc04a6f001d******": {
				"_id": "61f554fbc04a6f001d******",
				"type": "MCQ",
				"ver": 2,
				"published": true,
				"structure": {
					"settings": {
						"hasCorrectAnswer": true,
						"fibDataType": "string"
					},
					"theme": {
						"fontColor": {
							"text": "#5D2057"
						},
						"background": {
							"color": "#FFFFFF",
							"image": "",
							"video": ""
						},
						"shape": {
							"largeShapeColor": "#F2F2F2",
							"smallShapeColor": "#9A4292"
						},
						"titleFontFamily": "Quicksand",
						"fontFamily": "Quicksand"
					},
					"explain": {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": ""
					},
					"kind": "MCQ",
					"query": {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[question1]******</p>"
					},
					"options": [{
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[option1]******</p>"
					}, {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[option2]******</p>"
					}, {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[option3]******</p>"
					}, {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[option4]******</p>"
					}],
					"hasMath": false,
					"answer": 3
				},
				"topics": [],
				"isSuperParent": false,
				"teleportFrom": null,
				"createdAt": "2022-01-******",
				"updated": "2022-01-******",
				"__v": 0,
				"time": 30000,
				"state": "inactive",
				"attempt": 0,
				"cause": ""
			},
			"61f5538dfb7262001d******": {
				"_id": "61f5538dfb7262001d******",
				"type": "MCQ",
				"ver": 2,
				"published": true,
				"structure": {
					"settings": {
						"hasCorrectAnswer": true,
						"fibDataType": "string"
					},
					"theme": {
						"fontColor": {
							"text": "#5D2057"
						},
						"background": {
							"color": "#FFFFFF",
							"image": "",
							"video": ""
						},
						"shape": {
							"largeShapeColor": "#F2F2F2",
							"smallShapeColor": "#9A4292"
						},
						"titleFontFamily": "Quicksand",
						"fontFamily": "Quicksand"
					},
					"explain": {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": ""
					},
					"kind": "MCQ",
					"query": {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[question2]******</p>"
					},
					"options": [{
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[option1]******</p>"
					}, {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[option2]******</p>"
					}, {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[option3]******</p>"
					}, {
						"math": {
							"latex": [],
							"template": null
						},
						"type": "text",
						"hasMath": false,
						"media": [],
						"text": "<p>******[option4]******</p>"
					}],
					"hasMath": false,
					"answer": 1
				},
				"topics": [],
				"isSuperParent": false,
				"teleportFrom": null,
				"createdAt": "2022-01-******",
				"updated": "2022-01-******",
				"__v": 0,
				"time": 30000,
				"state": "inactive",
				"attempt": 0,
				"cause": ""
			}
		},
		"quizId": "3b5******427346365******8686f6f******1b74b04b9f******0b43e8eb4a2",
		"quizName": "testing",
		"groupIds": [],
		"groupsInfo": {
			"mode": "check",
			"create": {},
			"gcl": [],
			"assigned": [],
			"hasGCL": false,
			"assignedTo": {},
			"data": {
				"title": null,
				"description": null
			},
			"grading": {
				"isGraded": true,
				"maxPoints": 100
			}
		},
		"startedAt": 16434******31,
		"state": "running",
		"totalCorrect": 10,
		"totalPlayers": 7,
		"totalQuestions": 12,
		"type": "async",
		"assignmentTitle": null,
		"versionId": "61f553674f136f001d******",
		"expiry": 1******,
		"collectionId": null,
		"unitId": null,
		"replayOf": null,
		"courseId": null,
		"reopenable": true,
		"reopened": true,
		"soloApis": null,
		"subscription": {
			"playerLimit": 500,
			"trialEndAt": null,
			"adsFree": false,
			"branding": false
		},
		"simGame": false,
		"metadata": {},
		"responseLink": "shard",
		"totalAnswerableQuestions": 2,
		"traits": {
			"isQuizWithoutCorrectAnswer": false,
			"totalSlides": 0
		},
		"organization": "",
		"isShared": false,
		"players": [{
			"assignment": null,
			"attempts": [],
			"createdAt": 16434******53,
			"currentStreak": 2,
			"deleted": false,
			"experiment": "curriculum_exp",
			"id": "testing01",
			"isOver": true,
			"isUnderage": false,
			"lastPlayedAt": 1643******616,
			"locale": "en",
			"maximumStreak": 2,
			"metadata": {
				"type": "******",
				"model": "******",
				"ua": {
					"family": "******",
					"version": "******"
				},
				"os": {
					"family": "******",
					"version": "******"
				}
			},
			"mongoId": null,
			"monster": 23,
			"monsterId": 23,
			"name": "",
			"origin": "******",
			"playerId": "******01",
			"playerMetadata": {},
			"powerupEffects": [],
			"powerups": [],
			"questions": null,
			"rank": 1,
			"score": 1940,
			"startedAt": 1643******753,
			"totalAttempt": 2,
			"totalCorrect": 2,
			"totalResponses": 2,
			"uid": "8b******-b689-4******9c-******5f34e5",
			"userAddons": null
		}, 
		"questionIds": ["61f5538dfb7262001d******", "61f554fbc04a6f001d******"]
	},
	"player": {
		"assignment": null,
		"attempts": [],
		"createdAt": 1643******550,
		"currentStreak": 2,
		"deleted": false,
		"experiment": "main_main",
		"id": "testing007**",
		"isOver": true,
		"isUnderage": false,
		"lastPlayedAt": 1643******774,
		"locale": "en",
		"maximumStreak": 2,
		"metadata": {
			"type": "desktop",
			"model": "Other",
			"ua": {
				"family": "Chrome",
				"version": "89.0.4389"
			},
			"os": {
				"family": "Windows",
				"version": "10.0.0"
			}
		},
		"mongoId": null,
		"monster": 20,
		"monsterId": 20,
		"name": "",
		"origin": "web",
		"playerId": "******007**",
		"playerMetadata": {},
		"powerupEffects": [],
		"powerups": [],
		"questions": null,
		"rank": 4,
		"score": 1200,
		"startedAt": 1643******550,
		"totalAttempt": 2,
		"totalCorrect": 2,
		"totalResponses": 3,
		"uid": "******",
		"userAddons": null,
		"responses": [{
			"id": "61f55b761015ce001d******",
			"createdAt": "2022-01-******",
			"deleted": false,
			"elapsed": 18640,
			"isCorrect": false,
			"playerId": "******007**",
			"questionId": "61f5538dfb7262001d******",
			"questionType": "MCQ",
			"response": 3,
			"scoreBreakup": {
				"base": 0,
				"timer": 0,
				"streak": 0,
				"powerups": [],
				"total": 0
			},
			"score": 0,
			"timeTaken": 1831,
			"teamAdjustment": 0,
			"_v": "r2",
			"attempt": 0,
			"state": "attempted",
			"metadata": {
				"rescored": []
			}
		}, {
			"id": "******",
			"createdAt": "2022-01-******",
			"deleted": false,
			"elapsed": 81395,
			"isCorrect": true,
			"playerId": "testing007**",
			"questionId": "61f554fbc04a6f001d******",
			"questionType": "MCQ",
			"response": 3,
			"scoreBreakup": {
				"base": 600,
				"timer": 0,
				"streak": 0,
				"powerups": [],
				"total": 600
			},
			"score": 600,
			"timeTaken": 47643,
			"teamAdjustment": 0,
			"_v": "r2",
			"attempt": 0,
			"state": "attempted",
			"metadata": {
				"rescored": []
			}
		}, {
			"id": "61f55bc2a1dcec00******",
			"createdAt": "2022-01-******",
			"deleted": false,
			"elapsed": 95214,
			"isCorrect": true,
			"playerId": "******007**",
			"questionId": "61f5538dfb7262001d******",
			"questionType": "MCQ",
			"response": 1,
			"scoreBreakup": {
				"base": 600,
				"timer": 0,
				"streak": 0,
				"powerups": [],
				"total": 600
			},
			"score": 600,
			"timeTaken": 2210,
			"teamAdjustment": 0,
			"_v": "r2",
			"attempt": 1,
			"state": "attempted",
			"metadata": {
				"rescored": []
			}
		}],
		"scoreTrail": []
	},
	"powerupConfigVersion": "13"
}
  ```
  
</details>

<br/><br/><br/>

## /v4/proceedGame
This endpoint helps to send your score to the server. A POST request containing the player data, update to score, and question id is sent. Response will have JSON of updated score and leaderboard. Example of request and response below.

### Request
<details>
  <summary>Head</summary>
  
  ```
POST /play-api/v4/proceedGame HTTP/1.1
Host: game.quizizz.com
Connection: close
Content-Length: 651
sec-ch-ua: ******
Accept: application/json
experiment-name: main_main
X-CSRF-TOKEN: ******
sec-ch-ua-mobile: ?0
User-Agent: ******
Content-Type: application/json
Origin: https://quizizz.com
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://quizizz.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: _gid=******; _ga_N10L950FVL=******; _ga=******; suid=******
  ```
  
</details>

<details>
  <summary>Body</summary>
  
  ```json
{
	"roomHash": "61f555496b2e4c001d******",
	"playerId": "******007**",
	"response": {
		"attempt": 0,
		"questionId": "61f554fbc04a6f001d******",
		"questionType": "MCQ",
		"response": 3,
		"responseType": "original",
		"timeTaken": 47643,
		"isEvaluated": false,
		"state": "attempted",
		"provisional": {
			"scores": {
				"correct": 600,
				"incorrect": 0
			},
			"scoreBreakups": {
				"correct": {
					"base": 600,
					"timer": 0,
					"streak": 0,
					"powerups": [],
					"total": 600
				},
				"incorrect": {
					"base": 0,
					"timer": 0,
					"streak": 0,
					"powerups": [],
					"total": 0
				}
			},
			"teamAdjustments": {
				"correct": 0,
				"incorrect": 0
			}
		}
	},
	"questionId": "61f554fbc04a6f001d******",
	"powerupEffects": {
		"destroy": []
	},
	"gameType": "async",
	"quizVersionId": "61f553674f136f001d******",
	"elapsed": 0
}
  ```
  
</details>

<br/>

### Response
<details>
  <summary>Head</summary>
  
  ```
HTTP/1.1 200 OK
Date: ******
Content-Type: application/json; charset=utf-8
Content-Length: 1094
Connection: close
X-Powered-By: Express
Access-Control-Allow-Origin: https://quizizz.com
Vary: Origin
Access-Control-Allow-Credentials: true
ETag: ******
  ```
  
</details>
  
</details>

<details>
  <summary>Body</summary>
  
  ```json
{
	"__cid__": null,
	"response": {
		"id": "61f55bb431ead1001d******",
		"createdAt": "2022-01-******",
		"deleted": false,
		"elapsed": 81395,
		"isCorrect": true,
		"playerId": "testing007**",
		"questionId": "61f554fbc04a6f001d******",
		"questionType": "MCQ",
		"response": 3,
		"scoreBreakup": {
			"base": 600,
			"timer": 0,
			"streak": 0,
			"powerups": [],
			"total": 600
		},
		"score": 600,
		"timeTaken": 47643,
		"teamAdjustment": 0,
		"_v": "r2",
		"attempt": 0,
		"state": "attempted",
		"metadata": {
			"rescored": []
		}
	},
	"playerId": "******007**",
	"question": {
		"structure": {
			"answer": 3
		}
	},
	"player": {
		"currentStreak": 1,
		"maximumStreak": 1
	},
	"powerupEffects": [],
	"leaderboard": [{
		"playerId": "******01",
		"score": 1940,
		"rank": 1,
		"monsterId": 23,
		"origin": "******",
		"userAddons": null
	}, {
		"playerId": "******02",
		"score": 1930,
		"rank": 2,
		"monsterId": 24,
		"origin": "******",
		"userAddons": null
	}, {
		"playerId": "******02**",
		"score": 1560,
		"rank": 3,
		"monsterId": 30,
		"origin": "******",
		"userAddons": null
	}, {
		"playerId": "******007",
		"score": 900,
		"rank": 4,
		"monsterId": 7,
		"origin": "******",
		"userAddons": null
	}, {
		"playerId": "******007**",
		"score": 600,
		"rank": 5,
		"monsterId": 20,
		"origin": "******",
		"userAddons": null
	}],
	"playerCount": 5,
	"err": null
}
  ```
  
</details>

<br/><br/><br/>

## /v4/soloProceed
Apparently, Quizizz has a flashcard feature (which can be disabled). The params sent are similar to that of /v4/proceedGame, and response is similar, with the exception of the lack of scoreboard and the answer shown. Example of request and response shown below.

### Request
<details>
  <summary>Head</summary>
  
  ```
POST /play-api/v4/soloProceed HTTP/1.1
Host: game.quizizz.com
Connection: close
Content-Length: 617
sec-ch-ua: ******
Accept: application/json
experiment-name: curriculum_exp
X-CSRF-TOKEN: ******
sec-ch-ua-mobile: ?0
User-Agent: ******
Content-Type: application/json
Origin: https://quizizz.com
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://quizizz.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
  ```
  
</details>

<details>
  <summary>Body</summary>
  
  ```json
{
	"roomHash": "61f7805254c7760020******",
	"playerId": "qwerty",
	"response": {
		"attempt": 0,
		"questionId": "61f5538dfb7262001d******",
		"questionType": "MCQ",
		"response": -1,
		"responseType": "original",
		"timeTaken": 1844,
		"isEvaluated": false,
		"provisional": {
			"scores": {
				"correct": 600,
				"incorrect": 0
			},
			"scoreBreakups": {
				"correct": {
					"base": 600,
					"timer": 0,
					"streak": 0,
					"powerups": [],
					"total": 600
				},
				"incorrect": {
					"base": 0,
					"timer": 0,
					"streak": 0,
					"powerups": [],
					"total": 0
				}
			},
			"teamAdjustments": {
				"correct": 0,
				"incorrect": 0
			}
		}
	},
	"questionId": "61f5538dfb7262001d******",
	"powerupEffects": {
		"destroy": []
	},
	"gameType": "solo",
	"quizVersionId": "61f553674f136f001d******"
}
  ```
  
</details>

<br/>

### Response
<details>
  <summary>Head</summary>
  
  ```
HTTP/1.1 200 OK
Date: ******
Content-Type: application/json; charset=utf-8
Content-Length: 531
Connection: close
X-Powered-By: Express
Access-Control-Allow-Origin: https://quizizz.com
Vary: Origin
Access-Control-Allow-Credentials: true
ETag: ******
  ```
  
</details>

<details>
  <summary>Body</summary>
  
  ```json
{
	"__cid__": null,
	"data": {
		"response": {
			"id": "61f784d076f96c001d******",
			"createdAt": "2022-01-******",
			"deleted": false,
			"elapsed": 0,
			"isCorrect": false,
			"playerId": "qwerty",
			"questionId": "61f5538dfb7262001d******",
			"questionType": "MCQ",
			"response": -1,
			"scoreBreakup": {
				"base": 0,
				"timer": 0,
				"streak": 0,
				"powerups": [],
				"total": 0
			},
			"score": 0,
			"timeTaken": 1844,
			"teamAdjustment": 0,
			"_v": "r2",
			"attempt": 0,
			"state": "attempted",
			"metadata": {
				"rescored": []
			}
		},
		"playerId": "qwerty",
		"powerupEffects": [],
		"metadata": {},
		"question": {
			"structure": {
				"answer": 1
			}
		}
	}
}
  ```
  
</details>


<br/><br/><br/>

# Big No-No
Calculating the score on the client side is a big no-no. Why? Because this means the client can *fake their scores*.

By sending an edited POST request to the /v4/proceedGame endpoint, users can artificially inflate their scores and decrease their time to solve.

<br/>

## Proof of concept
By using BurpSuite to intercept and edit the POST request, we can change several params in the JSON object.

A portion of the JSON is shown below.

<table>
<tr>
<td>Original</td>
<td>Edited</td>
</tr>

<tr>
<td>

```json
"response": {
		"attempt": 0,
		"questionId": "61f554fbc04a6f001d******",
		"questionType": "MCQ",
		"response": 3,
		"responseType": "original",
		"timeTaken": 47643,
		"isEvaluated": false,
		"state": "attempted",
		"provisional": {
			"scores": {
				"correct": 600,
				"incorrect": 0
			},
			"scoreBreakups": {
				"correct": {
					"base": 600,
					"timer": 0,
					"streak": 0,
					"powerups": [],
					"total": 600
				},
				"incorrect": {
					"base": 0,
					"timer": 0,
					"streak": 0,
					"powerups": [],
					"total": 0
				}
			},
			"teamAdjustments": {
				"correct": 0,
				"incorrect": 0
			}
		}
```

</td>
<td>

```json
"response": {
		"attempt": 0,
		"questionId": "61f554fbc04a6f001d******",
		"questionType": "MCQ",
		"response": 3, // this can be edited
		"responseType": "original",
		"timeTaken": 1001, // decrease solve time
		"isEvaluated": false,
		"state": "attempted",
		"provisional": {
			"scores": {
				"correct": 2200, // change your total score here
				"incorrect": 0
			},
			"scoreBreakups": {
				"correct": {
					"base": 2000, // change score here too
					"timer": 200, // usually adds bonus score if you solve fast
					"streak": 0, // you can also add more score here
					"powerups": [],
					"total": 2200 // change your total score here (again)
				},
				"incorrect": {
					"base": 0,
					"timer": 0,
					"streak": 0,
					"powerups": [],
					"total": 0
				}
			},
			"teamAdjustments": {
				"correct": 0,
				"incorrect": 0
			}
		}
```

</td>
</tr>
</table>

By editing the request, you are able to earn extra points.

<br/>

## Notes

1. There is a hard-coded time limit before the page throws an error (of not being able to reach server)
	- You can "bypass" this by letting it fail to reach the server first
	- Edit the current intercepted request in BurpSuite, and copy it to clipboard
	- Forward the stuck request, wait for the page to reload itself, then quickly paste and forward the request
2. There is a server-sided limit on how many points you can earn from a question
	- Don't be too greedy, or it will throw an error
	- Server-side does **NOT** calculate any bonus, any amount of points in the timer or streak will work, regardless of the amount of time spent and/or the amount of correct answers

