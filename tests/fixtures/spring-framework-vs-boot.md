# 02. Spring Framework와 Spring Boot의 차이점

Java로 Spring 프로젝트를 개발하다 보면 Spring Framework와 Spring Boot라는 두 가지 이름을 자주 접하게 됩니다.

새로운 프로젝트를 생성할 때도 Spring Boot를 선택하고, 실제 개발 과정에서는 Spring Framework가 제공하는 `@Component`, `@Service`, `@Transactional`, `@RestController` 등의 기능을 사용합니다.

그런데 여기서 한 가지 의문이 생깁니다.

Spring Framework와 Spring Boot는 서로 다른 프레임워크일까요? 아니면 같은 기술의 다른 버전일까요?

두 기술은 밀접한 관계가 있지만 담당하는 역할은 다릅니다.

Spring Framework가 애플리케이션 개발에 필요한 핵심 기능과 기반 구조를 제공한다면, Spring Boot는 이러한 기능을 보다 쉽고 빠르게 구성하고 실행할 수 있도록 지원합니다.

이번 글에서는 두 기술의 차이점과 등장 배경을 살펴보고, 실제 프로젝트 구성과 실행 과정에서 어떤 역할을 하는지 알아보겠습니다.

## 1. Spring Framework와 Spring Boot의 관계

먼저 두 기술의 관계부터 이해해 보겠습니다.

Spring Framework는 Java 애플리케이션을 개발하기 위한 핵심 프레임워크입니다.

객체 생성과 의존성 관리, AOP, 트랜잭션, 웹 요청 처리 등 애플리케이션을 구성하는 데 필요한 다양한 기능을 제공합니다.

반면 Spring Boot는 Spring 기반 애플리케이션을 보다 쉽게 개발하고 실행할 수 있도록 만들어진 프로젝트입니다.

Spring Framework가 제공하는 기능을 기반으로 자동 설정, 의존성 관리, 내장 서버, 운영 편의 기능 등을 제공합니다.

두 기술의 관계를 간단하게 표현하면 다음과 같습니다.

```
                 Spring Boot
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
  자동 설정       의존성 관리      내장 서버
       |              |              |
       +--------------+--------------+
                      |
                      v
              Spring Framework
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
      IoC            AOP          Spring MVC
       |              |              |
       v              v              v
    Bean 관리      Proxy        HTTP 요청 처리
```

Spring Boot는 Spring Framework를 대체하는 기술이 아닙니다.

Spring Framework를 기반으로 애플리케이션을 구성하고 실행하는 과정을 단순화하는 기술입니다.

따라서 Spring Boot를 사용하더라도 실제 애플리케이션의 핵심 동작은 Spring Framework가 담당합니다.

## 2. Spring Framework만으로 애플리케이션을 개발한다면?

Spring Boot가 등장한 이유를 이해하려면 먼저 Spring Boot가 없던 시절의 개발 방식을 살펴볼 필요가 있습니다.

Spring Framework만으로도 웹 애플리케이션을 개발할 수 있습니다.

다만 개발자가 직접 설정해야 하는 부분이 상대적으로 많았습니다.

예를 들어 다음과 같은 작업이 필요합니다.

- Spring Framework 라이브러리 추가
    
- 필요한 의존성 버전 관리
    
- ApplicationContext 구성
    
- Bean 등록 및 컴포넌트 스캔 설정
    
- 데이터베이스 연결 설정
    
- 트랜잭션 관리자 설정
    
- Spring MVC 설정
    
- Servlet과 DispatcherServlet 등록
    
- 웹 애플리케이션 서버 구성
    

물론 이러한 설정이 모두 필수인 것은 아니며, 사용하는 기능과 프로젝트 환경에 따라 달라집니다.

하지만 프로젝트를 처음 구성할 때부터 개발자가 직접 결정하고 관리해야 하는 항목이 많았습니다.

### 2.1 의존성 관리

Spring MVC 기반 웹 애플리케이션을 개발한다고 가정하겠습니다.

Spring Framework의 핵심 기능을 사용하기 위해 필요한 라이브러리를 직접 추가해야 합니다.

