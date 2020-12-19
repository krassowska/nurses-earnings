# nurses-earnings
Earnings among Polish nurses.


# Virtual environment
To activate this environment, use
```bash
conda activate nurses-earnings
```
To deactivate an active environment, use
```bash
conda deactivate
```

# Install requirements.txt
```bash
conda install --file requirements.txt
```

# Python version
Python 3.8.2

# Run Flask application
## Ubuntu
```bash
cd website
export FLASK_APP=app.py
flask run
```
## Windows - PowerShell

```bash
cd website
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"  # trigger reloader on file changes
flask run
```

# Resources
- Maps of Poland with voivodeships and counties in geojson format: https://github.com/ppatrzyk/polska-geojson
- Table with information about powiats: [Source: Wikipedia -> "Lista powiatów w Polsce" accessed on 02/09/2020](https://pl.wikipedia.org/wiki/Lista_powiat%C3%B3w_w_Polsce#Lista_powiat%C3%B3w_w_Polsce), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.pl)

# Database
## Add the postgresql bin directory path to the path environment variable
[Configuring postreSQL PATH variable on Windows 7](https://stackoverflow.com/questions/11460823/setting-windows-path-for-postgres-tools)

## Create database
```bash
psql --username=postgres -f db.sql
```

## Add new table to database
```bash
psql --username=postgres -d nurses_earnings_db -f tables.sql
```
