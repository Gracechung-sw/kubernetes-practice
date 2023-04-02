# flask logging using ELK on Docker

### 1. git clone ELK docker config files.
(I already have in this repo.)
```bash
git clone https://github.com/deviantony/docker-elk.git
```

Change logstash.conf file
```json
input {
	tcp {
		port => 5044
	}
}

## Add your filters / logstash plugins configuration here

output {
	elasticsearch {
		hosts => "elasticsearch:9200"
		user => "elastic"
		password => "changeme"
		index => "deepdx-connect"
	}
}

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
source ./venv/bin/activate
flask run
```
