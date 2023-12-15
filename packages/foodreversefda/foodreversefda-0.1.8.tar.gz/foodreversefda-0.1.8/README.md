# foodreversefda

This API client package provides some basic search functionalities on FDA's open api.

## Description

All following functions generate accordingly json file containing FDA food reverse events.

## Getting Started

### Dependencies

* python = "^3.10"
* requests = "^2.31.0"
* vcrpy = "^5.1.0"
* pytest = "^7.3.1"

### Installing

* pip install foodreversefda

### Executing program

Functions include:
* id_get()
* date_get()
* class_get()
* city_get()

First, pass parameters to Class, then call function inside Class. 
Classes include:
* ID
* Date
* Classification
* City

```
#Example for id_get()
import foodreversefda

id_instance = ID["000000", "111111"] 
info = id_instance.id_get()
# "000000" and "111111" are placeholders for actual 'event_id'
# You can search for multiple 'event_id's
```

## Author

Yifei Chen  
yc4307@columbia.edu

## License

MIT
