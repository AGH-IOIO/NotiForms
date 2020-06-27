# NotiForms
[![Build Status](https://travis-ci.com/AGH-IOIO/NotiForms.svg?branch=master)](https://travis-ci.com/AGH-IOIO/NotiForms)

- frontend
    - nginx
    - jquery 3.4.1
    - gentellala theme

- backend
    - flask
    - mongoDB


## Running
```
  docker-compose up
```
website will be available at: ```localhost:8081```

## Testing
   ```
   TEST=y docker-compose up --abort-on-container-exit
   ```

## Model

### User
```
User:
{
  username: string,  # unique
  email: string,  # unique
  password: string,
  teams: list[string],  # ONLY team names, NOT teams
  push_subscription_info: list[{
      user_agent: string,
    subscription_info: dict
  }]
}
```
### UnconfirmedUser
```
UnconfirmedUser:
{
  link: string,  # registration confirmation link, unique
  user: User document
}
```

### Team
```
Team:
{
  name: string,  # unique
  members: list[username]  # ONLY usernames, NOT users
}
```
### OpenTextQuestion
```
OpenTextQuestion:
{
  type: "open_text"
  title: string,
  answer: string # default ""
}
```
allowed types: "open_text", "single_choice", "multiple_choice", "date"

### FormTemplate
```
FormTemplate:
{
  owner: string,  # username
  title: string,
  questions: list[Question]  # list of Question documents
}
```

### Message
```
Message:
{
  _id: ObjectId,
  text: string,
  send_date: date,
  ref_id: ObjectId,  # ID obiektu form jakiego dotyczy
  viewed: boolean
}
```
### NotificationDetails
```
NotificationDetails:
{
  _id: ObjectId,
  type: string (“push”, “online” or “e-mail”),
  dead_period: int,
  before_deadline_frequency: int,
  after_deadline_frequency: int
}
```
## Rest API

```
POST /token
IN: 
{
  username: string,
  password: string
}

OUT:
200 OK          | {token: “...”}
400 Bad Request | {error: “msg”}
```

```
POST /users
IN: 
{
  username: string,
  password: string,
  email: string
}

OUT:
200 OK          | {to_co_wysłano}
400 Bad Request | {error: “msg”}
```
```
[A] GET /users
IN: 
{
  username: string,
  password: string,
  email: string
}

OUT:
200 OK          | {“users” : [User]}
400 Bad Request | {error: “msg”}
```

```
GET /users/get_teams/<username>
IN: username as a parameter, user must be authenticated

OUT:
200 OK        | {“teams”: [string]}
400 Bad Request    | {error: “msg”}
```

```
GET /users/confirm/<token>
IN: token from invitation link as a parameter
OUT:
200 OK        | {“confirmation”: “OK”}
400 Bad Request    | {“confirmation”: “Error”}
```



```
GET /teams/confirm_team/<token>
IN: token as a parameter

OUT:
200 OK        | {“confirmation”: “OK”}
200 OK        | {“confirmation”: “Already confirmed”}
```

```
POST /teams/create_team/ or /teams/create_team_fast/
IN:
{
  name: string,
  owner: string,
  members: list[string]
}

OUT:
200 OK        | {“confirmation”: “OK”}
400 Bad Request    | {error: “msg”}
```

```
GET /teams/get_members/<team_name>
IN: team name as parameter, user must be authenticated

OUT:
200 OK        | {“members”: [string],
   “invited”: [string}
400 Bad Request    | {error: “msg”}
```

```
POST /templates/create/
IN:
{
  owner: string,
  title: string,
  questions: [questions]
}

OUT:
200 OK        | {“confirmation”: “OK”}
400 Bad Request    | {error: “msg”}
```

```
POST /templates/assign/
IN: user must be authenticated
{
  title: string, (title of new form!)
  team: string,
  owner: string,
  template_title: string,
  deadline: string, format %Y-%m-%d %H:%M:%S.%f
  notification_details: list[NotificationDetails]
}

OUT:
200 OK        | {“confirmation”: “OK”}
400 Bad Request     | {error: “msg”}
```

```
GET /templates/get_templates/<username>
IN: user must be authenticated
OUT:
200 OK        | {“templates”: list[Templates]}
400 Bad Request    | {error: “msg”}
```
```
POST /forms/fill
IN: user must be authenticated
{
  form_id: string,
  recipient: string,
  answers: list[int|string|list(int)]
}

OUT:
200 OK        | {“confirmation”: “OK”}
400 Bad Request    | {error: “msg”}
```
```
GET /forms/results/<results_id>/
IN: user must be authenticated
OUT:
200 OK        | {“results”: {
                “_id”: ObjectId,
                “owner”: string,
                “send_date”: string,
                “deadline”: string,
                “not_filled_yet”: list[string],
                “questions”: list[{
“type”: string,
“title”: string}],
                “answers”: list[{
“username”: string,
“answers”: list[int|string|list(int)]}]
}}
400 Bad Request    | {error: “msg”}
```


```
GET /forms/owned/<username>/
IN: user must be authenticated
OUT:
200 OK        | {“forms”: list[results]}
400 Bad Request    | {error: “msg”}

Autoryzowane zapytania
‘Authorization’: token
```

```
GET /messages/<username>/
IN: user must be authenticated
OUT:
200 OK        | {“messages”: list[Message]}
400 Bad Request    | {error: “msg”}
```

```
POST /messages/mark_as_viewed/
IN: user must be authenticated
{
  owner: string,
  ids: list[ObjectId]
}

OUT:
200 OK        | {“confirmation”: “OK”}
400 Bad Request    | {error: “msg”}
```
```
GET /push/get_public_key/
IN: user must be authenticated
OUT:
200 OK        | {“public_key”: string}
400 Bad Request    | {error: msg}
```

```
POST /push/subscribe/
IN: user must be authenticated
{
  username: string,
  user_agent: string,
  subscription_info: dict
}
OUT:
200 OK        | {“confirmation”: “OK”}
400 Bad Request    | {error: msg}

```
