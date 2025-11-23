import os, logging, asyncio
from datetime import datetime

class LogClass():
    def __init__(self, basePath, apiLogs):
        self.basePath = basePath
        self.apiLogs = apiLogs
        super().__init__()

    async def create_logger(self, logs_for_module = 'COMMON'):
        current_time = datetime.now().strftime('%Y%m%d')
        log_file_path = os.path.join(self.basePath, self.apiLogs, logs_for_module, current_time)
        if not os.path.exists(log_file_path):
            await os.makedirs(log_file_path, exist_ok=True)
        log_file_name = f"{logs_for_module.lower()}_{current_time}.log"
        log_path = os.path.join(log_file_path, log_file_name)
        print(f"FINAL_LOG PATH: {log_path}")
        logger = logging.getLogger(f"app_logger_{logs_for_module}")
        logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=10000)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s | %(name)s | %(filename)s:%(lineno)d\n')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger