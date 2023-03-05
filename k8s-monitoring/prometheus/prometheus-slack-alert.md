# Ch04_06. [실습] Prometheus AlarmManager을 통한 알람 수신

프로메테우스 UI에서 Alerts를 보면 여러 알림 내역을 확인할 수 있는데, 이는 프로메테우스가 수집하는 메트릭을 기반으로 어떠한 조건에 부합되는 상황이 유지되면
이를 알림으로 보내도록 룰 설정이 되어있기 때문에 알람이 발생한다. 
프로메테우스에서 설정된 알람 룰은 Status - Rules를 통해 어떤 알림이 등록되었는지 알 수 있다.
이러한 룰 설정은 kube-prometheus의 매니페스트를 통해 사전에 등록한 것이다.

```
kubectl get prometheusrules -n monitoring
kubectl get prometheusrules -n monitoring -o yaml node-exporter-rules
vi manifests/nodeExporter-prometheusRule.yaml
```

Prometheus는 정해진 알람의 룰에 따라 알람을 발생시키며, 이를 여러 메시지 수단으로 전달하는 것은 `alertmanager`의 역할이다.

# AlertManager
alertmanager는 알람 발생 시 정해진 메시지 수단으로 알람을 보내는 역할을 수행한다.
prometheus-operator에서 제공하는 alertmanager의 설정은 `manifests/alertmanager-secret.yaml`를 통해 설정한다.

```
vi manifests/alertmanager-secret.yaml

kubectl apply -f manifests/alertmanager-secret.yaml
```
이 설정파일에 slack에 대한 설정을 추가하면 이제 알림을 슬랙으로 받을 수 있다.

# Slack으로 알림 보내기
alertmanager 설정에 slack을 메시지 수단으로 추가할 수 있다. 이를 위해 slack의 설정이 필요한데, 테스트용으로 자신의 슬랙 채널의 설정에서 수신 webhook을 활성화하고 webhook url을 획득해야한다.

webhook을 활성화하고, 메시지를 보낼 채널을 설정한다.

1. 채널 생성 (그림7)
2. 

## alertmanager 설정
위의 webhook정보를 이용해 alertmanager를 설정한다.
```
vi manifests/alertmanager-secret.yaml
# manifests/alertmanager-secret.yaml 를 수정했다. git diff나 github으로 변경사항을 확인해보자. 
kubectl apply -f manifests/alertmanager-secret.yaml
```

## 테스트용 Rule 설정
slack으로 보낼 테스트 알람 룰을 생성한다. 
.
`manifests/kubernetesControlPlane-prometheusRule.yaml`에서 `CPUThrottlingHigh` 참고해서 알람 룰을 생성한다.
원래 여기 작성되어있는 것은 네임스페이스의 Pod의 컨테이너를 모니터링하면서 CPU사용율이 25%를 넘어가면 알람을 발생한다

```bash
kubectl get prometheusrules -n monitoring

# output
NAME                              AGE
alertmanager-main-rules           5d
kube-prometheus-rules             5d
kube-state-metrics-rules          5d
kubernetes-monitoring-rules       5d
node-exporter-rules               5d
prometheus-k8s-prometheus-rules   5d
prometheus-operator-rules         5d
```

```bash
vi test-prometheusRule.yaml
```
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  labels:
    app.kubernetes.io/name: kube-prometheus
    app.kubernetes.io/part-of: kube-prometheus
    prometheus: k8s
    role: alert-rules
  name: ddx-kubernetes-monitoring-rules
  namespace: monitoring
spec:
  groups:
  - name: ddx-test
    rules:
    - alert: DdxCPUThrottlingHighTest
      annotations:
        description: '{{ $value | humanizePercentage }} throttling of CPU in namespace
          {{ $labels.namespace }} for container {{ $labels.container }} in pod {{
          $labels.pod }}.'
        runbook_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/cputhrottlinghigh
        summary: Processes experience elevated CPU throttling.
      expr: |
        sum(increase(container_cpu_cfs_throttled_periods_total{container!="", namespace="default" }[5m])) by (container, pod, namespace)
          /
        sum(increase(container_cpu_cfs_periods_total{}[5m])) by (container, pod, namespace)
          > ( 5 / 100 )
      for: 1m # test라서 1분마다 모니터링하다가 1분만 threshold를 넘어가도 알람이 발생할 수 있게 설정했다. 
      labels:
        severity: critical
```
```bash
kubectl apply -f manifests/ddx-kubernetesControlPlane-prometheusRule.yaml
# output
prometheusrule.monitoring.coreos.com/ddx-kubernetes-monitoring-rules created


kubectl get prometheusrules -n monitoring
# output
NAME                              AGE
alertmanager-main-rules           5d
ddx-kubernetes-monitoring-rules   25s # custom한 rule이 생성되었음을 알 수 있다. 
kube-prometheus-rules             5d
kube-state-metrics-rules          5d
kubernetes-monitoring-rules       5d
node-exporter-rules               5d
prometheus-k8s-prometheus-rules   5d
prometheus-operator-rules         5d
```
prometheusRule을 생성하고, 프로메데우스 ui에서 이를 적용되는지 기다린다. 즉, 내가 custom해서 생성한 prometheus rule을 prometheus UI에서 확인 할 수 있다는 것임. 
Prometheus UI(localhost:9090/alert) -> Status -> Rules

## 부하발생
`metrics-server` 실습에서 사용한 loadgenerator를 사용해 default namespace에 CPU부하를 발생시키도록 pod에 부하를 주면서 알림 발생을 테스트한다.
```bash
# 지금 default namespace에 어떤 pod가 떠있는지 보자. 
kubectl get pod
```
No resources found in default namespace. 
php-apache 생성해보기. 
```bash
kubectl apply -f https://k8s.io/examples/application/php-apache.yaml
```

```bash
kubectl get pod
# output
NAME                          READY   STATUS    RESTARTS        AGE
php-apache-7495ff8f5b-fqkz6   1/1     Running   1 (3d14h ago)   5d
# php-apache-7495ff8f5b-fqkz6 는 이 web server에 index.php를 호출하면 내부적으로  백만번의 loop를 돌며 수학연산을 하고, loop가 모두 완료되면 OK를 출력하는 것이다. 
# 따라서 이 index.php를 계속 호출하는 것으로 이 pod에 부하를 줄 것이다. 
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://php-apache; done"

```