# Ch04_03. [실습] metrics-server를 활용한 리소스 모니터링

Metrics-server는 쿠버네티스 모니터링에서 리소스 메트릭 파이프라인으로 개발된 모니터링 도구로써
kubelet을 통해 리소스 메트릭을 수집하고 이를 kube-apiserver의 `metrics` API로 제공합니다.

Metrics server는 쿠버네티스에서 자원의 사용량에 따라 Pod의 개수나 용량을 조절하는 오토스케일을 위해
사용되는데, Pod개수를 조절하는 HPA, Pod의 용량을 조절하는 VPA가 metrics server가 제공하는 Pod의
CPU, Memory 사용량을 보고, 오토스케일 룰에 따라 Pod를 변경시킵니다.

## url

https://github.com/kubernetes-sigs/metrics-server

# 준비 - start minikube 
Minikube는 가벼운 쿠버네티스 구현체이며, 로컬 머신에 VM을 만들고 하나의 노드로 구성된 간단한 클러스터를 생성한다.   
see https://lovethefeel.tistory.com/125
```
$ minikube start
$ minikube tunnel # https://www.nakjunizm.com/2021/10/05/Minikube_ExternalIP_Pending/ LoadBalancer type 사용허용을 위해 
```

# 설치

```
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl apply -f components.yaml
```
```bash
kubectl get po -n kube-system   

# Output
NAME                               READY   STATUS              RESTARTS      AGE
coredns-787d4945fb-7qmt2           1/1     Running             0             89s
etcd-minikube                      1/1     Running             0             103s
kube-apiserver-minikube            1/1     Running             0             101s
kube-controller-manager-minikube   1/1     Running             0             103s
kube-proxy-k5dxk                   1/1     Running             0             89s
kube-scheduler-minikube            1/1     Running             0             103s
metrics-server-6c86dbcddc-flc79    0/1     ContainerCreating   0             5s
storage-provisioner                1/1     Running             1 (58s ago)   100s

# wait for sec...
(base) grace@jeonghyeonjeong-ui-MacBookPro metric-server-hpa % kubectl get po -n kube-system  
NAME                               READY   STATUS    RESTARTS      AGE
coredns-787d4945fb-7qmt2           1/1     Running   0             2m
etcd-minikube                      1/1     Running   0             2m14s
kube-apiserver-minikube            1/1     Running   0             2m12s
kube-controller-manager-minikube   1/1     Running   0             2m14s
kube-proxy-k5dxk                   1/1     Running   0             2m
kube-scheduler-minikube            1/1     Running   0             2m14s
metrics-server-6c86dbcddc-flc79    1/1     Running   0             36s
storage-provisioner                1/1     Running   1 (89s ago)   2m11s
```
# Troubleshooting
```
(base) grace@jeonghyeonjeong-ui-MacBookPro kube-prometheus % kubectl get po -n kube-system metrics-server-68bfd5c84d-j8j6n
E0224 19:22:13.195319   65270 memcache.go:255] couldn't get resource list for metrics.k8s.io/v1beta1: the server is currently unable to handle the request
E0224 19:22:13.214213   65270 memcache.go:106] couldn't get resource list for metrics.k8s.io/v1beta1: the server is currently unable to handle the request
E0224 19:22:13.217249   65270 memcache.go:106] couldn't get resource list for metrics.k8s.io/v1beta1: the server is currently unable to handle the request
E0224 19:22:13.220757   65270 memcache.go:106] couldn't get resource list for metrics.k8s.io/v1beta1: the server is currently unable to handle the request
NAME                              READY   STATUS    RESTARTS   AGE
metrics-server-68bfd5c84d-j8j6n   0/1     Running   0          39h
```
설치된 Deployment / metrics-server 에서 아래와 같이 --kubelet-insecure-tls 라는 커맨드를 추가해주자.

ubuntu@ip-10-0-0-246:~$ kubectl edit deploy -n kube-system metrics-server 

    spec:
      containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
        - --kubelet-insecure-tls   << 추가

```
(base) grace@jeonghyeonjeong-ui-MacBookPro kube-prometheus % kubectl get po -n kube-system metrics-server-6c86dbcddc-dfnnf 
NAME                              READY   STATUS    RESTARTS   AGE
metrics-server-6c86dbcddc-dfnnf   1/1     Running   0          59s
```

```
kubectl get po -n kube-system       
```

# 실행
```bash
kubectl top node

# output
(base) grace@jeonghyeonjeong-ui-MacBookPro kube-prometheus % kubectl top node
NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
minikube   541m         9%     2141Mi          17% 
```

slack alert 실습을 위한 단계는 여기까지. 아래를 HPA test를 위한 실습. 
---



# API 리퀘스트

```
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes" |jq '.'
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes/worker-4" |jq '.'
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods" |jq '.'
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/kube-scheduler-controller-2" |jq '.'
```

# hpa 테스트

https://kubernetes.io/ko/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/

## 테스트 deployment 설치 

```
kubectl apply -f https://k8s.io/examples/application/php-apache.yaml

kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
```

## 부하 발생

```
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```
