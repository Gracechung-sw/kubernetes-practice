# flask logging using ELK on Docker

### 1. git clone ELK docker config files.
```bash
git clone https://github.com/deviantony/docker-elk.git
```

### 2. Start ELK
```bash
cd docker-elk
docker-compose build && docker-compose up
```

### 3. Activate virtual env

```bash
cd flask-app
python3 -m venv venv && source ./venv/bin/activate
```

### 4. Install requirements

```bash
pip install -r requirements.txt
```

## 3. Start flask sample app
```bash
flask run
```
