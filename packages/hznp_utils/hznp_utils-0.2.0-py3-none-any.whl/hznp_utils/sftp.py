import logging
import logging.config
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from getpass import getpass
import stat

import pandas as pd
import paramiko
from fs_gcsfs import GCSFS
from google.cloud import storage, secretmanager

import helper_functions as hf

gcsfs = GCSFS(bucket_name="infusedproduct")
client = secretmanager.SecretManagerServiceClient()


def connect_sftp():
    """
    Connects to an SFTP server using the host, username, and password stored in the environment variables.
    Call init_sftp() to set these environment variables.

    Returns:
        paramiko.SFTPClient: An SFTP client object connected to the remote server.
    """
    paramiko.util.log_to_file("paramiko.log")

    # # Open a transport
    transport = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ["SFTP_PORT"])))

    # Auth
    transport.connect(None, os.environ["SFTP_USERNAME"], os.environ["SFTP_PASSWORD"])

    # Go!
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp


def init_sftp(host="transfer.veevacompass.com", port='22', username=None, password=None):
    """
    Initializes the SFTP connection with the given host, port, username, and password.

    Args:
        host (str): The hostname or IP address of the SFTP server. Defaults to 'transfer.veevacompass.com'.
        port (int): The port number to use for the SFTP connection. Defaults to 22.
        username (str): The username to use for the SFTP connection. If not provided, the user will be prompted to enter it.
        password (str): The password to use for the SFTP connection. If not provided, the user will be prompted to enter it.

    Returns:
        bool: True if the SFTP connection was successfully established, False otherwise.
    """

    os.environ["SFTP_HOST"] = input(f"Enter sftp host (default: {host}): ") or host
    os.environ["SFTP_PORT"] = input(f"Enter sftp port (default: {port}): ") or port
    
    os.environ["SFTP_USERNAME"] = username or input("Enter Veeva Compass username: ")
    os.environ["SFTP_PASSWORD"] = password or getpass("Enter Veeva Compass password: ")

    try:
        connect_sftp()
        return True
    except Exception as e:
        print(e)
        return False


def mkdir_p(sftp, remote_directory):
    """
    Creates a directory on a remote SFTP server.

    Args:
        sftp (paramiko.SFTPClient): An SFTP client object connected to the remote server.
        remote_directory (str): The directory path to create on the remote server.

    Returns:
        None
    """
    # Normalize the directory path
    remote_directory = os.path.normpath(remote_directory)

    # Split the directory path into individual folders
    dir_folders = remote_directory.split(os.path.sep)

    # Iterate over the folders and create them if they don't exist
    for i, folder in enumerate(dir_folders):
        if folder == "":
            continue
        dir_path = os.path.join(*dir_folders[: i + 1])
        try:
            sftp.listdir(dir_path)
        except FileNotFoundError:
            sftp.mkdir(dir_path)


def get_log_config(log_name: str) -> dict:
    """Returns a logging config dict for use in logging.config.dictConfig

    Args:
        log_name (str): file that will be using the logger

    Returns:
        dict: dict of config for logging streams
    """

    log_path = "/log"

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    LOGGING_CONFIG = {
        "version": 1,
        "loggers": {
            "": {  # root logger
                "level": "NOTSET",
                "handlers": [
                    "info_rotating_file_handler",
                ],
            },
            "my.package": {
                "level": "WARNING",
                "propagate": False,
                "handlers": [
                    "info_rotating_file_handler",
                ],
            },
        },
        "handlers": {
            "info_rotating_file_handler": {
                "level": "WARNING",
                "formatter": "info",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(log_path, f"{log_name}.log"),
                "mode": "a",
                "maxBytes": 1048576,
                "backupCount": 100,
            },
            "error_file_handler": {
                "level": "ERROR",
                "formatter": "error",
                "class": "logging.FileHandler",
                "filename": os.path.join(log_path, "error.log"),
                "mode": "a",
            },
        },
        "formatters": {
            "info": {
                "format": "%(asctime)s-%(levelname)s-%(name)s::|%(lineno)s:: %(message)s"
            },
            "error": {"format": "%(message)s"},
        },
    }

    return LOGGING_CONFIG


def get_logger(log_name: str) -> logging.Logger:
    """Creates a logging object

    Args:
        log_name (str): name of logger


    Returns:
        logging.Logger: the current logger used by the file
    """

    logging.config.dictConfig(get_log_config(log_name))

    # Get the logger specified in the file
    logger = logging.getLogger(log_name)

    return logger


def _sftp_get(conf):
    """
    Downloads a file from an SFTP server, uploads it to Google Cloud Storage, and removes it from the local machine.

    Args:
        conf (dict): A dictionary containing the configuration parameters for the SFTP download.

    Returns:
        None
    """

    gcsfs = GCSFS(bucket_name="infusedproduct")

    with connect_sftp() as sftp:
        # downloads file from sftp
        sftp.get(
            os.path.join(conf["src_path"], conf["file"]),
            os.path.join("/data/", conf["file"]),
        )

    # uploads file to GCP
    with open("/data/" + conf["file"], "rb") as f:
        with gcsfs.open(conf["dest_path"] + conf["file"], "wb") as f_out:
            shutil.copyfileobj(f, f_out)

    # removes file from the host machine
    os.remove("/data/" + conf["file"])


