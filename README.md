# Clieb

> 인공어 단어장 프로젝트

## `res/info.txt`

기본적인 문자열을 구성하기 위한 문자열들입니다.
첫번째 줄에는 언어의 이름, 두번째 줄에는 '검색'이라는 뜻의 단어,
세번째 줄에는 '`[|AMOUNT|]`개의 단어가 수록되어 있습니다.'라는 뜻의 문자열을 입력해주세요.
`[|AMOUNT|]`는 특수 문자열로, 수록된 단어의 수를 대변합니다.

```text
(언어 이름)
검색
[|AMOUNT|]개의 단어가 수록되어 있습니다.
```

## 사전

> ./dictionary.py를 실행해주세요.

사전을 켜면 언어의 이름과, 검색어를 입력할 수 있는 엔트리,
검색 버튼과 '단어 수정 및 추가' 버튼이 있습니다.
이 화면을 로비 화면이라고 부릅니다.

### 단어 추가 방법

단어 수정 및 추가 버튼을 누르면 한 개의 엔트리와 텍스트 입력 란을 볼 수 있습니다.
언어 이름 뒤에 엔트리는 추가/수정할 단어를 입력합니다.
만약 단어가 이미 존재한다면 - 단어의 뜻을 수정할 예정이라면 - 단어 입력 후 '불러오기'를 눌러주세요.
뜻 텍스트 입력 란에 단어에 맞는 원하는 뜻을 입력하고 '추가' 버튼을 눌러주세요.
창은 자동으로 종료됩니다.

### 단어 검색 방법

로비 화면에서 검색어를 입력할 수 있는 엔트리에 검색어를 입력하고 엔터 키를 누르거나 검색 버튼을 누릅니다.
`<언어 이름>: <검색어>` 형식의 이름을 가진 창을 볼 수 있습니다.
이 창을 검색 결과 창이라고 부릅니다.
검색 결과 창에는 단어의 이름이나 뜻으로 검색어를 포함하고 있는 모든 단어를 유니코드 순서로 나열합니다.
악센트, 움라우트 등이 있는 단어도 없는 것으로 계산됩니다.

프로그램의 모든 창은 `ESC` 키를 눌러서 종료할 수 있습니다.

## 서버

> ./online_dictionary.py를 실행해주세요

다음과 같은 문자열을 볼 수 있습니다:

```text
Listen requests on http://localhost:35536/
```

[이곳](http://localhost:35536/)에 접속하면 온라인으로 자신의 사전을 사용할 수 있습니다.
만약 자신의 아이피가 포드포워딩 되어있거나, 하마치 등의 프로그램을 이용해 다른 사람의 컴퓨터로 하여금
접속할 수 있는 상황에 놓여있다면 다른 사람도 사전 서버에 접속할 수 있습니다.

이 때 사용해야 하는 웹 주소는 다음과 같습니다:

```text
http://<당신의 아이피>:35536/
```

서버에서는 단어를 추가하거나 수정할 수 없습니다.

### 단어 검색

서버에 접속하면 큰 글씨로 자신의 언어의 이름,
현재 사전에 등재된 단어의 갯수 또는 사전에 대한 설명,
검색할 검색어를 입력할 수 있는 텍스트 입력 란과 검색 버튼이 있습니다.

검색어를 입력하고 검색 버튼을 누르면 검색 결과 창으로 이동합니다.
사용법은 사전과 동일합니다.