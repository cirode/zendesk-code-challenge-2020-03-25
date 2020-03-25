# Zendesk Code Challenge - "Zearch"

## Overview

This code challenge aims to test the coders knowledge of algorithms and general coding practices. If this were a real-world situation I would reach for elastic-search or postgres full-text indexing as the indexing engine, as there is no real need to roll your own. However given the constraints of the excercise, I have done so.

The Zearch class is backed by a Database which loads each object into an internally indexed representation enabling efficient searching. Essentially I've done a poor-mans full-index by creating a dict of each value in the table for that field, with a list of objects as the values. The indexes themselves do take space, however I've tried to be memory efficient by creating only one object which is re-indexed ( and re-referenced ) multiple times. The use of dict indexes in this way, should enable an O(1) search ( Hashtable ), with O(n*a) (number of documents * number of attributes) index build


## How to run

### Docker Environment

A docker envrionment is included in this code submission. Docker must be installed in order to utlise this ( https://www.docker.com/products/docker-desktop, or your favourite package manager )

In order to boot into the environment run

```bash
docker-compose run --rm app
```

This will boot you into bash, ensuring the correct pathing and libs are installed ( via poetry ).
`NOTE: It takes a moment to install the libs into the docker container on boot. Please be patient here :)`

Once in the environment, the repository on your local files sytem will be available to you mounted under "/application"


### Zearch

To run the "zearch" application simply provide a directory of json files to the 'zearch' command

For example: to use the data given as part of the excercise

```
zearch --file_dir specs/sample_files
```

`NOTE: Zearch indexes the files at startup. There may be slight delay before given the prompts depending on how large the files are`

### Tests

I've used Pytest to do the testing. To run them, boot into the docker env and type

```
pytest
```

## Further Discussion

#### Factory Methods or factory Objects
This morning I chose to use factory methods on the Database and IndexedTables rather than opting for a DatabaseFactory class. These sorts of choices are debatable, however in this case, if I were to do this again I would choose a DatabaseFactory object to read from the files and construct the db. The testing would have been slightly easier and I think the code would have been easier to read

#### Testing of a modal CLI
That was an interesting challenge. Usually with my clis I tend to be a little more simplistic and stick with argparse, which makes for a much easier to test application ( spin up a process, provide the options, capture the output). Given the example though, I decided to give the modal CLI a try. I'm not 100% happy with the level it tests at, but the Zearch integration test does a decent job of covering 98% of the application I think