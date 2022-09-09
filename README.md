# kubernetes-practice

# Kubernetes concept

# Kubernetes for Dev

개발자가 쿠버네티스를 실무에서 어떻게 활용할 것인가

## 클라우드 인프라 기반 컨테이너 플랫폼 환경 **설계 및 구축**을 할 수 있다.

1. AWS 네트워크 및 EKS 설계
2. Terraform을 활용한 AWS EKS 생성 및 관리
   - [Terraform](https://www.terraform.io)
   - [Terraformer](https://github.com/GoogleCloudPlatform/terraformer)
3. AWS EKS 기본 설정 (EKS plugin)

## 컨테이너 플랫폼 기반 **개발 환경**을 구성할 수 있다.

1. Kubernetes Manifest 작성
   아무리 yaml 파일을 작성한다고 하더라도 중복되는 부분이나 설정을 직접 작성해줘야 할 것들이 매우 많음.  
   그래서 개발자가 효율적으로 쉽고 빠르게 개발자가 쿠버네티스로 micro service를 배포하기 위해 사용하는 툴이 바로 [Kustomize](https://kustomize.io), [Helm](https://helm.sh)이다.

## 컨테이너 플랫폼의 안정적인 **운영 방안**을 마련할 수 있다.

1. GitOps - 버전 별로 무중단으로 배포 및 전환이 가능하고 선언적 코드와 실제 배포된 자원 정보가 git 같은 버전 관리 툴에서 관리가 되어 형상 관리까지 되도록 하는 것.  
   이를 실현하기 위해, Blue/Green, Canary 배포 등의 무중단 배포를 GitOps 기반의 형상, 배포 관리 툴인 [ArgoCD](https://argo-cd.readthedocs.io/en/stable/)를 통해 해볼 것
2. kubernetes 안정성 강화 방법 - 즉, 안정적으로 운영하는 방법
   - [minio](https://min.io)
   - [velero](https://velero.io)
3. kubernetes 보안 강화 활용
   - [kube2iam](https://github.com/jtblin/kube2iam)
   - [Falco](https://falco.org/ko/)
   - [opa](https://github.com/open-policy-agent/gatekeeper)
   - [cert-manager](https://cert-manager.io/docs/)
4. kubernetes 트러블 슈팅 방법 - 로깅
5. Go를 활용한 kubernetes CLI 개발
   - https://github.com/kubernetes/client-go
