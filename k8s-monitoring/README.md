# Kubernetes 구축
[macOs m1 환경에서 Kubernetes 시작하기(feat. Docker)](https://velog.io/@pinion7/macOs-m1-%ED%99%98%EA%B2%BD%EC%97%90%EC%84%9C-kubernetes-%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0)
```bash
brew install minikube  

minikube version

minikube start --driver=docker  

brew install kubectl
```

## 1. Master Node 구축
## 2. Worker Node 구축


# Kubernetes 운영

## 1. metrics-server를 활용한 리소스 모니터링
[Kubernetes Metics Server](https://github.com/kubernetes-sigs/metrics-server)
: Metrics Server is a scalable, efficient source of container resource metrics for Kubernetes built-in autoscaling pipelines.   
k8s 리소스 메트릭 파이프라인으로 개발된 서버.    

Metrics Server collects resource metrics from Kubelets and exposes them in Kubernetes apiserver through Metrics API for use by Horizontal Pod Autoscaler and Vertical Pod Autoscaler. Metrics API can also be accessed by kubectl top, making it easier to debug autoscaling pipelines.   
즉, Horizontal Pod Autoscaler and Vertical Pod Autoscaler 가 Metrics Server가 제공하는 Pod의 CPU, memory사용량을 보고, auto scale rule에 따라 Pod를 scaling한다. 

실습 내용)
1. K8s cluster에 metrics server를 설치
2. metric api를 사용해서 node와 pod의 사용량 metrics을 확인
즉, metric api 명령어($ kubectl top)를 치면 -> Kubernetes apiserver에 metrics api를 호출 -> Kubernetes Metrics Server가 수집한 metrics를 보여줌.
3. HPA를 활용하여 Pod의 auto scaling

### 1) K8s cluster에 metrics server를 [설치](https://github.com/kubernetes-sigs/metrics-server#installation)
```bash
# metrics server yaml file을 download
$ wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# 위 명령어로 다운받은 components.yaml 에 명시되어있는 K8s object들을 설치
$ kubectl apply -f ./components.yaml

# metrics server 설치 확인
$ kubectl get po -n kube-system  
# NAME                               READY   STATUS    RESTARTS   AGE
# coredns-787d4945fb-57nbt           1/1     Running   0          107s
# etcd-minikube                      1/1     Running   0          2m1s
# kube-apiserver-minikube            1/1     Running   0          2m1s
# kube-controller-manager-minikube   1/1     Running   0          2m1s
# kube-proxy-7dzqj                   1/1     Running   0          107s
# kube-scheduler-minikube            1/1     Running   0          2m1s
# metrics-server-68bfd5c84d-j8j6n    0/1     Running   0          99s # HERE!
# storage-provisioner                1/1     Running   0          2m
```
### 2) metric api를 사용해서 node와 pod의 사용량 metrics을 확인
```bash
# ( metric api x) 그냥 top 명령어 사용
$ kubectl top node

$ kubectl top pod -n kube-system
# 이러면 NAME CPU(cors) MEMORY(bytes) 정보들이 나옴.

# metric api 사용
$ kubectl get --raw "/apis/metrics.k8s.io/vibeta1/nodes" |ja '.'
# node에 대한 metrics가 json형태로 나옴. 

$ kubectl get --raw "/apis/metrics.k8s.io/vibeta1/nodes/[node_이름]" |ja '.'
# [node_이름]의 특정 node에 대한 정보만 확인 할 수도 있음. 

# pod
$ kubectl get --raw "/apis/metrics.k8s.io/vibeta1/namespaces/kube-system/pods" |ja '.'
``` 
### 3) HPA를 활용하여 Pod의 auto scaling
Ref. 공식문서 [HorizontalPodAutoscaler 연습](https://kubernetes.io/ko/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)

(base) grace@jeonghyeonjeong-ui-MacBookPro metric-server-hpa % kubectl apply -f php-apache.yaml 

deployment.apps/php-apache created
service/php-apache created



## 2. Prometheus와 Grafana를 통한 k8s 모니터링
[kube-prometheus](https://github.com/prometheus-operator/kube-prometheus)
### 1) 설치
쿠버네티스 클러스터 환경에서 사용할 수 있도록 clone해온 뒤 menifest들을 설치한다. 
git clone https://github.com/prometheus-operator/kube-prometheus.git -b release-0.10

### 2) 
아래 명령어를 통해 kube-prometheus project를 통해 설치 할 수 있는 application, menifest가 있음을 알 수 있다.
setup folder에는 operator를 사용하기 위한 custom definition file들도 위치 해있음. 

cd kube-prometheus
ls manifests -l
ls manifests/setup -l

그리고 menifeasts/setup/namespace.yml을 보면 monitoring이라는 namespace로 설치되도록 하고 있다는 것을 알 수 잇음. 

### 3) 설치
kubectl create -f ./manifests/setup/
kubectl create -f ./manifests/

설치된 pod 확인
kubectl -n monitoring get pods

설치된 service들 확인
kubectl get svc -n monitoring

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
alertmanager-main       ClusterIP   10.102.31.81    <none>        9093/TCP,8080/TCP            2m12s
alertmanager-operated   ClusterIP   None            <none>        9093/TCP,9094/TCP,9094/UDP   88s
blackbox-exporter       ClusterIP   10.97.52.57     <none>        9115/TCP,19115/TCP           2m12s
grafana                 ClusterIP   10.97.216.106   <none>        3000/TCP                     2m11s
kube-state-metrics      ClusterIP   None            <none>        8443/TCP,9443/TCP            2m11s
node-exporter           ClusterIP   None            <none>        9100/TCP                     2m11s
prometheus-adapter      ClusterIP   10.104.177.30   <none>        443/TCP                      2m10s
prometheus-k8s          ClusterIP   10.107.53.171   <none>        9090/TCP,8080/TCP            2m10s
prometheus-operated     ClusterIP   None            <none>        9090/TCP                     87s
prometheus-operator     ClusterIP   None            <none>        8443/TCP                     2m10s

이 service들은 web UI를 제공하고 있기 때문에 외부에서도 접근 가능해야하는데, 보이는 것 처럼 **EXTERNAL-IP**가 none이다. 
port forwarding을 사용할 수도 있지만, Load balancer를 사용해서 외부에서 접근 가능하도록 설정할 것임. 

Grafana 설정파일에 가서 load balancer 사용 설정을 추가해주겠음. 

vi menifests/grafana-service.yaml

apiVersion: v1
kind: Service
metadata:
  labels:
    app.kubernetes.io/component: grafana
    app.kubernetes.io/name: grafana
    app.kubernetes.io/part-of: kube-prometheus
    app.kubernetes.io/version: 8.3.3
  name: grafana
  namespace: monitoring
spec:
  ports:
  - name: http
    port: 3000
    targetPort: http
  selector:
    app.kubernetes.io/component: grafana
    app.kubernetes.io/name: grafana
    app.kubernetes.io/part-of: kube-prometheus
  type: LoadBalancer # 이거 추가!

alarm에도
 vi manifests/alertmanager-service.yaml

promethues의 service도 
vi manifests/prometheus-service.yaml 

이를 재적용
후
service 재조회해보면
NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                         AGE
alertmanager-main       LoadBalancer   10.102.31.81    <pending>     9093:30506/TCP,8080:31151/TCP   10m
alertmanager-operated   ClusterIP      None            <none>        9093/TCP,9094/TCP,9094/UDP      9m34s
blackbox-exporter       ClusterIP      10.97.52.57     <none>        9115/TCP,19115/TCP              10m
grafana                 LoadBalancer   10.97.216.106   <pending>     3000:30120/TCP                  10m
kube-state-metrics      ClusterIP      None            <none>        8443/TCP,9443/TCP               10m
node-exporter           ClusterIP      None            <none>        9100/TCP                        10m
prometheus-adapter      ClusterIP      10.104.177.30   <none>        443/TCP                         10m
prometheus-k8s          LoadBalancer   10.107.53.171   <pending>     9090:30483/TCP,8080:31494/TCP   10m
prometheus-operated     ClusterIP      None            <none>        9090/TCP                        9m33s
prometheus-operator     ClusterIP      None            <none>        8443/TCP                        10m

EXTERNAL-IP 잘 할당 받는 것을 알 수 있다. 

- Prometeus, grafana ui 접근

- Prometeus ui에 들어가 어떤 기능을 제공하는지 봐보자. 

- grafana ui 접근하면, 기본적으로 prometheus에서 제공해주는 메트릭으로 이루어진 기본 dashboard를 제공함. 
-> 근데 이게 우리 관리자 admin 하드웨어 관리 에 매우 적절한 정보들이 있는 것 같음. 
15분 42초경. 


## 3. Prometheus와 AlertManager를 통한 알람 수신
2:27 -> 이 alarm ruled의 severity는 warning이고, 
-> description은 이 filesystem이 24간 내에 다 찰 거 같다. 지금 어느 정도 남았다 ~~ 임
-> 우리 서비스에 매우 유용할 듯!
-> 개발자 세션에서 소개해주면 좋을 듯!

alertmanager도 UI를 제공해주고, 여기서 rule Setting 가능. 
4'19''

6'01'' slack alert 실습하심. 

**앞서 metrics-server를 활용한 리소스 모니터링 말고 ## 2. Prometheus와 Grafana를 통한 k8s 모니터링, ## 3. Prometheus와 AlertManager를 통한 알람 수신 부분만 개발자세션에서 Hands on으로 발표하자. 그리고 이전에는 Envoy를 설명하는 시간을 가진 적이 있는데, Istio는 ~~~이다. 그래서 다음 개발자세션때는 Istio를 이용한 Service Mesh에 대한 내용을 하려고 한다. 라고 하기**

-> **일단 여기까지 하고 promethus 설정에 대한 실습 이후는 안해도 될 듯 과함.**

## 4. Prometheus 설정
kube-Prometheus 프로젝트의 Prometheus를 어떻게 설정할 수 있는지를 알아본다. 
https://github.com/Jaesang/fastcampus_kubernetes/blob/main/kubernetes/monitoring/07_prometheus_configuration.md 

## 5. Grafana 설치
kube-Prometheus를 통한 Grafana 설치를 해본다. 