Maven을 사용한다면 다음과 같은 방식으로 의존성을 선언할 수 있습니다.

```
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>${spring.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-webmvc</artifactId>
        <version>${spring.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-jdbc</artifactId>
        <version>${spring.version}</version>
    </dependency>
</dependencies>
```

여기서는 필요한 Spring 모듈을 직접 추가하고 있습니다.

실제 프로젝트에서는 여기에 데이터베이스 드라이버, JSON 처리 라이브러리, 로깅 라이브러리 등 다양한 의존성이 추가됩니다.

문제는 라이브러리가 늘어날수록 버전 관리가 복잡해진다는 점입니다.

서로 호환되는 버전을 사용해야 하며, 의존성 간 충돌이 발생하지 않도록 관리해야 합니다.

특히 프로젝트 규모가 커질수록 직접 관리해야 하는 라이브러리의 수가 증가합니다.

### 2.2 Spring 설정 관리

Spring Framework는 다양한 설정 방식을 제공합니다.

예를 들어 Java 기반 설정을 사용한다면 다음과 같이 ApplicationContext를 구성할 수 있습니다.

```
@Configuration
@ComponentScan(basePackages = "com.example")
public class AppConfig {

    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }
}
```

그리고 애플리케이션에서 해당 설정을 읽어 Spring Container를 생성해야 합니다.

```
public class Main {

    public static void main(String[] args) {

        AnnotationConfigApplicationContext context =
                new AnnotationConfigApplicationContext(AppConfig.class);

        MemberService memberService =
                context.getBean(MemberService.class);

        memberService.register("Kim");

        context.close();
    }
}
```

이 코드는 Spring Framework가 제공하는 기능을 이용해 ApplicationContext를 직접 생성하고 Bean을 조회하는 예제입니다.

웹 애플리케이션이라면 여기에 HTTP 요청을 처리하기 위한 추가적인 설정이 필요합니다.

예를 들어 Servlet 기반 애플리케이션에서는 `DispatcherServlet`을 Servlet Container에 등록해야 합니다.

### 2.3 웹 애플리케이션 서버 구성

Spring MVC를 이용해 웹 애플리케이션을 개발하려면 HTTP 요청을 받아 처리할 수 있는 Servlet Container가 필요합니다.

대표적으로 Tomcat을 사용할 수 있습니다.

전통적인 WAR 배포 방식에서는 다음과 같은 구조를 사용했습니다.

```
사용자
  |
  | HTTP Request
  v
Tomcat
  |
  v
DispatcherServlet
  |
  v
Controller
  |
  v
Service
  |
  v
Repository
```

개발자는 애플리케이션을 WAR 파일로 패키징하고, 별도로 설치된 Tomcat에 배포하는 방식을 사용할 수 있었습니다.

이러한 구조는 충분히 안정적이고 유효한 방식이지만, 개발 환경을 구성하고 배포하는 과정에서 별도의 설정과 관리가 필요합니다.

Spring Framework만으로 개발하는 것이 불가능하거나 잘못된 방식이라는 의미는 아닙니다.

다만 애플리케이션을 실행하기 위해 필요한 여러 기술적 설정을 개발자가 직접 관리해야 한다는 특징이 있습니다.

## 3. Spring Boot가 해결하는 문제

Spring Boot는 Spring 기반 애플리케이션을 개발할 때 반복적으로 발생하는 설정과 구성 작업을 줄이기 위해 등장했습니다.

대표적인 기능은 다음과 같습니다.

1. Auto Configuration
    
2. Starter Dependencies
    
3. Embedded Server
    
4. Externalized Configuration
    
5. Production-ready Features
    

각 기능을 살펴보겠습니다.

## 4. Auto Configuration: 자동 설정

Spring Boot의 가장 대표적인 기능 중 하나는 자동 설정(Auto Configuration)입니다.

자동 설정은 애플리케이션의 클래스패스, 설정값, 등록된 Bean 등의 조건을 확인하여 필요한 설정을 자동으로 구성하는 기능입니다.

예를 들어 Spring MVC를 사용하려면 여러 가지 구성 요소가 필요합니다.

- DispatcherServlet
    
- HandlerMapping
    
- HandlerAdapter
    
