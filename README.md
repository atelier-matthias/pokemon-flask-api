# pokemon-flask-api

## Description

This api allow to create Pokemons by name, and save it in local database. Rest of Pokemons data is taken from external PokeApi.
When Pokemon is created Api allow to create encounter for this Pokemon.


### Server
For server is used Flask framework. 

### Databases - MongoDB, Redis
Main database is MongoDB, but there is also Redis used for external Pokemons data. 

## Launch

### On local server
You need python3.x to run this app.  
`Mongo` - Required launched on standard `localhost:27017`  
`Redis` - Required launched on standard `localhost:6379`

Go to `/src folder`  
`$ pip3 install -r requirements.txt`  
`python3 app.py -c develop`

`-c` parameter is for config. Available options: `develop`, `testing`, `staging`, `production`
If You dont want to use `-c` parameter, You can use system variable `ENVIRONMENT` as same as `-c` parameter   

### By Docker
`Docker` and `docker-compose` Required
Just go to `/pokemon-flask-api` folder and run:
  
`$ docker-compose up`
* `mongo` should up
* `redis` should up
* `test_1` should run
* `server` if everything goes right, `server` is up
* if everything is right application is available on `localhost:8989`

DOCKER IMPORTANT NOTE - Application uses PORT:
* `27017`
* `6379`
* `8989`

Remember not to use it on Your localhost when You start by docker.

## Pokemons List

### HTTP Request

`GET http://BASE_URL/pokemons`  

> JSON RESPONSE BODY  
>OK Response

```json
{
  "pokemons": [
    {
      "baseExperience": 62,
      "createdAt": "Sat, 04 Apr 2020 12:17:20 GMT",
      "height": 6,
      "id": "ebab82a1-ac80-4b15-93b8-2a0fe7ab1551",
      "name": "charmander",
      "sprites": {
        "backDefault": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/4.png",
        "backFemale": null,
        "backShiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/4.png",
        "backShinyFemale": null,
        "frontDefault": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
        "frontFemale": null,
        "frontShiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/4.png",
        "frontShinyFemale": null
      },
      "weight": 85
    },
    {
      "baseExperience": 64,
      "createdAt": "Sat, 04 Apr 2020 12:26:33 GMT",
      "height": 7,
      "id": "d712a641-3ec5-436c-8da7-0ad4506c6381",
      "name": "bulbasaur",
      "sprites": {
        "backDefault": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
        "backFemale": null,
        "backShiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/1.png",
        "backShinyFemale": null,
        "frontDefault": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        "frontFemale": null,
        "frontShiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png",
        "frontShinyFemale": null
      },
      "weight": 69
    }
  ],
  "status": "OK",
  "totalCount": 2
}
```

### Query Parameters


Filter | Type | Required | Description  
--------- | ----------- | -----------  | -------
name | string | False |  filtering by `name` field include filtering contains value
sort | string | False | sort parameter. Accepted values `name`, `createdAt`. Default sort is `createdAt`
order | string | False | sorting order. Accepted values `asc` and `desc`. Default `asc`
limit | number | False | set limit results per page. Default `limit=25`. Max value per page `limit=50`
page | number | False | show page number. Default value `page=0`


## Create Pokemon

### HTTP Request

`POST http://BASE_URL/pokemons`  

> JSON REQUEST BODY

```json
{
  "name": "charmander"
}
```


Field | Type | Required | Description  
--------- | ----------- | -----------  | -------
name | string | True |  Pokemon name


> JSON RESPONSE BODY  
> OK Response

```json
{
  "pokemons": {
      "baseExperience": 62,
      "createdAt": "Sat, 04 Apr 2020 12:17:20 GMT",
      "height": 6,
      "id": "ebab82a1-ac80-4b15-93b8-2a0fe7ab1551",
      "name": "charmander",
      "sprites": {
        "backDefault": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/4.png",
        "backFemale": null,
        "backShiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/4.png",
        "backShinyFemale": null,
        "frontDefault": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
        "frontFemale": null,
        "frontShiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/4.png",
        "frontShinyFemale": null
      },
      "weight": 85
    },
  "status": "OK"
}
```

### Errors


Error Type | Code |  Description  
--------- | -----------   | -------
Conflict | 400 | Validation Error - read response details
NotFound | 404 | Pokemon Not Found
Internal Server Error | 500 | Check Response Details. Probably external pokemon api server not response


## Encounters List

### HTTP Request

`GET http://BASE_URL/pokemons/:POKEMON_UUID/encounter`  

Parameter | Type | Required | Description  
--------- | ----------- | -----------  | -------
POKEMON_UUID | uuid | True |  Pokemon id.

> JSON RESPONSE BODY  
>OK Response

```json
{
  "encounters": [
    {
      "id": "a9098f01-d475-4518-b789-95437bcfcb57",
      "note": null,
      "place": "forrest",
      "timestamp": 1586102806
    }
  ],
  "status": "OK",
  "totalCount": 1
}
```

### Query Parameters

Filter | Type | Required | Description  
--------- | ----------- | -----------  | -------
note | string | False |  filtering by `note` field include filtering contains value
place | string | False |  filtering by `place` field include filtering contains value
sort | string | False | sort parameter. Accepted values `place`, `timestamp`. Default sort is `timestamp`
order | string | False | sorting order. Accepted values `asc` and `desc`. Default `asc`
limit | number | False | set limit results per page. Default `limit=25`. Max value per page `limit=50`
page | number | False | show page number. Default value `page=0`


## Create Pokemon

### HTTP Request

`POST http://BASE_URL/pokemons`  

> JSON REQUEST BODY

```json
{
  "place": "forrest",
  "note": "some encounter note"
}
```


Field | Type | Required | Description  
--------- | ----------- | -----------  | -------
place | string | True |  Encounter Place
note | string | False |  Encounter note


> JSON RESPONSE BODY  
> OK Response

```json
{
  "encounter": {
    "id": "619dd62b-f549-4d6e-9fd2-dacfbedf6f5a",
    "note": null,
    "place": "forrest",
    "timestamp": 1586102973
  },
  "status": "OK"
}
```

### Errors


Error Type | Code |  Description  
--------- | -----------   | -------
Conflict | 400 | Validation Error - read response details
NotFound | 404 | Pokemon Not Found

