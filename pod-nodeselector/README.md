# nodeSelector

nodeSelector로 원하는 노드 집합에 pod 배포하기.

## Quick start

1. 노드에 label을 추가한다.
2. pod yaml 파일에 spec.nodeSelector을 선언하여 원하는 노드에 해당 pod가 배포되도록 한다.
   즉, 쿠버네티스의 Master Node의 scheduler가 Pod 배포시 우리가 지정한 metadata의 nodeSelector를 보고 Pod를 배포할 노드를 선택한다.

label이

- soil: moist 인 node에
  tree-app pod가 배포되도록 한다.
- soil: dry 인 node에는 아무 pod도 배포되지 않도록 한다.
