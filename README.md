# Zendesk Code Challenge - "Zearch"

## Overview

This code challenge aims to test the coders knowledge of algorithms and general coding practices. If this were a real-world situation I would reach for elastic-search or postgres full-text indexing as the indexing engine, as there is no real need to roll your own. However given the constraints of the excercise, I have written a simple indexer from scratch.

The Zearch class is backed by a Database which loads each object into an internally indexed representation enabling efficient searching. Essentially I've done a poor-mans full-index by creating a dict of each value in the table for that field, with a list of objects as the values. The indexes themselves do take space, however I've tried to be memory efficient by creating only one object which is re-indexed ( and re-referenced ) multiple times. The use of dict indexes in this way, should enable an O(1) search ( Hashtable ), with O(n*a) (number of documents * number of attributes) index build


I havn't done any pre-processing of the associations, instead opting to allow the user to determine if they want associatd records returned or not. This choice results in many searches in the indexes, however unless the result count is very high, I dont think the user will notice

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

#### Factory Methods or Factory Objects
This morning I chose to use factory methods on the Database and IndexedTables rather than opting for a DatabaseFactory class. These sorts of choices are debatable, however in this case, if I were to do this again I would choose a DatabaseFactory object to read from the files and construct the db. The testing would have been slightly easier and I think the code would have been easier to read

#### Testing of a modal CLI
That was an interesting challenge. Usually with my clis I tend to be a little more simplistic and stick with argparse, which makes for a much easier to test application ( spin up a process, provide the options, capture the output). Given the example though, I decided to give the modal CLI a try. I'm not 100% happy with the level it tests at, but the Zearch integration test does a decent job of covering 98% of the application I think. It just doesnt test the intergration with PyInquirer.. i'd much rather it did that too

#### Complex config as Dicts, vs a nice DSL
I've used a schema definition described in dicts in the config. It turned out reasonably complex, and the issue with this is that it puts it back on the users definiing these schemas to get it right, and doesnt help them do it. I'd prefer to create a nice DSL for crafting these schemas, so that settings cant be misspelled etc without nice errors coming back. For this submission thugh, I think the dicts are fine

#### Integration testing vs Unit Testing
Ahhhh! the old connundrum, and I found myself deliberating here as well. Not everything here is unit tested, some methods, I have opted to test via localised integration tests as the mocking was getting pretty onerous. In general, this is a sign that the modelling could be better (see DatabaseFactory vs factory methods above). I've spent enough time though, so I think i'll leave it as is. I'd be interested to see how others have modelled it

While I'm chatting about integration vs unit: There is a tradeoff between too much unit testing making the code resistent to change, and too little unit testing making the tests take ages to run, and the errors untraceable. I like to skate that line. Happy to chat this through