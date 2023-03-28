# Real Time Python Log Ingestion with Logstash & elk and Visualize Logs on Kibana

# Real Time Python Log Ingestion with Logstash & elk and Visualize Logs on Kibana
어느 페이지에 많이 머물고, 서비스를 많이 사용하는지 알 수 있을 것 같다. -> FE logging :)
BE: 웹서버 프레임워크는 요새 내가 애정하게 된 프레임워크인 flask를 사용 하려고 한다.
FE: 사용자가 보는 화면은 Vue로 만들려고한다.
DB: 데이터베이스는 MonogoDB를 사용하려고한다. 디비 구축에 너무 많은 시간을 안들여도 되고, 이벤트를 중심으로 데이터를 저장할 수 있는 장점이 있다.

## ELK
- ElasticSearch: 
  - 로깅과 로그 분석
  - 인프라 메트릭과 컨테이너 모니터링
  - 애플리케이션 성능 모니터링
- Logstash
  - Logstash는 데이터를 집계하고 처리해서 ElasticSearch로 전송하는데 사용되는 도구이다.
- Kibana
  - ElasticSearch의 데이터를 시각화 해주는 관리 도구이다. 실시간으로 반영되는 시각화 도구로 데이터의 흐름을 분석 할 수 있다.


logstash --version 
치니까. zsh: command not found: logstash 에러 떠서 venv 말고 docker에서 ELK 환경을 구축해보려고 한다. 

Set tup Docker ELK
https://github.com/deviantony/docker-elk.git 참고. 

1. 
```bash
git clone https://github.com/deviantony/docker-elk.git
```

2. 
```bash
cd docker-elk
```

3. 
```bash
docker-compose build && docker-compose up
```

4. 
```bash
docker ps

# output
# (venv) (base) grace@jeonghyeonjeong-ui-MacBookPro docker-elk % docker ps
# CONTAINER ID   IMAGE                      COMMAND                  CREATED         STATUS         PORTS                                                                                                NAMES
# 78cd109338cc   docker-elk_logstash        "/usr/local/bin/dock…"   5 seconds ago   Up 4 seconds   0.0.0.0:5044->5044/tcp, 0.0.0.0:9600->9600/tcp, 0.0.0.0:50000->50000/tcp, 0.0.0.0:50000->50000/udp   docker-elk_logstash_1
# 286b35a01074   docker-elk_kibana          "/bin/tini -- /usr/l…"   5 seconds ago   Up 4 seconds   0.0.0.0:5601->5601/tcp                                                                               docker-elk_kibana_1
# 9f0b193e47a7   docker-elk_elasticsearch   "/bin/tini -- /usr/l…"   6 seconds ago   Up 5 seconds   0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   
```
즉, 
docker ps 로 확인 해 보았을 때 각각의 port는 다음과 같다

Elastic Search : 9200, 9300
Logstash : 5044, 9600, 50000
Kibana : 5601

6. 
docker-compose.yml파일과 각 config파일을 확인해보자

아래의 docker-compose.yml 파일을 보면, 각각 service들의 config파일들의 설정을 가져와서 설정한다.

Elastic Search : /elasticsearch/config/elasticsearch.yml
Logstash : /logstash/config/logstash.yml
Kibana : /kibana/config/kibana.yml

7. Logstash의 설정
flask의 로그를 받는 것은 ELK스택 중, Logstash 이다.
Logstash —> Elastic Search —> Kibana(조회/분석) 
그렇기 때문에 Logstash의 설정이 중요하다.
```conf
input {
	beats {
		port => 5044
	}

	tcp {
		port => 50000
	}
}

## Add your filters / logstash plugins configuration here

output {
	elasticsearch {
		hosts => "elasticsearch:9200"
		user => "logstash_internal"
		password => "${LOGSTASH_INTERNAL_PASSWORD}"
		index => "dxc-elk-logger"
	}
}
```

8. Activate venv
```bash
python3 -m venv venv && source ./venv/bin/activate
```

