import inspect, os
from datetime import datetime

LOG_LEVEL_ALL = 0
LOG_LEVEL_HIGH = 1
LOG_LEVEL_MEDIUM = 2
LOG_LEVEL_LOW = 3

__LOG_TYPE_FATAL = 0
__LOG_TYPE_ERROR = 1
__LOG_TYPE_WARNING = 2
__LOG_TYPE_SUCCESS = 3
__LOG_TYPE_INFORMATION = 4
__LOG_TYPE_DEBUG = 5
__LOG_TYPE_TRACE = 6

def create_logger(ident: str):
    return {"id": ident, "toggle_file_logging": None, "toggle_db_logging": None, "log_level": None, "file_path": None, "file_logging_timestamp": None, "conn": None, "cursor": None}

def initialize_logger(logger_instance,toggle_db_logging: bool = False, toggle_file_logging: bool = False):
    logger_instance["toggle_file_logging"] = toggle_file_logging
    logger_instance["toggle_db_logging"] = toggle_db_logging
    logger_instance["log_level"] = LOG_LEVEL_ALL
    logger_instance["file_path"] = "logs/"
    logger_instance["file_logging_timestamp"] = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    if toggle_db_logging:
        __initialize_db_logger(logger_instance)

def __initialize_db_logger(logger_instance):
    import sqlite3
    logger_instance["conn"] = sqlite3.connect("logs/logs.db")
    logger_instance["cursor"] = logger_instance["conn"].cursor()

    logger_instance["cursor"].execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            logger TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            header TEXT NOT NULL,
            message TEXT NOT NULL
        )        
    """)

    logger_instance["conn"].commit()

def set_log_level(logger_instance, log_level: int):
    logger_instance["log_level"] = log_level

def set_toggle_file_logging(logger_instance, toggle: bool):
    logger_instance["toggle_file_logging"] = toggle

def set_toggle_db_logging(logger_instance, toggle: bool):
    logger_instance["toggle_db_logging"] = toggle
    if toggle:
        __initialize_db_logger(logger_instance)

def set_file_path(logger_instance, file_path: str):
    logger_instance["file_path"] = file_path

def fatal(logger_instance, message: str):
    if logger_instance["log_level"] > LOG_LEVEL_LOW: return
    __log(logger_instance, __LOG_TYPE_FATAL, message)

def error(logger_instance, message: str):
    if logger_instance["log_level"] > LOG_LEVEL_LOW: return
    __log(logger_instance, __LOG_TYPE_ERROR, message)

def warning(logger_instance, message: str):
    if logger_instance["log_level"] > LOG_LEVEL_MEDIUM: return
    __log(logger_instance, __LOG_TYPE_WARNING, message)

def success(logger_instance, message: str):
    if logger_instance["log_level"] > LOG_LEVEL_HIGH: return
    __log(logger_instance, __LOG_TYPE_SUCCESS, message)

def information(logger_instance, message: str):
    if logger_instance["log_level"] > LOG_LEVEL_ALL: return
    __log(logger_instance, __LOG_TYPE_INFORMATION, message)

def debug(logger_instance, message: str):
    __log(logger_instance, __LOG_TYPE_DEBUG, message)

def trace(logger_instance, message: str):
    frame = inspect.stack()[1]
    filename = frame.filename
    lineno = frame.lineno
    __log(logger_instance, __LOG_TYPE_TRACE, message, filename, lineno)

def __log(logger_instance, log_type: int, message: str, filename = None, lineno = None):
    header: str = ""
    style_ansi: str = ""

    if log_type == __LOG_TYPE_FATAL:
        style_ansi = "\033[1m\033[31m"
        header += "[FATAL]:"
    elif log_type == __LOG_TYPE_ERROR:
        style_ansi = "\033[1m\033[35m"
        header += "[ERROR]:"
    elif log_type == __LOG_TYPE_WARNING:
        style_ansi = "\033[1m\033[93m"
        header += "[WARNING]:"
    elif log_type == __LOG_TYPE_SUCCESS:
        style_ansi = "\033[1m\033[32m"
        header += "[SUCCESS]:"
    elif log_type == __LOG_TYPE_INFORMATION:
        style_ansi = "\033[1m\033[34m"
        header += "[INFORMATION]:"
    elif log_type == __LOG_TYPE_DEBUG and os.getenv("DEBUG") == "1":
        style_ansi = "\033[2m"
        header += "[DEBUG]:"
    elif log_type == __LOG_TYPE_TRACE and filename is not None and lineno is not None and os.getenv("DEBUG") == "1":
        style_ansi = "\033[1m\033[90m"
        header += "[TRACE]: - File Path: " + str(filename) + " - Line Number: " + str(lineno) + " -"

    timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

    if header != "" and style_ansi != "":
        __log_console(logger_instance, timestamp, message, style_ansi, header)
        if logger_instance["toggle_file_logging"]:
            __log_file(logger_instance, timestamp, message, header)
        if logger_instance["toggle_db_logging"]:
            __log_db(logger_instance, timestamp, message, header)

def __log_console(logger_instance, timestamp, message, style_ansi, header):
    print("\033[96m(" + logger_instance["id"] + ") \033[0m" + style_ansi + timestamp, "~", header, message + "\033[0m")

def __log_file(logger_instance, timestamp, message, header):
    if os.path.exists(logger_instance["file_path"]):
        try:
            file = open(logger_instance["file_path"] + str(logger_instance["file_logging_timestamp"]).replace("-", "_") + ".log", "a")
            file.write("(" + logger_instance["id"] + ") " + timestamp + " ~ " + header + " " + message + "\n")
            file.close()
        except Exception as e:
            current_toggle_file_logging = logger_instance["toggle_file_logging"]
            set_toggle_file_logging(False)
            fatal("An error occured... %s" % str(e))
            set_toggle_file_logging(current_toggle_file_logging)
    else:
        current_toggle_file_logging = logger_instance["toggle_file_logging"]
        set_toggle_file_logging(False)
        fatal("File Path for Logger is Not Valid!")
        set_toggle_file_logging(current_toggle_file_logging)

def __log_db(logger_instance, timestamp, message, header):
    if logger_instance["conn"] is not None and logger_instance["cursor"] is not None:
        logger_instance["cursor"].execute("INSERT INTO logs (logger, timestamp, header, message) VALUES (?, ?, ?, ?)",
                            (str(logger_instance["id"]), str(timestamp), str(header), str(message)))
        logger_instance["conn"].commit()