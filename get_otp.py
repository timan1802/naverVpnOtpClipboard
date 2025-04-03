import poplib
import email
import pyperclip
import re
from bs4 import BeautifulSoup

# ❗개인메일함에 넣어놓으면 POP3로 못 가져옴

def read_config(file_path="config.txt"):
    config = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                config[key] = value
    except Exception as e:
        print(f"❌ 설정 파일을 읽는 중 오류 발생: {e}")
        exit()
    return config

config = read_config()

POP3_SERVER = config.get("POP3_SERVER", "")
POP3_PORT = int(config.get("POP3_PORT", 995))
USERNAME = config.get("USERNAME", "")
PASSWORD = config.get("PASSWORD", "")

TARGET_SUBJECT = "[네이버 클라우드 플랫폼] SSL VPN 접속을 위한 인증 OTP"
TARGET_SENDER = "dl_sslvpn_otp@navercorp.com"

def decode_header(header):
    """이메일 제목 디코딩"""
    decoded_fragments = email.header.decode_header(header)
    decoded_string = ""
    for fragment, encoding in decoded_fragments:
        if isinstance(fragment, bytes):
            encoding = encoding or "utf-8"
            decoded_string += fragment.decode(encoding, errors="ignore")
        else:
            decoded_string += fragment
    return decoded_string

def extract_otp_from_html(html_content):
    """HTML에서 OTP 코드 추출"""
    soup = BeautifulSoup(html_content, "html.parser")
    otp_cell = soup.find("td", {"colspan": "5"})  # OTP 코드가 들어있는 <td> 찾기

    if otp_cell:
        otp_code = otp_cell.text.strip()
        return otp_code
    return None

mailbox = None
try:
    print("📩 POP3 서버에 연결 중...")
    mailbox = poplib.POP3_SSL(POP3_SERVER, POP3_PORT)
    mailbox.user(USERNAME)
    mailbox.pass_(PASSWORD)
    print("✅ 로그인 성공!")

    messages = mailbox.list()[1]
    num_messages = len(messages)
    print(f"📬 서버에서 불러온 메일 개수: {num_messages}")

    if num_messages == 0:
        print("⚠️ 받은 메일이 없습니다.")
        mailbox.quit()
        exit()

    messages.reverse()
    check_count = min(5, num_messages)
    print(f"🔍 최근 {check_count}개의 메일을 확인합니다.")

    found_otp = False
    for i in range(check_count):
        index = int(messages[i].split()[0])
        print(f"🔍 {index}번 메일 확인 중...")

        response, lines, octets = mailbox.retr(index)
        msg_data = b"\n".join(lines)
        msg = email.message_from_bytes(msg_data)

        sender = decode_header(msg["From"])
        print(f"📨 보낸 사람: {sender}")
        if TARGET_SENDER not in sender:
            print(f"🚫 보낸 사람이 {TARGET_SENDER}이(가) 아닙니다.")
            continue

        subject = decode_header(msg["Subject"])
        print(f"📌 메일 제목: {subject}")

        body = ""
        html_body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    try:
                        payload = part.get_payload(decode=True).decode(part.get_content_charset(), errors="ignore")
                        if content_type == "text/plain":
                            body = payload
                        elif content_type == "text/html":
                            html_body = payload
                    except:
                        continue
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset(), errors="ignore")

        print("📜 HTML 본문 내용:")
        print(html_body[:500])  # 디버깅을 위해 일부만 출력

        otp_code = None

        if html_body:
            otp_code = extract_otp_from_html(html_body)
        if not otp_code:
            match = re.search(r"SSL VPN 인증 OTP\s*(\d{6})", body)
            if match:
                otp_code = match.group(1)

        if otp_code:
            print(f"✅ OTP 코드: {otp_code}")
            pyperclip.copy(otp_code)
            print("📋 OTP 코드가 클립보드에 복사되었습니다.")
            found_otp = True
            break
        else:
            print("⚠️ OTP 코드가 본문에서 발견되지 않았습니다.")

    if not found_otp:
        print("⚠️ OTP 메일을 찾지 못했습니다.")

except Exception as e:
    print(f"❌ 오류 발생: {e}")

finally:
    if mailbox is not None:
        mailbox.close()
        print("📤 연결 종료")