- HttpMessageConverter
    
- ViewResolver 등
    

Spring Framework만 사용하는 환경에서는 이러한 구성 요소를 직접 설정하거나 관련 설정을 구성해야 할 수 있습니다.

반면 Spring Boot에서는 필요한 의존성을 추가하면 조건에 따라 관련 설정을 자동으로 구성합니다.

### 4.1 자동 설정 적용하기

Spring Boot 프로젝트에서 다음과 같이 애플리케이션을 작성했다고 가정하겠습니다.

```
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

이 코드만으로도 Spring Boot 애플리케이션의 기본 실행 구조를 구성할 수 있습니다.

여기서 중요한 어노테이션은 `@SpringBootApplication`입니다.

이 어노테이션은 다음 세 가지 주요 어노테이션을 결합한 형태입니다.

```
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan
```

각각의 역할은 다음과 같습니다.

|어노테이션|역할|
|---|---|
|@SpringBootConfiguration|Spring Boot 애플리케이션의 설정 클래스임을 나타냄|
|@EnableAutoConfiguration|조건에 따라 필요한 자동 설정을 활성화|
|@ComponentScan|지정된 범위에서 Spring Bean 후보를 검색|

즉, `@SpringBootApplication` 하나로 애플리케이션 설정, 자동 설정, 컴포넌트 스캔을 활성화할 수 있습니다.

### 4.2 자동 설정은 어떻게 동작할까?

자동 설정은 단순히 모든 기능을 무조건 활성화하는 방식이 아닙니다.

Spring Boot는 특정 조건을 만족하는 경우에만 설정을 적용합니다.

예를 들어 웹 애플리케이션을 구성하는 자동 설정은 관련 라이브러리가 클래스패스에 존재하는지, 특정 Bean이 이미 등록되어 있는지 등을 확인합니다.

이러한 조건을 표현하는 데 다음과 같은 어노테이션이 사용됩니다.

- `@ConditionalOnClass`: 특정 클래스가 존재하는 경우
    
- `@ConditionalOnMissingBean`: 특정 Bean이 등록되어 있지 않은 경우
    
- `@ConditionalOnProperty`: 특정 설정값이 존재하거나 조건을 만족하는 경우
    
- `@ConditionalOnBean`: 특정 Bean이 등록되어 있는 경우
    

예를 들어 다음과 같은 자동 설정을 생각해 볼 수 있습니다.

```
@Configuration
@ConditionalOnClass(SomeLibrary.class)
public class ExampleAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public ExampleService exampleService() {
        return new ExampleService();
    }
}
```

이 설정은 다음 조건을 만족할 때 적용됩니다.

1. `SomeLibrary` 클래스가 클래스패스에 존재해야 합니다.
    
2. `ExampleService` 타입의 Bean이 이미 등록되어 있지 않아야 합니다.
    

조건을 만족하면 Spring Container에 `ExampleService` Bean이 등록됩니다.

이러한 방식 덕분에 개발자는 기본 설정을 직접 작성하지 않아도 필요한 기능을 사용할 수 있습니다.

### 4.3 자동 설정은 개발자의 설정을 무시할까?

자동 설정을 이해할 때 중요한 부분이 있습니다.

자동 설정은 개발자가 직접 작성한 설정을 무조건 덮어쓰는 기능이 아닙니다.

Spring Boot의 자동 설정은 조건부로 동작하며, 개발자가 직접 Bean을 등록하면 기본 자동 설정이 적용되지 않도록 구성된 경우가 많습니다.

예를 들어 다음과 같이 직접 Bean을 등록할 수 있습니다.

```
@Configuration
public class CustomConfig {

