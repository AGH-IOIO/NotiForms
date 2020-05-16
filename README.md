# NotiForms
[![Build Status](https://travis-ci.com/AGH-IOIO/NotiForms.svg?branch=master)](https://travis-ci.com/AGH-IOIO/NotiForms)

## Running
  #+begin_src bash
  docker-compose up
  #+end_src

## Testing
   #+begin_src bash
   TEST=y docker-compose up --abort-on-container-exit
   #+end_src

## Port mappings
| Service | Description | Container port | Local port |
|---------+-------------+----------------+------------|
| Flask   | Backend     |           8080 |       8080 |
| nginx   | Frontend    |             80 |       8081 |
| mongo   | Database    |          27017 |      27017 |
