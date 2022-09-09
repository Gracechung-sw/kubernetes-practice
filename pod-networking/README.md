# Pod 끼리 Pod IP로 통신, Pod 안에서 localhost로 통신하기

## 1. Pod 안에 서로 다른 컨테이너끼리 localhost로 통신하는 방법

- 하나의 Pod에 서로 다른 port로 컨테이너 2개를 선언하면 된다.

## 2. 서로 다른 Pod끼리 Pod IP로 통신하는 방법

- Pod A에 있는 컨테이너 -> Pod B에 있는 컨테이너로 요청 전송/ 응답 확인

## 사용하는 명렁어

1. Pod 생성

```
kubectl apply -f <yaml 파일 경로>
```

2. Pod 실행 및 IP 확인

```
kubectl get pod -o wide
```

3. Pod 종료

```
kubectl delete pod --all
or
kubectl delete pod <pod-name>
```

4. Pod 간 통신  
   -c: 어떤 컨테이너에서 해당 명령어를 실행시킬지 지정

```
kubectl exec <pod name> -c <container name> -- curl -s <pod ip>:<container port>
```

5. 컨테이너 로그 출력

```
kubectl logs <pod name> <container name>
```

6. 컨테이너 IP 확인

```
kubectl exec <pod name> -c <container name> -- ifconfig eth0
```

7. 컨테이너 환경변수 확인

```
kubectl exec <pod name> -- printenv
```

8. 포트 포워딩

```
kubectl port-forward <pod name> <host port>:<container port>
```
