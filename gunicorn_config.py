command = 'gunicorn'
pythonpath = 'your_application_path'
workers = 4  # CPU 코어 수에 따라 조정
threads = 2
timeout = 120  # 타임아웃 값을 120초로 설정
bind = '0.0.0.0:8000'
