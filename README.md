# watson Coat of Arms

## Setup

1. Install the required packages
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the `config.example.py` to `config.py` and adjust the settings
3. Run the script
   ```bash
   python import.py
   ```

## Frontend

### URL

```
<TARGET_PATH>/coa/gde/{{ bfs_nr }}.png
```

### Datawrapper Title

```
<img src="<TARGET_PATH>/coa/gde/{{ bfs_nr }}.png" width="30" height="35" align="center"> <b>{{ gde_name }}</b>
```
