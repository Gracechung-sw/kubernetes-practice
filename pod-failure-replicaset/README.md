# ReplicaSet을 통한 내결함성 지키기
## Pod에 장애 발생 시 ReplicaSet이 어떻게 동작하는지 알아보자

## 실습 내용1. ReplicaSet이 내결함성(fault-tolerance)를 어떻게 지키는지 확인
1. ReplicaSet이 관리하는 Pod를 삭제해서 Pod 장애 상황을 가정한다. 
2. ReplicaSet이 관리하는 Pod 목록의 변화를 살펴본다. 
3. 위 과정을 통해 Node 장애 시 ReplicaSet의 행동을 예상해보자. 

## 실습 내용2. ReplicaSet만 제거하고 새로운 ReplicaSet으로 교체하는 방법 또는 ReplicaSet을 통해 생성된 Pod들은 놔두고, ReplicaSet'만' 삭제하는 방법

1. $ kubectl delete rs blue-replicaset
명령어의 결과는? 해당 replicaset(blue-replicaset)이 삭제되면서 replicaset이 관리하는 모든 pod가 같이 삭제됨. 

2. $ kubectl delete rs blue-replicaset --cascade=orphan
명령어의 결과는? 해당 replicaset(blue-replicaset)이 삭제되어도 생성된 pod는 삭제되지 않음. 