9. Install packages for flask app. 
```bash
pip install -r requirements.txt
```

9. Start flask app
```bash
python app.py
```

10. Check log in Kibana
Go http://localhost:5601/
Username: elastic
Password: changeme
as default

---


1. Activate venv
```bash
python3 -m venv venv && source ./venv/bin/activate
```

2. Install python-logstash

```bash
pip install python-logstash
```

3. Setting the logstash congif
```conf
# sample.conf
# TODO: config option에 대해서 좀 더 알아보기. 
input {
  udp {
    port => 5959
    codec => json {
          target => "[document]"
        }
  }
}
output {
  stdout { # which means 'I'm gonna see the logs from the document'
    codec => rubydebug
  }
  elasticsearch { # which means 'I'm gonna send the logs to the elasticsearch'
		hosts => ["http://localhost:9200"]
		index => "logdb"
  }
}
```

4. Start logstash with config file
```bash
logstash -f ./sample.conf --config.reload.automatic
# --config.reload.automatic: anytime changing the configuration, it reload automatically.
```

# 여기까지 하고 
logstash --version 
치니까. zsh: command not found: logstash 에러 떠서 venv 말고 docker에서 ELK 환경을 구축해보려고 한다. 

Set tup Docker ELK
https://github.com/deviantony/docker-elk.git 참고. 

1. 
```bash
git clone https://github.com/deviantony/docker-elk.git
```

2. 
```bash
cd docker-elk
```

3. 
```bash
docker-compose build && docker-compose up
```

4. 
```bash
docker ps

# output
# (venv) (base) grace@jeonghyeonjeong-ui-MacBookPro docker-elk % docker ps
# CONTAINER ID   IMAGE                      COMMAND                  CREATED         STATUS         PORTS                                                                                                NAMES
# 78cd109338cc   docker-elk_logstash        "/usr/local/bin/dock…"   5 seconds ago   Up 4 seconds   0.0.0.0:5044->5044/tcp, 0.0.0.0:9600->9600/tcp, 0.0.0.0:50000->50000/tcp, 0.0.0.0:50000->50000/udp   docker-elk_logstash_1
# 286b35a01074   docker-elk_kibana          "/bin/tini -- /usr/l…"   5 seconds ago   Up 4 seconds   0.0.0.0:5601->5601/tcp                                                                               docker-elk_kibana_1
# 9f0b193e47a7   docker-elk_elasticsearch   "/bin/tini -- /usr/l…"   6 seconds ago   Up 5 seconds   0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   
```
즉, 
docker ps 로 확인 해 보았을 때 각각의 port는 다음과 같다

Elastic Search : 9200, 9300
Logstash : 5044, 9600, 50000
Kibana : 5601

6. 
docker-compose.yml파일과 각 config파일을 확인해보자

아래의 docker-compose.yml 파일을 보면, 각각 service들의 config파일들의 설정을 가져와서 설정한다.

Elastic Search : /elasticsearch/config/elasticsearch.yml
Logstash : /logstash/config/logstash.yml
Kibana : /kibana/config/kibana.yml

7. Logstash의 설정
flask의 로그를 받는 것은 ELK스택 중, Logstash 이다.
Logstash —> Elastic Search —> Kibana(조회/분석) 
그렇기 때문에 Logstash의 설정이 중요하다.
```conf
input {
	beats {
		port => 5044
	}

	tcp {
		port => 50000
	}
}

## Add your filters / logstash plugins configuration here

output {
	elasticsearch {
		hosts => "elasticsearch:9200"
		user => "logstash_internal"
		password => "${LOGSTASH_INTERNAL_PASSWORD}"
		index => "dxc-elk-logger"
	}
}
```

8. Activate venv
```bash
python3 -m venv venv && source ./venv/bin/activate
```

9. Install packages for flask app. 
```bash
pip install -r requirements.txt
```

9. Start flask app
```bash
python app.py
```

10. Check log in Kibana
Go http://localhost:5601/
Username: elastic
Password: changeme
as defaul