    @Bean
    public ExampleService exampleService() {
        return new CustomExampleService();
    }
}
```

자동 설정에 `@ConditionalOnMissingBean` 조건이 적용되어 있다면 이미 등록된 `ExampleService`를 확인하고 기본 Bean 등록을 건너뛸 수 있습니다.

즉, 자동 설정은 기본값을 제공하면서도 개발자가 필요에 따라 구성을 변경할 수 있도록 설계되어 있습니다.

자동 설정은 개발자의 자유를 제한하는 기능이 아니라, 반복적인 기본 설정을 줄여 주는 기능입니다.

## 5. Starter Dependencies: 의존성 관리 간소화

Spring Boot의 또 다른 핵심 기능은 Starter입니다.

앞서 살펴본 것처럼 Spring Framework만 사용하는 경우 필요한 라이브러리를 직접 추가해야 합니다.

그런데 특정 기능을 구현하기 위해서는 여러 라이브러리가 함께 필요한 경우가 많습니다.

예를 들어 Spring MVC 기반 웹 애플리케이션을 개발하려면 Spring Web 관련 라이브러리와 JSON 처리 등에 필요한 의존성이 필요합니다.

Spring Boot는 이러한 의존성을 하나의 Starter로 묶어 제공합니다.

### 5.1 Spring Boot Starter란?

Starter는 특정 기능을 개발하는 데 필요한 의존성들을 편리하게 추가할 수 있도록 제공하는 의존성 묶음입니다.

대표적인 Starter는 다음과 같습니다.

|Starter|주요 역할|
|---|---|
|spring-boot-starter-web|Servlet 기반 웹 애플리케이션 개발|
|spring-boot-starter-webflux|Reactive 기반 웹 애플리케이션 개발|
|spring-boot-starter-data-jpa|JPA 기반 데이터 접근|
|spring-boot-starter-jdbc|JDBC 기반 데이터 접근|
|spring-boot-starter-security|보안 기능|
|spring-boot-starter-validation|입력값 검증|
|spring-boot-starter-test|테스트 지원|

예를 들어 Spring MVC를 사용하는 프로젝트라면 다음과 같이 의존성을 추가할 수 있습니다.

Gradle:

```
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

Maven:

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

이렇게 하면 Spring MVC 애플리케이션 개발에 필요한 관련 의존성을 편리하게 추가할 수 있습니다.

### 5.2 의존성 버전은 누가 관리할까?

Starter를 사용하는 것만큼 중요한 기능이 의존성 버전 관리입니다.

Spring Boot는 함께 사용하도록 검증된 라이브러리 버전 정보를 관리합니다.

Gradle에서는 Spring Boot의 의존성 관리 기능을 활용할 수 있으며, Maven에서는 Spring Boot의 Parent 또는 BOM(Bill of Materials)을 이용할 수 있습니다.

예를 들어 Gradle 프로젝트에서는 다음과 같이 작성할 수 있습니다.

```
plugins {
    id 'java'
    id 'org.springframework.boot' version '4.1.0'
    id 'io.spring.dependency-management' version '1.1.7'
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

위 버전은 설정 방식의 예시이며, 실제 프로젝트에서는 사용하는 Spring Boot 릴리스와 호환되는 버전을 확인해야 합니다.

이처럼 Starter와 의존성 관리를 함께 사용하면 라이브러리 간 버전 충돌을 줄이고 프로젝트 구성을 단순화할 수 있습니다.

## 6. Embedded Server: 내장 서버

Spring Boot의 또 다른 중요한 특징은 내장 서버입니다.

기존 Servlet 기반 웹 애플리케이션에서는 외부에 설치된 Tomcat 등의 Servlet Container에 애플리케이션을 배포하는 방식이 일반적이었습니다.

반면 Spring Boot는 애플리케이션 내부에서 실행할 수 있는 내장 서버를 지원합니다.

대표적으로 다음과 같은 서버를 사용할 수 있습니다.

- Tomcat
    
- Jetty
    
- Undertow
    

### 6.1 기존 방식과 Spring Boot 방식 비교

기존 WAR 배포 방식은 다음과 같습니다.

```
+---------------------------+
|       외부 Tomcat         |
|                           |
|  +---------------------+  |
|  |   Spring Application|  |
|  |                     |  |
|  |   DispatcherServlet |  |
|  |   Controller        |  |
|  |   Service           |  |
|  +---------------------+  |
|                           |
+---------------------------+
```

Spring Boot의 내장 서버를 사용하는 방식은 다음과 같습니다.

```
+--------------------------------+
|       Spring Boot Application  |
|                                |
|  +--------------------------+  |
|  |       Embedded Tomcat    |  |
|  |                          |  |
|  |    DispatcherServlet     |  |
|  |    Controller            |  |
|  |    Service               |  |
|  +--------------------------+  |
|                                |
+--------------------------------+
```

기존 방식에서는 서버를 별도로 준비하고 애플리케이션을 배포해야 했습니다.

Spring Boot의 내장 서버를 사용하면 애플리케이션 실행 시 서버도 함께 시작할 수 있습니다.

### 6.2 Spring Boot 애플리케이션 실행하기

다음과 같은 코드를 작성했다고 가정하겠습니다.

```
@SpringBootApplication
public class Application {

