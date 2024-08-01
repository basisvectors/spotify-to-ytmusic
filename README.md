# Moving from Spotify to YTMusic


```(¯`·._.··¸.-~*´¨¯¨`*·~-.𝓯𝓾𝓬𝓴 𝓼𝓹𝓸𝓽𝓲𝓯𝔂 𝓪𝓷𝓭 𝓯𝓾𝓬𝓴 𝓭𝓪𝓷𝓲𝓮𝓵 𝓮𝓴.-~*´¨¯¨`*·~-.¸··._.·´¯)```

I already use youtube most of the time so it makes sense for me to move my listening history and library to youtube music instead.

#Usage

Request your data from spotify - listening history and extended listening history

Get the YourLibrary.json file from the Spotify data

Install the ytmusicapi library using pip

```bash
pip install ytmusicapi
```
Authenticate it with OAuth, follow the instructions in the terminal, itll open a browser window and ask you to login to your google account and save the credentials in a file, the file is valid for 20hrs
```bash
ytmusicapi oauth
```

Read the template code in SpotifyToYTMusic.ipynb notebook and customize according to your needs

#TODO

add scripts that convert entire playlists into YTMusic playlists and move all liked and followed artists to the YTMusic library.