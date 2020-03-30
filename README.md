# Zendesk Code Challenge - "Zearch"

## Overview

I deliberated a little on which approach to take on this challenge. If it were a real-world project I'd be reaching for elastic-search, or finding another full-text indexing library. Often with these things, it starts out with simple requirements and then quickly devolves. After chatting with tyler though my understanding is that the people grading the challenge want to see some thought in the algorithmic-complexity at play, and so I've decided to just stay simple and write a simple indexer from scratch

The Zearch class is backed by a Database which loads each object into an internally indexed representation enabling efficient searching. Essentially I've done a poor-mans full-index by creating a dict of each value in the table for that field, with a list of objects as the values. The indexes themselves do take space, however I've tried to be memory efficient by creating only one object which is re-indexed ( and re-referenced ) multiple times. The use of dict indexes in this way, should enable an O(1) search ( Hashtable ), with O(n*a) (number of documents * number of attributes) index build


I havn't done any pre-processing of the associations, instead opting to allow the user to determine if they want associated records returned or not. Adding the associated records results in many searches on the indexes, however unless the result count is very high, I dont think the user will notice much of a speed drop

## How to run

### Docker Environment

In order to boot into the docker environment run

```bash
docker-compose run app
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

I've used Pytest to do the testing. To run the tests, boot into the docker env and type

```
pytest
```

## Further Discussion

#### Factory Methods or Factory Objects
This morning I chose to use factory methods on the Database and IndexedTables rather than opting for a DatabaseFactory class. These sorts of choices are debatable, however in this case, if I were to do this again I would choose a DatabaseFactory object to read from the files and construct the db. The testing would have been slightly easier and I think the code would have been easier to read

#### Testing of a modal CLI
That was an interesting challenge. Usually with my clis I tend to be a little more simplistic and stick with argparse, which makes for a much easier to test application ( spin up a process, provide the options, capture the output). Given the example though, I decided to give the modal CLI a try. I'm not 100% happy with the level it tests at, but the Zearch integration test does a decent job of covering 98% of the application I think. It just doesnt test the integration with PyInquirer.. i'd much rather it did that too. 

In order to do that though, I'd need to spin up a seperate process and push keyboard commands through to it. That would take more digging than I'm wanting to dedicate to this project. For a production system it would be worth looking into, or double checking that we want a model GUI :)

#### Complex config as Dicts, vs a nice DSL
I've used a schema definition described in dicts in the config. It turned out reasonably complex, and the issue with this is that it puts it back on the users definiing these schemas to get it right, and doesnt help them do it. I'd prefer to create a nice DSL for crafting these schemas, so that settings cant be misspelled etc without nice errors coming back. For this submission thugh, I think the dicts are fine

#### Integration testing vs Unit Testing
Ahhhh! the old connundrum, and I found myself deliberating here as well. Not everything here is unit tested, some methods, I have opted to test via localised integration tests as the mocking was getting pretty onerous. In general, this is a sign that the modelling could be better (see DatabaseFactory vs factory methods above). I've spent enough time though, so I think i'll leave it as is. I'd be interested to see how others have modelled it

While I'm chatting about integration vs unit: There is a tradeoff between too much unit testing making the code resistent to change, and too little unit testing making the tests take ages to run, and the errors untraceable. I like to skate that line. Happy to chat this through

#### Testing Interfaces
I'm of the opinion that the exact wording etc of UIs should be able to change without test modification. You dont want to make it hard to change things, just be assured that the functionality you're expecting is there. Therefore my UI tests try to test at that level. I think their appropriate
