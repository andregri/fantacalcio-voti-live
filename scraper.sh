#!/bin/bash
cd "/home/andrea/Documents/progetto_python/fantacalcio-voti-live"
source "venv/bin/activate"
python3 scraper.py "Sampdoria" "Empoli" --giornata 26 --until "17:00"
