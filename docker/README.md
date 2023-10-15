## Instructions

* Install docker
* Build docker image:

```
docker build --file Dockerfile --tag fantacalcio .
```
  
  Note: unnecessary once on the Hub

* Run docker image:

```
docker run fantacalcio <command>
```

* [optional] For development, run in interactive mode

```
docker run -it fantacalcio bash
```
