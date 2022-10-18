# IMDB analyse de sentiment


## Installation

Suivre les indications ci-dessous :

```bash
git clone https://github.com/Simplon-Martin/imdb_analyse_sentiment_v2.git
cd imdb_analyse_sentiment_v2/
```

Créer une BDD Mysql :
```sql
CREATE DATABASE  IF NOT EXISTS `imdb_v2` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ /*!80016 DEFAULT ENCRYPTION='N' */;
```

Config environement :

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

Ensuite : 

```bash
pip install -r requirements.txt
```

## Configuration

Configuration
Ouvrir le fichier exemple_config.yml et remplacer les valeurs par défaut par celle de votre environnement. Copier ensuite ce fichier dans un dossier instance et le renommer config.yml.

```bash
mkdir instance
cp exemple_config.yml instance/config.yml
```

Générer le dossier "migrations" :
```bash
flask db init
```
Au besoin : 
```bash
flask db migrate
```
Création du script.sql et insertion des données : 
```bash
flask db upgrade
flask insert-db
```

Exécution
Pour lancer l'app, vous devrez taper la commande :

```bash
FLASK_APP=app.py
FLASK_ENV=development flask run --port 8080
```


## Contribution
Martin

## License

