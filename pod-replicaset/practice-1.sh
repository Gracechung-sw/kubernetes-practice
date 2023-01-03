# ReplicaSet 생성
kubectl apply -f replicaset.yaml

# ReplicaSet과 Pod Template 확인
kubectl get rs blue-replicaset -o wide

# 생성된 Pod 목록과 배포된 노드 확인
kubectl get pod -o wide

# ReplicaSet의 Pod 생성 기록 확인 (kubectl describe)
kubectl describe rs blue-replicaset

# ReplicaSet의 Pod 생성 이후 과정 확인 (kubectl get events --sort-by=.metadata.creationTimestamp)
kubectl get events --sort-by=.metadata.creationTimestamp # 생성 순으로 정렬해서 볼 수 있게 --sort-by 사용

# 포트포워딩 8080 -> 8080 (ReplicaSet에 의해 생성된 파드로 트래픽 전달)
# rs/blue-replicaset 의미: replicaSet으로 생성된 blue-replicaset pod
# 8080:8080 의미: local의 8080 port와 pod의 8080 port container를 연결 port-forward
kubectl port-forward rs/blue-replicaset 8080:8080 
# 확인해보면 replicaSet 3개 중, 첫 번째 생성된 pod로만 요청이 전달된다. 즉, 로드밸런싱이 일어나지 않는 것을 알 수 있다.
# -> 즉, ReplicaSet Object는 Pod를 복제하고 관리하는 목적이 있지, Loadbalancing의 역할은 없음을 알 수 있고, 이 기능은 다른 Object를 사용해야 한다. 

# Pod로 요청 실행해보기 
curl -vs localhost:8080/hello
curl -vs localhost:8080/sky

# ReplicaSet 삭제
kubectl delete rs/blue-replicaset 
