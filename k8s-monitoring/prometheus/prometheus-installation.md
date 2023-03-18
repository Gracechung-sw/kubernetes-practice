# Ch04_05. [실습] Prometheus와 Grafan를 통한 쿠버네티스 모니터링
이번 시간에는 kube-prometheus 프로젝트를 통해 프로메테우스, 그라파나, alertmanager, node-exporter등 프로메테우스와 관련된 서비스를 설치하고
 사용해본다.

kube-prometheus는 Prometheus-operator를 기본으로 프로메테우스, Alertmanger, node-exporter, kube-state-metrics, grafana 애플리케이션과 관련 설정을 제공하는 프로젝트로, 간편한 설정을 통해 프로메테우스를 관리할 수 있다.

# start minikube 
Minikube는 가벼운 쿠버네티스 구현체이며, 로컬 머신에 VM을 만들고 하나의 노드로 구성된 간단한 클러스터를 생성한다.   
see https://lovethefeel.tistory.com/125

# kube-prometheus 저장소
https://github.com/prometheus-operator/kube-prometheus

# 지원 버전 확인
https://github.com/prometheus-operator/kube-prometheus#compatibility

# 저장소 복사

```
git clone https://github.com/prometheus-operator/kube-prometheus.git -b release-0.10
```

--
이미 있다면 바로 아래 단계로!

#  Manifest, CRD

```
cd kube-prometheus
ls manifests -l
ls manifests/setup -l
```

# 설치

```
kubectl create -f ./manifests/setup/
kubectl create -f ./manifests/
```


# 서비스 연결

설치된 pod 확인
```bash
kubectl get pods -n monitoring

# output
(base) grace@jeonghyeonjeong-ui-MacBookPro kube-prometheus % kubectl get pods -n monitoring
NAME                                   READY   STATUS              RESTARTS   AGE
blackbox-exporter-7bcbc4f86c-8crgv     0/3     ContainerCreating   0          5s
grafana-5d4999d5c7-r849j               0/1     ContainerCreating   0          5s
kube-state-metrics-948c54447-gmzm6     0/3     Pending             0          4s
node-exporter-p4vvx                    0/2     Pending             0          4s
prometheus-adapter-7857494459-d7bpk    0/1     Pending             0          4s
prometheus-adapter-7857494459-m222b    0/1     Pending             0          4s
prometheus-operator-74dbf5644d-pld2w   0/2     Pending             0          4s

# wait for sec...
(base) grace@jeonghyeonjeong-ui-MacBookPro kube-prometheus % kubectl get pods -n monitoring
NAME                                   READY   STATUS    RESTARTS   AGE
alertmanager-main-0                    2/2     Running   0          89s
alertmanager-main-1                    2/2     Running   0          89s
alertmanager-main-2                    2/2     Running   0          89s
blackbox-exporter-7bcbc4f86c-8crgv     3/3     Running   0          2m3s
grafana-5d4999d5c7-r849j               1/1     Running   0          2m3s
kube-state-metrics-948c54447-gmzm6     3/3     Running   0          2m2s
node-exporter-p4vvx                    2/2     Running   0          2m2s
prometheus-adapter-7857494459-d7bpk    1/1     Running   0          2m2s
prometheus-adapter-7857494459-m222b    1/1     Running   0          2m2s
prometheus-k8s-0                       1/2     Running   0          88s
prometheus-k8s-1                       1/2     Running   0          88s
prometheus-operator-74dbf5644d-pld2w   2/2     Running   0          2m2s
```

설치된 service들 확인
```bash
kubectl get svc -n monitoring

# output
NAME                    TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE
alertmanager-main       LoadBalancer   10.109.116.194   127.0.0.1     9093:30179/TCP,8080:30761/TCP   2m21s
alertmanager-operated   ClusterIP      None             <none>        9093/TCP,9094/TCP,9094/UDP      107s
blackbox-exporter       ClusterIP      10.107.202.163   <none>        9115/TCP,19115/TCP              2m21s
grafana                 LoadBalancer   10.110.225.41    127.0.0.1     3000:31759/TCP                  2m21s
kube-state-metrics      ClusterIP      None             <none>        8443/TCP,9443/TCP               2m20s
node-exporter           ClusterIP      None             <none>        9100/TCP                        2m20s
prometheus-adapter      ClusterIP      10.107.21.40     <none>        443/TCP                         2m20s
prometheus-k8s          LoadBalancer   10.109.42.165    127.0.0.1     9090:30291/TCP,8080:31446/TCP   2m20s
prometheus-operated     ClusterIP      None             <none>        9090/TCP                        106s
prometheus-operator     ClusterIP      None             <none>        8443/TCP                        2m20s
```

이 service들은 web UI를 제공하고 있기 때문에 외부에서도 접근 가능해야하는데, 보이는 것 처럼 **EXTERNAL-IP**가 none이다. 
port forwarding을 사용할 수도 있지만, Load balancer를 사용해서 외부에서 접근 가능하도록 설정할 것임. 

Grafana 설정파일에 가서 load balancer 사용 설정을 추가해주겠음. 

즉, 
prometheus 어플리케이션을 사용하기 위해서는 외부에서 접속할 수 있도록 서비스 설정이 필요하다. `prometheus-service.yaml`은 기본적으로 clusterIP로 설정되어있는데, `LoadBalancer`나 `NodePort`, 혹은 Ingress를 통해 외부에서 접속할 수 있도록 변경한다. 아래 파일은 `LoadBalancer`를 사용하도록 설정한 예시이다.

`LoadBalancer` 서비스로 Pod를 노출하는 방법은

