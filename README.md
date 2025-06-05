# Daylift Prototype

Dieses Repository enthält ein einfaches Python-Skript `task_manager.py`, mit dem Aufgaben über die Kommandozeile verwaltet werden können. Eine Aufgabe wird per Texteingabe erfasst, an die OpenAI-API gesendet und der geschätzte Aufwand in einer SQLite-Datenbank gespeichert.

## Voraussetzungen

- Python 3.9 oder neuer
- Abhängigkeiten installieren:
  ```bash
  pip install openai
  ```
- Die Umgebungsvariable `OPENAI_API_KEY` muss gesetzt sein.

## Nutzung

Das Skript kann direkt ausgeführt werden:

```bash
python task_manager.py
```

Nach Eingabe einer Aufgabenbeschreibung werden ähnliche Einträge aus der Datenbank angezeigt und der Aufwandsschätzung von OpenAI ausgegeben. Anschließend wird die Aufgabe gespeichert.

Die gespeicherten Aufgaben werden in der Datei `tasks.db` angelegt.
