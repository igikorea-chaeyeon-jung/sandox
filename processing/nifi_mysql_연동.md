## 3. nifi 와 mysql 연동 및 데이터 수집 파이프라인 구성
### 실행 순서
1. kubernetes 환경 구성 -> kubespray

2. helm으로 mysql 설치
```
   helm install mysql oci://registry-1.docker.io/bitnamicharts/mysql
```

3. mysql password 설정
```
   MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace default mysql -o jsonpath="{.data.mysql-root-password}" | base64 -d)
```

4. mysql client 접속
```
1. Run a pod that you can use as a client:

   kubectl run mysql-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mysql:8.0.34-debian-11-r8 --namespace default --env MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD --command -- bash

2. To connect to primary service (read/write):

   mysql -h mysql.default.svc.cluster.local -uroot -p"$MYSQL_ROOT_PASSWORD"
```
5. database & table 생성
```
  # database "trade" 생성
  mysql> create database trade;
   
  # 데이터베이스 목록 확인
  mysql> show databases;

  # 데이터베이스 선택
  mysql> use testDB;

  # 테이블 생성
  mysql> 
  CREATE TABLE nation_trade_list (
    balPayments DECIMAL(18, 0),   
    expCnt INT,
    expDlr DECIMAL(18, 0),
    impCnt INT,
    impDlr DECIMAL(18, 0),
    statCd CHAR(2),
    statCdCntnKor1 VARCHAR(255),
    year VARCHAR(7)
  );

  # 칼럼 정보
  balPayments    number
  무역수지(달러)  
  expCnt    number
  수출건수
  expDlr    number
  수출금액(달러)
  impCnt    number
  수입건수
  impDlr    number
  수입금액(달러)
  statCd    string
  국가코드
```
* table columns 및 options 확인
```
  mysql> desc nation_trade_list;
```
<img width="577" alt="image" src="https://github.com/igikorea-chaeyeon-jung/sandox/assets/133837435/2b20d47d-0196-4e55-bda7-452008ae5325">

* 이외 명령어
```
  # database 삭제
  mysql> DROP DATABASE testDB;
```




  mysql 테이블 구성
<img width="901" alt="스크린샷 2023-08-11 오후 5 16 17" src="https://github.com/igikorea-chaeyeon-jung/sandox/assets/133837435/9e26a5f3-0a68-4204-8b28-a27a6698acde">

  Configure Processor(PutSQL)
<img width="793" alt="스크린샷 2023-08-11 오후 5 24 28" src="https://github.com/igikorea-chaeyeon-jung/sandox/assets/133837435/defe016f-081f-41c8-8cdc-2d9a1953a831">

  Controller Service Details
<img width="1209" alt="스크린샷 2023-08-11 오후 5 24 44" src="https://github.com/igikorea-chaeyeon-jung/sandox/assets/133837435/5fd23d1e-d614-4a16-9c6a-e6244be72598">
