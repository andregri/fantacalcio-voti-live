```
python3 scraper.py --squadra "Milan" --giornata 24 --until "20:00"
```

```
sudo docker run --rm -d --name fantacalcio_db -v $(pwd)/var/fantacalcio_pgdata:/var/lib/postgresql/data -e POSTGRES_USER=fantallenatore -e POSTGRES_PASSWORD=password -e POSTGRES_DB=fantacalcio_db -p 5432:5432 postgres
```

## ToDo
- [ ] insert in db only if any field is different from last inserted one.
  Probably you need to store a dictionary (key: player id, value: voto + eventi)
- deploy
  - [ ] supervisord
  - [ ] nginx
