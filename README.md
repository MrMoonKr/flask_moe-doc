# Flask 기반의 파이썬 웹 프로그래밍 사이트

## 관련링크
- https://bitbucket.org/jiholee/flask_moe/src/master/
- https://www.flask.moe/

## 설치방법
```bash
$ python3 -m venv venv
```
### 가상환경 진입(윈도우)
```bash
> venv\Scripts\activate
```

### 가상환경 진입(맥 또는 리눅스)
```bash
$ source venv/bin/activate
```

### 필수 패키지 설치
```bash
$ pip install -r requirements.txt
```

## 설정 파일 생성
```bash
$ vi config.yml
telegram_token: <Telegram Bot Token>
database_uri: <SQLAlchemy Database URI>
telegram_search5: <텔레그램 ID>
```

## 실행 (가상 환경 안에서)
```bash
$ python run.py
```