def _sftp_download_files(confs):
    """
    Downloads multiple files from an SFTP server using multiple threads.

    Args:
        confs (list): A list of dictionaries, where each dictionary contains the configuration parameters for an SFTP download.

    Returns:
    """

    threads = []
    start = datetime.now()
    with ThreadPoolExecutor(max_workers=10) as executor:
        percent = 0
        step = 100 / len(confs)

        for conf in confs:
            threads.append(executor.submit(_sftp_get, conf))

        for task in as_completed(threads):
            percent += step
            print("\r{0:.2f}% {1}".format(percent, datetime.now() - start), end="")

        return 0


def sftp_multi_import(src_path, gcp_path):

    try:
        os.makedirs("/data")
    except FileExistsError:
        print("Directory '/data' already exists.")
    except Exception as e:
        print(f"Error creating directory '/data': {e}")

    try:
        gcsfs.mkdir(gcp_path)
    except FileExistsError:
        print(f"Directory '{gcp_path}' already exists in Google Cloud Storage.")
    except Exception as e:
        print(f"Error creating directory '{gcp_path}' in Google Cloud Storage: {e}")

    with connect_sftp() as sftp:
        not_copied = sftp.listdir(src_path)
        not_copied = pd.DataFrame(data={"file": not_copied})

        copied = gcsfs.listdir(gcp_path)
        copied = pd.DataFrame(data={"copied": [1] * len(copied), "file": copied})

        to_copy = copied.merge(not_copied, "outer", "file")
        files = list(to_copy[to_copy["copied"] != 1]["file"])

    confs = []
    for file in files:
        confs.append({"src_path": src_path, "dest_path": gcp_path, "file": file})

    print("there are", len(files), "to download")
    return _sftp_download_files(confs)

def get_pull_confs(sftp, file_path, location_path, gcp_path, base_path, copied=[]):
    confs = []
    for x in sftp.listdir(file_path):
        file_attr = sftp.stat(file_path + x)
        if stat.S_ISDIR(file_attr.st_mode):
            print(file_path+x+'/', location_path+x+'/')
            confs += get_pull_confs(sftp, file_path+x+'/', location_path+x+'/', gcp_path, base_path, copied)
            print(len(confs))
        else:
            if file_path[len(base_path):] + x not in copied:
                confs.append({'src_path':gcp_path,'location_path':location_path,'file':x})
    return confs


def sizeof_fmt(num, suffix="B"):
    """
    Converts a number of bytes to a human-readable format.

    Args:
        num (int): The number of bytes to convert.
        suffix (str, optional): The suffix to use for the converted value. Defaults to "B".

    Returns:
        str: The human-readable representation of the number of bytes.
    """

    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def get_sizes(sftp, path, location_path):
    sizes = []
    for file in sorted(sftp.listdir(path)):
        file_path = path + file
        attr = sftp.stat(file_path)
        if stat.S_ISDIR(attr.st_mode):
            print(file_path)
            sizes += get_sizes(sftp, file_path + "/", location_path)
        else:
            sizes.append(
                {
                    "file": file_path[len(location_path) :],
                    "size": attr.st_size,
                    "modified": attr.st_mtime,
                }
            )
    return sizes


def show_sizes(sftp, gcp_path, location_path):
    sizes = get_sizes(sftp, location_path, location_path)
    if len(sizes) > 0:
        df = pd.DataFrame(data=sizes)
        df["human_size"] = df["size"].apply(sizeof_fmt)
        df["modified"] = pd.to_datetime(df["modified"], unit="s")
    else:
        df = pd.DataFrame()
        print("nosftp")

    if gcp_path[-1] != "/":
        gcp_path += "/"
    gcp_bucket = gcp_path.split("/")[2]
    gcp_path = "/".join(gcp_path.split("/")[3:])
    client = storage.Client()
    start_at = len(gcp_path)
    gcp_size = []
    for blob in client.list_blobs(gcp_bucket, prefix=gcp_path):
        if len(blob.name[start_at:]) > 0:
            gcp_size.append({"file": blob.name[start_at:], "gcp_size": blob.size})
    gcp_df = pd.DataFrame(data=gcp_size)

    if len(df) > 0:
        if len(gcp_df) > 0:
            df = gcp_df.merge(df, "left", "file")
        else:
            df = df.copy()
    else:
        if len(gcp_df) > 0:
            df = gcp_df.copy()
        else:
            df = pd.DataFrame()

    if "size" in list(df.columns):
        copied_size = df["size"].sum()
    else:
        copied_size = 0

    if "gcp_size" in list(df.columns):
        origin_size = df["gcp_size"].sum()
    else:
        origin_size = 0

    if "size" in list(df.columns) and "gcp_size" in list(df.columns):
        df["full_copy"] = df["size"] == df["gcp_size"]

    if origin_size >= copied_size:
        print(
            f"transferred {sizeof_fmt(copied_size)} of {sizeof_fmt(origin_size)} -- {(copied_size/origin_size)*100:.2f}% done"
        )
    else:
        print(
            f"transferred {sizeof_fmt(origin_size)} of {sizeof_fmt(copied_size)} -- {(origin_size/copied_size)*100:.2f}% done"
        )
    return df