    public static void main(String[] args) {

        SpringApplication.run(
                Application.class,
                args
        );
    }
}
```

애플리케이션을 실행하면 Spring Boot가 ApplicationContext를 구성하고, 웹 애플리케이션에 필요한 내장 서버를 시작합니다.

실행 결과는 다음과 비슷한 형태로 나타납니다.

```
Tomcat initialized with port 8080
Starting service [Tomcat]
Starting Servlet engine
Tomcat started on port 8080
Started Application
```

이제 별도의 Tomcat 설치와 수동 배포 없이 애플리케이션을 실행할 수 있습니다.

물론 Spring Boot가 내장 서버만 지원하는 것은 아닙니다.

필요하다면 WAR 형태로 패키징하여 외부 Servlet Container에 배포하는 방식도 사용할 수 있습니다.

## 7. Externalized Configuration: 외부 설정 관리

애플리케이션을 개발하다 보면 환경에 따라 서로 다른 설정값을 사용해야 합니다.

예를 들어 데이터베이스 연결 정보를 생각해 보겠습니다.

개발 환경에서는 개발용 데이터베이스를 사용하고, 운영 환경에서는 운영용 데이터베이스를 사용해야 합니다.

이러한 설정값을 Java 코드에 직접 작성한다면 환경이 변경될 때마다 코드를 수정해야 합니다.

Spring Boot는 외부 설정 기능을 통해 이러한 문제를 해결합니다.

### 7.1 application.properties

Spring Boot에서는 `application.properties` 파일을 이용해 설정값을 관리할 수 있습니다.

```
server.port=8080

spring.datasource.url=jdbc:postgresql://localhost:5432/blog
spring.datasource.username=developer
spring.datasource.password=password
```

이렇게 설정하면 Spring Boot가 해당 설정을 읽어 애플리케이션 구성에 활용합니다.

YAML 형식을 선호한다면 `application.yml`을 사용할 수도 있습니다.

```
server:
  port: 8080

spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/blog
    username: developer
    password: password
```

두 파일은 같은 목적을 수행하며 프로젝트의 설정 방식에 따라 선택할 수 있습니다.

### 7.2 환경별 설정 분리

개발 환경과 운영 환경의 설정을 분리하려면 Profile을 활용할 수 있습니다.

예를 들어 다음과 같이 파일을 구성할 수 있습니다.

```
src/main/resources/
    application.yml
    application-local.yml
    application-dev.yml
    application-prod.yml
```

각 환경에 맞는 설정을 작성합니다.

`application-local.yml`

```
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/blog_local
    username: local_user
    password: local_password
```

`application-prod.yml`

```
spring:
  datasource:
    url: jdbc:postgresql://production-db:5432/blog
    username: production_user
    password: production_password
