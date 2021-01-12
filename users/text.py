def message(domain, uidb64, token):
    print(domain)
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다. \n\n 회원가입 링크 : http://{domain}/users/activate/{uidb64}/{token}\n\n감사합니다. "


# 나중에 링크 수정하기 -> main