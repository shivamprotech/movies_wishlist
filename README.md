# Movie Wishlist

Movie wishlist is an small application for keeping the track of your movies.

## Features

- Search for Movies.
- Check details of Movies.
- Add movies in Wishlist.
- Remove movies from Wishlist 

### Pre-requirements
These services must be installed, configured and running:

- MongoDB
- Python (>= 3.8)

To use movie wishlist, create an API KEY of OMDB: http://www.omdbapi.com/apikey.aspx
and set it as ENV API_KEY=<your_api_key>

## Installation

### Run Movie Wishlist locally using Docker

Clone the git repo and then switch to movies_wishlist folder
```
cd movies_wishlist
docker-compose build
docker-compose up
```

This will start movie wishlist on http://localhost:5000 or http://127.0.0.1:5000
