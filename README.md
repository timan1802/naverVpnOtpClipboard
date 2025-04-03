# 📩 POP3 이메일에서 OTP 코드 추출 (EXE 실행 파일)

이 프로젝트는 POP3 이메일 서버에서 최근 OTP 메일을 검색하고,
NAVER Cloude SSL VPN 6자리 OTP 코드를 추출하여 클립보드에 복사하는 Python 스크립트입니다. 
Windows에서 실행 가능한 **EXE 파일**로 변환하여 쉽게 사용할 수 있습니다.


---

## 🔹 1. 설정 파일 (`config.txt`) 작성

EXE 실행 파일이 사용할 POP3 서버 정보를 설정해야 합니다.
`config.txt` 파일을 `get_otp.exe`와 같은 폴더에 만들고 다음 내용을 입력하세요.

```ini
POP3_SERVER=pop.naver.com
POP3_PORT=995
USERNAME=your_email@naver.com
PASSWORD=your_password
```

**⚠️ 주의:** 비밀번호를 직접 입력하는 것은 보안상 위험할 수 있으므로, 안전한 방법을 고려하세요.

---

## 🔹 2. EXE 파일 생성 방법

### ✅ 사전 준비 (Python & 라이브러리 설치)

EXE 파일을 만들려면 Python과 필요한 패키지를 설치해야 합니다.

```sh
pip install pyinstaller beautifulsoup4 pyperclip
```

### ✅ EXE 파일 만들기

`get_otp.py`가 있는 폴더에서 다음 명령어를 실행하세요.

```sh
pyinstaller --onefile --noconsole get_otp.py
```

- `--onefile` : 단일 실행 파일로 패키징
- `--noconsole` : 실행 시 콘솔 창 없이 실행됨 (백그라운드에서 동작)

생성이 완료되면 `dist` 폴더에 `get_otp.exe` 파일이 만들어집니다.

---

## 🔹 3. EXE 실행 방법

1. `config.txt` 파일을 `get_otp.exe`와 같은 폴더에 둡니다.
2. `get_otp.exe`를 더블 클릭하여 실행합니다.
3. 실행 후 OTP 코드가 자동으로 클립보드에 복사됩니다.

### ✅ CMD에서 실행 (로그 확인 가능)

만약 실행 후 바로 창이 닫혀서 로그를 확인하기 어렵다면, `CMD`를 열고 다음 명령어로 실행하세요.

```sh
cd dist
get_otp.exe
```

---

## 🔹 4. 문제 해결 (FAQ)

### ❓ 실행했는데 콘솔 창이 닫혀서 로그를 볼 수 없음

👉 CMD를 열고 직접 실행하면 로그를 확인할 수 있습니다.

```sh
cd dist
get_otp.exe
```

### ❓ 백신이 실행 파일을 차단함

👉 일부 백신 프로그램에서 `pyinstaller`로 만든 EXE를 오진할 수 있습니다. Windows Defender 예외 목록에 추가하면 해결됩니다.

### ❓ OTP 코드가 클립보드에 복사되지 않음

👉 `pyperclip`이 정상적으로 동작하지 않을 수 있습니다. Python 환경에서 `pyperclip`이 정상적으로 설치되었는지 확인하세요.

```sh
pip install pyperclip
```

### ❓ 개인메일함에 넣어놓으면 POP3로 못 가져옴
👉 분류메일함에 해당 메일을 분류해 놓으면 POP3에서 내려 주지 않음. 분류를 해제 하고 사용해야 한다. 

---

## 🛠️ 추가 개발

이 프로그램을 개선하거나 기능을 추가하고 싶다면 `get_otp.py` 파일을 수정하고 다시 EXE로 변환하면 됩니다.

✅ **추가 기능 제안:**

- GUI 추가하여 설정 파일 없이 로그인 가능하게 만들기
- Gmail, Outlook 등 IMAP 지원 추가
- OTP 코드를 자동으로 특정 프로그램에 입력하기

---

## 📜 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자유롭게 사용하고 개선하세요! 🚀

