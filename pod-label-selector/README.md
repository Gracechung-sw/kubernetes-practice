# 개념

## label

쿠버네티스 오브젝트를 식별하기 위한 key/value 쌍의 메타정보.
쉽게 말해 쿠버네티스 리소스를 논리적인 그룹으로 나누기 위해 붙이는 이름표.

## Selector

Label을 이용해서 쿠버네티스 리소스를 필터링하고 원하는 리소스 집합을 구하기 위한 label query.
쉽게 말해 label을 이요해서 쿠버네티스 리소스를 선택하는 방법.

그래서 label과 selector의 관계를 정리해보면,

사용자나 쿠버네티스 내부에서 특정한 리소스 집합을 구하기 위해 label query인 selector로 명령을 날리면

쿠버네티스는 이를 통해 리소스 조회를 한 뒤 리턴한다.

# Use case

1.  클러스터에서 서로 다른 팀의 수백개 Pod이 동시에 실행되고 있는 상황에서

주문 트래픽을 주문 Pod으로만 리다이렉트 하고 싶다면?

주문 Pod을 식별할 수 있어야 한다.

배달 트래픽을 배달 Pod으로만 리다이렉트 하고 싶다면?

배달 Pod을 식별할 수 있어야 한다.

\-> 이 때 label을 이용할 수 있다.

2.  음식 배달만 하느 서비스에 꽃 배달 기능을 추가하였다고 하자.

트래픽이 증가할 것이기 때문에 클러스터에서 실행 중인 배달 관련 pod들을 수평 확장해야 한다면?

배달 Pod을 식별할 수 있어야 한다. 그래야 그것만 골라서 수평 확장 할 수 있으니까.

\-> 이 때 label을 이용할 수 있다.

# Label과 Selector 표현 방법과 명령어 사용법

## label의 표현 방법

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: my-pod
    labels: # 이제 my-pod라는 Pod는 이 아래 3개의 key:value로 특정 지어질 수 있다.
    	app: backend
        version: v1
        env: pod
spec:
	containers:
    	- image: my-pod
          name: my-pod
```

## label 관련 명령어

1. 이렇게 label을 설정한 pod를 배포해두었을 때 kubectl 명령어로 label 정보 조회 방법

```bash
$ kubectl get pod <pod name> --show-labels
or 원하는 lable만 보고자 한다면
$ kubectl get pod/<pod name> --label-columns <label key1>,<label key2>...
```

2. label 추가

```bash
$ kubectl label pod <pod name> <key>=<value>
```

3. label 수정

```bash
$ kubectl label pod <pod name> <key>=<value> --overwrite
```

4. label 삭제

```bash
$ kubectl label pod/<pod name> <key>-
```

## selector의 표현 방법

kubectl get 명령어와 함께 Selector를 사용하는 방법

```bash
$ kubectl get <object type> --selector <label query 1, ..., label query N>

or

$ kubectl get <object type> -l <label query 1, ..., label query N>
```

selector의 연산자

1. 같다(=) key=value
2. 같지 않다(!=) key!=value
