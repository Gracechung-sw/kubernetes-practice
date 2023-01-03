# ReplicaSet이 파드를 생성하는 과정과 ReplicaSet의 역할 이해

## 실습 내용1. 레플리카셋을 통한 파드 생성 확인
1. ReplicaSet 선언
2. ReplicaSet이 파드 생성하는 과정 확인 
3. 로컬 머신에서 ReplicaSet으로 생성한 파드로 트래픽을 전달하여 테스트하는 방법
4. 여러 개의 파드로 로드밸런싱이 되는지 확인

## 실습 내용2. 선언한 파드 수보다 더 많은 파드가 존재할 때 레플라카셋의 행동 확인 
1. ReplicaSet에 선언한 셀렉터로 새로운 파드 생성
2. 생성한 파드 상태와 ReplicaSet 행동 확인

## 실습 내용3. ReplicaSet의 Pod Template을 변경하고 적용하는 방법
1. ReplicaSet을 생성한다
2. Pod Template을 변경한 후 ReplicaSet을 변경한다
3. Pod 제거 후 변화를 관찰한다
이를 통해 Replicaset에 선언한 replicas 값이 변경되었을 경우에만 Pod을 새로 생성하지, 그 외 Template가 변경되면 기존 template로 생성된 Pod에는 영향을 주지 않는 것을 확인 할 수 있다. 

## 실습 내용4. ReplicaSet으로 Pod 레플리카수 조정하기