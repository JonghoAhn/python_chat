command = 'gunicorn'
pythonpath = 'https://port-0-python-chat-1272llwx73p0i.sel5.cloudtype.app/chat'
workers = 4  # CPU 코어 수에 따라 조정
threads = 2
timeout = 120  # 타임아웃 값을 120초로 설정
bind = '0.0.0.0:8000'
