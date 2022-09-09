# ReplicaSet

## 학습 목표

1. ReplicaSet 오브젝트를 이용해 Pod를 생성할 수 있다.

- ReplicaSet 선언과 생성
- kubectl의 port forward기능을 통해 생성된 Pod으로 요청/응답 확인

2. ReplicaSet이 클러스터 상태에 따라 Pod수를 어떻게 관리하는지 이해할 수 있다.

- ReplicaSet으로 Pod를 생성하는 경우
- 기존에 생성한 Pod를 ReplicaSet으로 관리하려는 경우

## ReplicaSet이란

Pod 복제본을 생성하고 관리해주는 것으로,
이를 사용하면

- 더 이상 N개의 Pod를 생성하기 위해 생성 명령을 N번 실행할 필요가 없다.
- ReplicaSet 오브젝트를 정의하고 원하는 Pod의 개수를 replicas 속성으로 선언한다.
- 클러스터 관리자 대신 Pod 수가 부족하거나 넘치치 않게 딱 설정한 숫자 만큼의 Pod수를 조정해주기도 한다.

## Use case

참고) 소프트웨어 내결함성

- 소프트웨어나 하드웨어 실패가 발생하더라도 소프트웨어가 정상적인 기능을 수행할 수 있는 것.
- 그렇담 사람의 개입없이 내결함성을 가진 소프트웨어를 구성하는 것이 정말 중요하겠다.

Pod에 문제가 생겼을 때

- Pod는 즉시 종료되고 클라이언트 요청을 처리할 수 없어지며 복구 까지 down time이 생긴다. (No self-healing)
  그렇기 때문에 클러스터 관리자가 24/7 동안 Pod사애를 감시하고 정상 복구해야하는데
  N개의 Pod를 실행하고 상태 이상에 대한 대비는 어떻게 하는가?!

-> Pod와 node의 상태에 따라 Pod의 수를 조정할 수 있도록 사람이 아닌 ReplicaSet에게 역할을 위임할 수 있다.

- ReplicaSet을 이용해서 Pod 복제 및 복구 작업을 자동화
- 클러스터 관리자는 ReplicaSet을 만들어 필요한 Pod의 개수를 쿠버네티스에게 선언한다.
- 쿠버네티스가 ReplicaSet요청시에 선언된 replicas를 읽고 그 수만큼 Pod 실행을 보장.

## 선언

```yaml
apiVersion: apps/v1 # Kubernetes API 버전

kind: ReplicaSet # 오브젝트 타입

metadata: # 오브젝트를 유일하게 식별하기 위한 정보
  name: blue-app-rs # 오브젝트 이름
  labels: # 오브젝트 집합을 구할 때 사용할 라벨
    app: blue-app

spec: # 사용자가 원하는 Pod의 바람직한 상태
  selector: # ReplicaSet이 관리해야하는 Pod를 선택하기 위한 label query
    matchLabel: # 이 아래에 key=value로 Pod label query 작성
    # ex. app: blue-app # 이렇게 작성해주면 'app=blue-app 이라는 label을 가진' 모든 Pod를 관리해준다.
  replicas: # 실행하고자 하는 Pod 복제본 개수 선언 ex. 3
  template: # 내가 ReplicaSet을 통해 생성하고자 하는 Pod의 실행 정보: Pod template와 동일 (metadata, spec, ....)
    metadata:
      labels:
        # ReplicaSet selector에 정의한 label을 포함해야 한다. ex. app: blue-app
    spec:
      containers:
        - name: blue-app
          image: blue-app:1.0
```

## Quick start

1. ReplicaSet생성, 배포
2. ReplicaSet의 Pod생성 이벤트 확인
3. 생성된 Pod 목록과 배포 노트 확인
4. 포트포워딩을 통한 Pod 요청/응답 확인
   포트포워딩 host port 8080 -> container port 8080 (ReplicaSet에 의해 생성된 파드로 트래픽 전달)
   kubectl port-forward rs/blue-replicaset 8080:8080  
   이러면 replicaSet으로 생성된 pod에서 실행되고 있는 container port가 8080가 아니면 요청이 전달되지 않음.  
   그리고 첫번째로 생성된 pod로만 요청이 전달된다.  
   **즉, 로드밸런싱이 일어나지 않음** replicaSet은 pod 복제, 생성에만 역할이 있지, 로드밸런싱은 담당해주지 않는다.
