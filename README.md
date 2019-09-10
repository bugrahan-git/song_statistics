# Dataset
I took all the data from [A-Z Lyrics](https://www.azlyrics.com/). Dataset includes 3 MySQL tables which are genres, artists and songs.

#### genres

| id INTEGER    | name VARCHAR(255)|
| ------------- |------------------|
| 1      | punk |
| 2      | rock |
| ... | ... |

#### artists

| id INTEGER| name VARCHAR(255)| genreId INTEGER|
| ----------|------------------|----------------|
|1| ramones|1|
|2|bonjovi|2|
|...|...|...|

#### songs

|name VARCHAR(255)|lyrics TEXT|artistId INTEGER|
|------------------|-----------|---------|
|Rockaway Beach| LYRICS...|1|
|Runaway| LYRICS...|2|
|...|...|...|

# Scraping
You must use [A-Z Lyrics](https://www.azlyrics.com/) naming convention while scraping.<br/>
<br/>
:x: The Clash<br/>
:heavy_check_mark: clash

:x: AC/DC<br/>
:heavy_check_mark: acdc

:x: Green Day<br/>
:heavy_check_mark: greenday

:x: beyonce<br/>
:heavy_check_mark: knowles

# Analysis

### Output
Analysis class produces two outputs:
#### 1. Pie Chart
Pie chart shows us the most used 10 words for a single artist or genre with their percentage.
<img src="https://user-images.githubusercontent.com/45638465/64608864-41160380-d3d4-11e9-8d2f-ca685fa6f70b.png" width="324">
<img src="https://user-images.githubusercontent.com/45638465/64609007-9baf5f80-d3d4-11e9-8d77-359d2b7847b4.png" width="324">
#### 2. Bar Chart
Bar chart shows us the most used 20 words for a single artist or genre with their number of usage.
<img src="https://user-images.githubusercontent.com/45638465/64609062-b2ee4d00-d3d4-11e9-99e0-3dd9f591beca.png" width="324">
<img src="https://user-images.githubusercontent.com/45638465/64609063-b386e380-d3d4-11e9-9608-68783f4c172f.png" width="324">
