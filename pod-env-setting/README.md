# 컨테이너로 환경 변수 전달 실습
1. Pod 선언과 환경변수 설정
2. Pod 생성/배포
3. Pod IP 할당 및 컨테이너 실행 확인
4. Port-forward procdess를 실행하여 3000:3000
5. local에서 Pod로 트래픽 전송
6. HTTP 서버 응답 확인
7. 컨테이너 환경변수 목록 확인

## 쿠버네티스 값을 컨테이너로 전달할 환경변수와 값 참조 경로
POD_NAME: metadata.name
NAMESPACE_NAME: metadata.namespace
POD_IP: status.podIP
NODE_IP: status.hostIP
NODE_NAME: spec.nodeName

## Pod 템플릿 선언 시 컨테이너로 전달할 환경변수와 값
STUDENT_NAME: 본인이름
GREETING: STUDENT_NAME을 참조한 인삿말

## kubectl 명령어
- Pod 생성: kubectl apply -f <yaml 파일 경로>
- Pod 실행 및 IP 확인: kubectl get pod -o wid # -o 는 output의 출력 형식에 대한 옵션이다. wide는 상세 정보 표현. 
- Pod는 종료: kubectl deletes pod --all or kubectl delete pod <pod name>
- 컨테이너 IP 확인: kubectl exec <pod name> [-c <container name>] --ifconfig eth0
- 컨테이너 환경변수 확인 kubectl exec <pod name> --env
- 포트 포워딩 kubectl port-forward <pod name> <host port> <container port>