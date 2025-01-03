import logging

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    # 로거가 이미 핸들러를 가지고 있다면 추가 설정하지 않음
    if logger.handlers:
        return logger
        
    # 로그 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 파일 핸들러 설정 (선택사항)
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    
    return logger