## push to sftp
def _sftp_push_files(confs):
    threads = []

    start = datetime.now()
    with ThreadPoolExecutor(max_workers=8) as executor:
        
        
        total = len(confs)
        percent = 0
        step = 100 / total
        done = 0
        
        for conf in confs:
            threads.append(executor.submit(_sftp_push, conf))

        for task in as_completed(threads):
            done += 1
            percent += step
            
            run_time =  datetime.now() - start
            remaining  = total - done
            time_per = run_time.seconds / done
            
            remaining_time = timedelta(seconds=int(time_per * remaining))
            finish_time = datetime.utcnow() + remaining_time
            finish_time = str(finish_time.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('America/Chicago')))
            
            print("\r{0:.2f}% run time {1} est time {2} est finish at {3}".format(percent, run_time, remaining_time, finish_time), end="")
        return 0
        
def sftp_multi_push(confs):
    
    try:
        os.makedirs('/data')
    except:
        print('/data already created')


    print("there are", len(confs), "to upload")
    return _sftp_push_files(confs)

def _sftp_push(conf):
    try:
        start = datetime.now()

        gcsfs = GCSFS(bucket_name="infusedproduct")
        
        source_location = os.path.join(conf["src_path"], conf["file"])
        transit_location = os.path.join('/data', conf['file'])
        dest_location = os.path.join(conf['location_path'], conf['file'])
        
        with gcsfs.open(source_location, "rb") as f:
            with open(transit_location, "wb") as f_out:
                shutil.copyfileobj(f, f_out)
        
        with connect_sftp() as sftp:
            try:
                sftp.listdir(conf['location_path'])
            except:
                mkdir_p(sftp, conf['location_path'])

            logger.error(f"transit from {transit_location} to {dest_location}")

            sftp.put(transit_location, dest_location)

        os.remove(transit_location)
       
    except Exception as e:
        logger.error(json.dumps(conf))
        logger.warning('fail', exc_info=True)

def get_push_confs(file_path, location_path, base_path, coppied=[]):
    confs = []
    for x in hf.infusedproduct.listdir(file_path):
        if hf.infusedproduct.isdir(file_path+x):
            print(file_path+x+'/', location_path+x+'/')
            # print(file_path[len(base_path):] + x)

            confs += get_push_confs(file_path+x+'/', location_path+x+'/', base_path, coppied)
            print(len(confs))
        else:
            # print(file_path[len(base_path):] + x)
            if file_path[len(base_path):] + x not in coppied:
                confs.append({'src_path':file_path,'location_path':location_path,'file':x})
    return confs

def connect_horizon_sftp():
    """
    Connects to an SFTP server using the host, username, and password stored in the environment variables.
    Call init_sftp() to set these environment variables.
 
    Returns:
        paramiko.SFTPClient: An SFTP client object connected to the remote server.
    """
    paramiko.util.log_to_file("paramiko.log")
 
    # # Open a transport
    transport = paramiko.Transport(('ftp.horizontherapeutics.com', 22))
 
    # Auth
    SFTP_USERNAME = client.access_secret_version(request={"name": "projects/511675646729/secrets/horizon_sftp_user/versions/1"}).payload.data.decode("UTF-8")
    SFTP_PASSWORD = client.access_secret_version(request={"name": "projects/511675646729/secrets/horizon_sftp_password/versions/1"}).payload.data.decode("UTF-8")
    transport.connect(None, SFTP_USERNAME, SFTP_PASSWORD)
 
    # Go!
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp
 
def horizon_sftp_push(file, source, dest):
    """copy file from gcp to horizon sftp server
 
    Args:
        file (str): file name to be copied
        source (str): source in gcp in format gs://bucket_name/dir/name
        dest (_type_): dest in sftp server in format /dir/name
    """
    try:
        bucket = source.split('/')[2]
        bucket_path = "/".join(os.path.split('/')[3:])
       
        gcsfs = GCSFS(bucket_name=bucket)
       
        transit_dir = f'/home/{getpass.getuser()}/data'
       
        if not os.path.exists(transit_dir):
            os.mkdir(transit_dir)
           
        source_location = os.path.join(bucket_path, file)
        transit_location = os.path.join(transit_dir, file)
        dest_location = os.path.join(dest, file)
       
        with gcsfs.open(source_location, "rb") as f:
            with open(transit_location, "wb") as f_out:
                shutil.copyfileobj(f, f_out)
       
        with connect_horizon_sftp() as sftp:
            try:
                sftp.listdir(dest)
            # except FileNotFoundError:
            except:
                mkdir_p(sftp, dest)
 
            sftp.put(transit_location, dest_location)
 
        os.remove(transit_location)
 
        print(f"File {file} successfully pushed to Horizon SFTP server at {dest_location}")
    except Exception as e:
        print(e)