```

실행할 때 활성화할 Profile을 지정할 수 있습니다.

```
java -jar application.jar --spring.profiles.active=prod
```

이렇게 하면 동일한 애플리케이션 코드를 사용하면서 환경에 따라 서로 다른 설정을 적용할 수 있습니다.

단, 실제 운영 환경에서는 데이터베이스 비밀번호와 같은 민감한 정보를 설정 파일에 평문으로 저장하지 않고 환경 변수나 별도의 Secret 관리 시스템을 사용하는 것이 좋습니다.

## 8. Production-ready Features: 운영 환경을 위한 기능

애플리케이션을 개발하는 것과 실제 운영 환경에서 안정적으로 서비스하는 것은 다른 문제입니다.

운영 환경에서는 애플리케이션이 정상적으로 실행 중인지, 요청을 처리할 수 있는 상태인지, 어떤 문제가 발생하고 있는지 확인할 수 있어야 합니다.

Spring Boot는 이러한 운영 요구사항을 지원하기 위해 Spring Boot Actuator를 제공합니다.

Actuator를 사용하면 애플리케이션의 상태와 다양한 운영 정보를 확인할 수 있습니다.

대표적인 Endpoint는 다음과 같습니다.

|Endpoint|역할|
|---|---|
|/actuator/health|애플리케이션의 상태 확인|
|/actuator/info|애플리케이션 정보 확인|
|/actuator/metrics|메트릭 정보 확인|
|/actuator/env|환경 설정 정보 확인|
|/actuator/beans|등록된 Bean 정보 확인|

예를 들어 Health Endpoint를 활성화하면 애플리케이션이 정상적으로 동작하는지 확인할 수 있습니다.

Actuator 의존성을 추가합니다.

```
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
}
```

필요한 Endpoint를 설정합니다.

```
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
```

이후 다음 주소로 요청하면 상태 정보를 확인할 수 있습니다.

```
GET /actuator/health
```

응답 예시는 다음과 같습니다.

```
{
  "status": "UP"
}
```

실제 응답에는 데이터베이스 등 연결된 구성 요소의 상태가 추가로 포함될 수 있습니다.

Actuator는 모니터링 시스템과 연동할 수 있기 때문에 운영 환경에서 유용하게 활용됩니다.

다만 모든 Endpoint를 외부에 공개해서는 안 됩니다.

특히 환경 변수나 Bean 정보처럼 내부 시스템 정보가 포함될 수 있는 Endpoint는 접근 권한과 노출 범위를 신중하게 설정해야 합니다.

## 9. Spring Framework와 Spring Boot 비교

지금까지 살펴본 내용을 바탕으로 두 기술의 역할을 비교해 보겠습니다.

|비교 항목|Spring Framework|Spring Boot|
|---|---|---|
|목적|애플리케이션 개발을 위한 핵심 기능 제공|Spring 애플리케이션의 구성과 실행 간소화|
|객체 관리|IoC Container와 DI 제공|Spring Framework의 기능 활용|
|AOP|AOP 기능 제공|Spring Framework의 AOP 기능 활용|
|트랜잭션|트랜잭션 추상화와 관리 기능 제공|관련 자동 설정과 의존성 구성 지원|
|웹 개발|Spring MVC, WebFlux 제공|웹 애플리케이션 자동 설정과 실행 지원|
|의존성 관리|개발자가 직접 구성 가능|Starter와 버전 관리 기능 제공|
|서버 실행|실행 환경을 별도로 구성할 수 있음|내장 서버 지원|
|설정 관리|다양한 설정 방식 제공|외부 설정과 Profile 관리 지원|
|운영 기능|핵심 기반 기능 제공|Actuator 등 운영 편의 기능 제공|

여기서 중요한 점은 Spring Boot가 Spring Framework의 모든 기능을 대신 구현하는 것이 아니라는 사실입니다.

Spring Boot는 Spring Framework를 기반으로 애플리케이션을 구성하는 과정을 간소화합니다.

실제 애플리케이션의 객체 관리, AOP, 트랜잭션, MVC 등의 핵심 동작은 Spring Framework와 관련 모듈이 담당합니다.

## 10. Spring Boot 없이 Spring Framework를 사용할 수 있을까?

그렇다면 Spring Boot를 사용하지 않고 Spring Framework만으로 개발하는 것도 가능할까요?

당연히 가능합니다.

Spring Framework는 Spring Boot에 종속된 기술이 아닙니다.

Spring Boot 없이도 다음과 같은 기능을 사용할 수 있습니다.

- IoC Container
    
- Dependency Injection
    
- AOP
    
- Spring MVC
    
- Transaction Management
    
- JDBC 지원
    
- ORM 통합
    

예를 들어 다음과 같이 ApplicationContext를 직접 생성할 수 있습니다.

```
@Configuration
@ComponentScan(basePackages = "com.example")
public class AppConfig {
}
```

```
public class Main {