prometheus와 grafana의 svc타입을 `LoadBalancer`로 추가하여 다시 kubernetes에 적용한다.

```
vi manifests/grafana-service.yaml
vi manifests/prometheus-service.yaml
vi manifests/alertmanager-service.yaml
# type 추가
type: LoadBalancer

kubectl apply -f manifests/grafana-service.yaml
kubectl apply -f manifests/prometheus-service.yaml
kubectl apply -f manifests/alertmanager-service.yaml
```

# 서비스 확인

```bash
kubectl get svc -n monitoring

# output
(base) grace@jeonghyeonjeong-ui-MacBookPro kube-prometheus % kubectl get svc -n monitoring

NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                         AGE
alertmanager-main       LoadBalancer   10.104.7.188    127.0.0.1     9093:32026/TCP,8080:30811/TCP   21m
alertmanager-operated   ClusterIP      None            <none>        9093/TCP,9094/TCP,9094/UDP      35h
blackbox-exporter       ClusterIP      10.97.52.57     <none>        9115/TCP,19115/TCP              35h
grafana                 LoadBalancer   10.109.131.97   127.0.0.1     3000:31046/TCP                  21m
kube-state-metrics      ClusterIP      None            <none>        8443/TCP,9443/TCP               35h
node-exporter           ClusterIP      None            <none>        9100/TCP                        35h
prometheus-adapter      ClusterIP      10.104.177.30   <none>        443/TCP                         35h
prometheus-k8s          LoadBalancer   10.103.86.120   127.0.0.1     9090:31243/TCP,8080:30272/TCP   21m
prometheus-operated     ClusterIP      None            <none>        9090/TCP                        35h
prometheus-operator     ClusterIP      None            <none>        8443/TCP                        35h
```

EXTERNAL-IP 잘 할당 받는 것을 알 수 있다. 

## troubleshooting
EXTERNAL-IP pending issue
https://www.nakjunizm.com/2021/10/05/Minikube_ExternalIP_Pending/


# 프로메테우스 UI
- Prometeus, grafana ui 접근
- Prometeus ui에 들어가 어떤 기능을 제공하는지 봐보자. 
- grafana ui 접근하면, 기본적으로 prometheus에서 제공해주는 메트릭으로 이루어진 기본 dashboard를 제공함. 
-> 근데 이게 우리 관리자 admin 하드웨어 관리 에 매우 적절한 정보들이 있는 것 같음. 
15분 42초경. 

```
kubectl get svc -n monitoring prometheus-k8s -o jsonpath={.status.loadBalancer.ingress[].ip}
```
127.0.0.1:9090 -> Prometheus Web UI에 접속하여, Graph, Status->Target, Rules를 살표본다.
- Graph: prometheus가 수집하고 있는 metric을 조회할 수 있다. 검색창에 http를 쳐서 (그림1) 자동완성으로 어떤 metric이 수집되고 있는지 확인할 수 있다. 'prometheus_http_requests_total'을 검색해보rh, Graph를 눌러보면 어떤 request의 metric을 graph로 보여준다. 


# 프로메테우스 서비스 모니터: 무엇을 모니터링 하나
Web UI에서 Status-Target에 표시되는 것이 ServiceMonitor이다. 이는 처음 설치한 manifests에서 `serviceMonitor`라는 파일로 설정되어있는데, kubectl 명령으로 현재 생성된 서비스모니터를 확인 할 수 있다.
```bash
ls manifests/*serviceMonitor* -alh

kubectl get servicemonitor -n monitoring
kubectl get servicemonitor -n monitoring -o yaml node-exporter 
kubectl get svc -n monitoring | grep node-exporter
kubectl get svc -n monitoring -o yaml node-exporter # 이것에 대한 설명 9'경 수업 다시보기!
```

kubectl get svc -n monitoring -o yaml node-exporter 에 대한 output
```yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: "2023-02-23T01:09:36Z"
  labels:
    app.kubernetes.io/component: exporter
    app.kubernetes.io/name: node-exporter
    app.kubernetes.io/part-of: kube-prometheus
    app.kubernetes.io/version: 1.3.1
  name: node-exporter
  namespace: monitoring
  resourceVersion: "18420"
  uid: 7205c1d1-bc85-4928-a1e9-3e0114f77175
spec:
  clusterIP: None
  clusterIPs:
  - None
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - name: https
    port: 9100 # node exporter가 9100번 port를 사용해 서비스 되고 있다.  curl http://localhost:9100/metrics 로 metric 확인 할 수 있음. 
    protocol: TCP
    targetPort: https
  selector:
    app.kubernetes.io/component: exporter
    app.kubernetes.io/name: node-exporter
    app.kubernetes.io/part-of: kube-prometheus
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
```



# metrics 확인
node-exporte 메트릭을 확인해본다.

```
sudo ss -lp|grep 9100
curl http://localhost:9100/metrics
```

# Grafana
그라파나는 프로메테우스에 수집되는 메트릭을 대시보드를 통해 시각화 페이지를 제공한다.
우리가 모니터링 화면이라고 알고있는 다양한 그래프를 그라파나를 통해 볼 수있다.

## 서비스 접근
```
kubectl get svc -n monitoring
```
http://localhost:3000 (그림2)

## Login, 비밀번호 설정
최초 계정정보는 `admin`/`admin`이며, 새 비밀번호를 설정할 수 있다.

## 대시보드
kube-prometheus에서 기본으로 제공하는 대시보드가 있는데 이를 통해 쿠버네티스 클러스터에 대한 모니터링 화면을 확인할 수 있다.

왼쪽 패널 menu(네모 4개 있는 것) -> Browse (그림4 )
-> default -> (그림5,6)