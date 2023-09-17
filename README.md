```
python3 scraper.py "Empoli" "Cagliari" "Udinese" "Verona" "Genoa" "Salernitana" --giornata 25 --until "17:00"
```

```
sudo docker run --rm -d --name fantacalcio_db -v $(pwd)/var/fantacalcio_pgdata:/var/lib/postgresql/data -e POSTGRES_USER=fantallenatore -e POSTGRES_PASSWORD=password -e POSTGRES_DB=fantacalcio_db -p 5432:5432 postgres
```

```
25 18 * * * /home/andrea/Documents/progetto_python/fantacalcio-voti-live/scraper.sh > ~/fantacalcio_18.log
```

## ToDo
- [x] insert in db only if any field is different from last inserted one.
  Probably you need to store a dictionary (key: player id, value: voto + eventi)
- [x] deploy on heroku
- [ ] run scraper with supervisord

## Take Home
- Docker volumes to store db
- plotly and dash to make dashboards
  - callback chains for dropdowns
  - live updates of plots
- PostgreSQL and pgadmin
  - handling strings with quotes
  - timestamp type
  - `ON CONFLICT DO NOTHING` for insertion
  - `SELECT DISTINCT ON` for query unique values
- Python
  - implement `__eq__` for comparing objects
