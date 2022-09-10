# Kubernetes로 구축하는 MSA

## MicroService란

[MicroService](https://microservices.io)
느슨하게 결홥된 stateless 서비스의 모임
작은 여러 서비스로 분해
독립적으로 개발, 전개, 규모 확장, 배포 -> 병렬로 개발이 가능

하지만 microservice로 개발시 생길수 있는 문제점 또는 고려사항은

- 동기식 통신을 사용하는 다수의 소형 컴포넌트는 연쇄 장애를 일으킬 수 있다.
- 다수의 소형 컴포넌트를 최신 상태로 유지하는 것이 어렵다.
- 많은 컴포넌트 처리에 관여하는 요청은 추적하기 어렵다.
- 컴포넌트 수준의 하드웨어 자원 사용량 분석도 어려움
- 다수의 소형 컴포넌트를 수동으로 구성하고 관리할 때 비용이 많이 들고 오류가 발생하기 쉬움.

결국 **아키텍쳐 디자인** 이 중요하다.

## [Microservice 디자인 패턴](https://microservices.io/patterns/index.html) 목록

(사진 첨부하기)

## 학습 목표

1. 컨테이너화된 마이크로서비스를 쿠버네티스 상에서 구현
2. 쿠버네티스 기반의 MSA 설계 및 구축
3. 실무에서 활용 가능한 수준의 기본적인 MSA 기반 운영/관리

## 학습 목차

1. Microservic 개발 방법 (Spring(https://spring.io/microservices) 기반으로 할 것임.)  
   -> 이걸로 한 번 감 잡고, 나는 Nodejs & Python 기술 스택 기반으로 MSA를 구축해야 하는 상황이기 때문에 사내 Udemy [
   Microservices with Node JS and React](https://www.udemy.com/course/microservices-with-node-js-and-react/learn/lecture/19102526?start=0#content) 참고하기.

   - requirements

     - Java, Curl, jq(json 처리 opensource), Sprint boot CLI 설치
       [맥에서 자바 런타임(JRE) 설치하는 방법(인텔, 애플 실리콘 공통)](https://www.lainyzine.com/ko/article/how-to-install-java-runtime-environment-on-macos/)

     ```bash
     brew tap spring-io/tap
     brew install java
     java -version

     brew install jq
     jq --version

     brew install spring-boot
     spring version

     ```

2. API 설계 및 구현 방법
3. Persistence 레이어 구현 방법
4. [Spring Cloud Data Flow](https://spring.io/projects/spring-cloud-dataflow)를 활용한 Batch 및 Stream 구현 방법
5. Reactive 개발 방법
6. Kafka를 활용한 Pub/Sub 구현
7. MSA 안정성 강화 방법
8. Service Mesh 구축 방법
9. gRPC 구현 방법
10. MSA 보안 강화 방법 -> 지금 현업에서 중요한 것!! 각 서비스 어플리케이션에 대한 인증(식별), 보안
11. MSA 트러블 슈팅 방법
12. MSA 활용 미니 프로젝트 수행하기

## 1. Microservic 개발 방법

1. [실습] MSA를 위한 Microservice 개발 소개
2. [실습] Dependency 설정 및 패키지 및 클래스 지정 방법
3. [실습] Aspect 및 Listener 명시 및 Rest Template 및 Controller
4. [실습] Application 설정 및 Actutator 적용 및 Jar 생성 옵션 설정 방법
