# Zendesk Code Challenge - "Zearch"

## Overview

This is a basic search application. If this were a real-world situation I would immediately reach for elastic-search or postgres full-text indexing as the indexing engine, as there is no real need to roll your own. Seeing as how the code challenge was written to not get too deep into specifics of search indexing however (GIST,GIN,trigrams,etc), I decided to not go down the roll-your-own route

The Zearch class is backed by a Database which loads each object into an internal indexed representation enabling efficient searching. Essentially I've done a poor-mans full-index by creating a dict of each value in the table for that field, with a list of objects as the values. The indexes themselves do take space, however I've tried to be memory efficient by creating only one object which is re-indexed ( and re-referenced ) multiple times. The use of dict indexes in this way, should enable an O(1) search ( Hashtable ), with O(n) index build

An overview and reponsibility split of the objects is below
- **ZearchCLI**: Runs the user interface
- **ZearchCLI**: Runs the user interface


## How to run

A docker envrionment is included in this code submission. Docker must be installed in order to utlise this ( https://www.docker.com/products/docker-desktop, or your favourite package manager )

In order to boot into the environment run

```bash
docker-compose run --rm app
```

This will boot you into bash, ensuring the correct pathing and libs are installed

Once in the environment, the repository on your local files sytem will be available to you mounted under "/application"

To run the "zearch" application