    public static void main(String[] args) {

        ApplicationContext context =
                new AnnotationConfigApplicationContext(
                        AppConfig.class
                );

        MemberService service =
                context.getBean(MemberService.class);

        service.register("Kim");
    }
}
```

이처럼 Spring Boot가 없어도 Spring Container를 생성하고 Bean을 관리할 수 있습니다.

다만 웹 애플리케이션을 개발하거나 운영 환경을 구성한다면 필요한 설정을 직접 관리해야 할 부분이 많아집니다.

따라서 특별한 이유가 없다면 신규 Spring 기반 애플리케이션에서는 Spring Boot를 사용하는 것이 일반적으로 효율적입니다.

## 11. Spring Framework를 먼저 이해해야 하는 이유

최근에는 대부분의 Spring 프로젝트에서 Spring Boot를 사용합니다.

프로젝트 생성부터 서버 실행까지 많은 부분이 자동으로 처리되기 때문에 개발자는 빠르게 API를 구현할 수 있습니다.

하지만 자동으로 처리되는 기능이 많다는 것은 반대로 내부 동작을 이해하기 어려워질 수 있다는 의미이기도 합니다.

예를 들어 다음과 같은 코드를 살펴보겠습니다.

```
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

단 몇 줄의 코드만으로 애플리케이션이 실행됩니다.

하지만 내부적으로는 다음과 같은 작업이 수행됩니다.

1. SpringApplication이 애플리케이션 실행을 준비합니다.
    
2. ApplicationContext의 종류를 결정합니다.
    
3. Environment와 설정 정보를 준비합니다.
    
4. BeanDefinition을 등록합니다.
    
5. 자동 설정을 적용합니다.
    
6. Bean을 생성하고 의존 관계를 구성합니다.
    
7. 필요한 경우 내장 웹 서버를 시작합니다.
    
8. 애플리케이션이 실행 가능한 상태가 됩니다.
    

이 과정은 단순히 Spring Boot가 모든 것을 대신 처리하는 것이 아닙니다.

Spring Framework의 Container, BeanFactory, ApplicationContext, BeanPostProcessor 등의 기능이 함께 동작합니다.

따라서 Spring Boot를 능숙하게 사용하려면 그 기반이 되는 Spring Framework의 동작 원리를 이해하는 것이 중요합니다.

자동 설정이 정상적으로 적용되지 않거나, Bean이 예상과 다르게 등록되거나, 트랜잭션이 제대로 동작하지 않는 상황에서도 내부 원리를 알고 있다면 문제를 훨씬 빠르게 추적할 수 있습니다.

## 12. 마무리

이번 글에서는 Spring Framework와 Spring Boot의 차이점과 각 기술의 역할을 살펴보았습니다.

핵심 내용을 정리하면 다음과 같습니다.

1. Spring Framework는 Java 애플리케이션 개발을 위한 핵심 프레임워크입니다.
    
2. Spring Boot는 Spring 기반 애플리케이션의 구성과 실행을 간소화하는 프로젝트입니다.
    
3. Auto Configuration은 조건에 따라 필요한 설정을 자동으로 구성합니다.
    
4. Starter는 특정 기능에 필요한 의존성을 편리하게 추가할 수 있도록 제공합니다.
    
5. Embedded Server를 사용하면 별도의 서버 설치 없이 애플리케이션을 실행할 수 있습니다.
    
6. Externalized Configuration을 통해 환경별 설정을 분리할 수 있습니다.
    
7. Actuator는 애플리케이션의 상태와 운영 정보를 확인할 수 있도록 지원합니다.
    

두 기술의 관계를 한 문장으로 정리하면 다음과 같습니다.

Spring Framework는 애플리케이션을 구성하는 핵심 기능을 제공하고, Spring Boot는 이러한 기능을 더 쉽고 빠르게 사용할 수 있도록 도와줍니다.

다음 글에서는 Spring Framework의 전체 아키텍처를 살펴보겠습니다.

Spring Framework가 단순히 여러 기능을 제공하는 라이브러리의 집합이 아니라, Core Container, AOP, Data Access, Web 등 어떤 구조로 나뉘어 있고 각 모듈이 어떻게 연결되는지 알아보겠습니다.