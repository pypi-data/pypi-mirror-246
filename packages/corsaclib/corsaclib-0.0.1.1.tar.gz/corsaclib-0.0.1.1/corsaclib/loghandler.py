"""
This module implements the main functionality of corsaclib.

Author: Marijn van Dijk
"""

import codecs
import json
import hashlib
import os
import pyspx.shake_256f as sphincs
import queue
import threading
import time
import uuid
import yaml

from Crypto.Cipher import AES
from Crypto.Util import Padding

from corsaclib.utils import FileType, secure_delete

class LogHandler:
    """
    Class for the LogHandler.
    This class is used to handle all the logging and file activity.

    Attributes
    ----------

    Methods
    -------
    """

    def __init__(self,
                 config_file="config.json",
                 filetype=FileType.JSON,
                 delete_config=True,
                 directory="logs",
                 create_directory=True,
                 logchain_size=1000) -> None:
        """
        Creates a new instance of LogHandler.

        ### Parameters

        configfile : str
            The path to the configuration file.
        filetype : FileType
            The type of the configuration file.
            json or yaml.
        deleteconfig : bool
            Whether the configuration file should be scrubbed after loading.
        directory : str
            The directory where the logs are stored.
        create_directory : bool
            Whether the directory should be created.
        logchain_size : int
            The maximum amount of logs that will be stored in one file.
        """

        self._config_file = config_file
        self._filetype = filetype
        self._create_directory = create_directory
        self._directory = directory
        self._delete_config = delete_config
        self._logchain_size = logchain_size
        self._queue = queue.Queue()
        self._load_config()
        self._verify_config()
        self._key = ""
        self._update_key(initialized=False)
        self._initialize_logs()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def _load_config(self) -> None:
        """
        Loads the configuration file.
        """
        try:
            filetype = FileType(self._filetype)
        except ValueError:
            raise ValueError(f"Invalid filetype. Expected one of {list(FileType.__members__.keys())}")

        if (os.path.isfile(self._config_file) == False):
            raise FileNotFoundError(f"The configuration file ({self._config_file}) could not be located at the specified path.")
        
        config = open(self._config_file, "r").read()

        if (filetype == FileType.JSON):
            self._config = json.loads(config)

        elif (filetype == FileType.YAML):
            self._config = yaml.safe_load(config)

        else:
            raise ValueError(f"The filetype ({self._filetype}) is not supported.")
        
        if (self._delete_config): secure_delete(self._config_file)

    def _verify_config(self) -> None:
        """
        Verifies the configuration is correct
        """
        if ('devicename' not in self._config.keys() or 'chainid' not in self._config.keys()
            or 'chainroot' not in self._config.keys() or 'sig' not in self._config.keys()):
            raise ValueError(f"Config does not hold all expected keys: {['devicename', 'chainid', 'chainroot', 'sig']}")
        
    def _initialize_logs(self) -> None:
        """
        Initializes the log and sets handle to file.
        """
        if (self._create_directory and os.path.isdir(self._directory)):
            raise FileExistsError(f"The directory ({self._directory}) already exists.")
        elif (self._create_directory and os.path.isdir(self._directory) == False):
            os.mkdir(self._directory)
        elif (self._create_directory == False and os.path.isdir(self._directory) == False):
            raise ValueError(f"The directory for logging ({self._directory}) does not exist. Please check the arguments to LogHandler.")

        self._logchain_uuid = str(uuid.uuid4()).replace('-', '')
        self._chain_link = 1
        self._log_number = 0
        self._cur_log_count = 0
        filename = f"{self._logchain_uuid}-{str(self._log_number)}.log"
        self._cur_log_path = os.path.join(self._directory, filename)
        self._cur_log_file = open(self._cur_log_path, "a+")

    def _update_key(self, initialized=True) -> None:
        """
        Updates the key
        """
        h = hashlib.sha256()
        if (initialized == False):
            h.update(bytes(self._config["chainroot"], 'utf8'))
            self._key = h.hexdigest()
            del self._config["chainroot"]
        else:
            h.update(bytes(self._key, 'utf8'))
            self._key = h.hexdigest()


    def _check_logfile(self) -> None:
        """
        Checks if a new logfile should be created.
        """
        if (self._cur_log_count >= self._logchain_size):
            self._cur_log_file.close()
            self._log_number += 1
            self._cur_log_count = 0
            filename = f"{self._logchain_uuid}-{str(self._log_number)}.log"
            self._cur_log_path = os.path.join(self._directory, filename)
            self._cur_log_file = open(self._cur_log_path, "a+")

    def _worker(self):
        """
        Gets a log from the queue to encrypt and sign
        """
        while True:
            try:
                log = self._queue.get()
                data = json.dumps(log).encode("utf8")
                padded_data = Padding.pad(data, AES.block_size)
                encrypter = AES.new(bytes.fromhex(self._key), AES.MODE_CBC)
                self._update_key()
                cipher = encrypter.encrypt(padded_data)
                iv = encrypter.iv
                signature = sphincs.sign(cipher + iv, bytes.fromhex(self._config["sig"]["private"]))
                del log["data"]
                logdata = {}
                logdata.update(log)
                logdata["cipher"] = codecs.encode(cipher, 'hex').decode('utf8')
                logdata["iv"] = codecs.encode(iv, 'hex').decode('utf8')
                logdata["sig"] = codecs.encode(signature, 'hex').decode('utf8')
                self._cur_log_file.write(f"{json.dumps(logdata)}\n")
                self._queue.task_done()
            except Exception as e:
                print(f"[FATAL] Failed to log: {e}")
                self._queue.task_done()

    def log(self, data: dict, join_queue: bool=True) -> None:
        """
        Writes a log to the current log file.

        ### Parameters
        
        log : dict
            The log to write.
        join_queue : bool
            Whether to process all items in the log queue.
            A blocking operation.
        """
        self._check_logfile()
        log = {}
        log["timestamp"] = time.time().__round__()
        log["device_name"] = self._config["devicename"]
        log["chain_id"] = self._config["chainid"]
        log["chain_link"] = self._chain_link
        log["data"] = data
        self._chain_link += 1
        self._cur_log_count += 1
        self._queue.put(log)
        if (join_queue): self._queue.join()