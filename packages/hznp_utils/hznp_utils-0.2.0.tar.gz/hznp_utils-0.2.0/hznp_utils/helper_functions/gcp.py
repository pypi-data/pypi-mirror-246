# gcp spark helper functions
from pyspark.sql import functions as f
from pyspark.sql.types import StringType, StructField, StructType, BooleanType, DateType, IntegerType, TimestampType, FloatType
import pyspark
import pandas as pd
from fs_gcsfs import GCSFS
from datetime import date, datetime, timezone
import locale
import time
import pickle
from subprocess import PIPE, run, call
import os 
from fs_gcsfs import GCSFS
import json
import hashlib
from datetime import datetime
import pytz
import time
import pandas as pd
import yaml
from pathlib import Path
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

infusedproduct = GCSFS(bucket_name="infusedproduct")
horizontherapeutics = GCSFS(bucket_name="horizontherapeutics")

current_time = lambda: time.localtime()
long_date = lambda: time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
short_date = lambda: time.strftime("%Y%m%d", time.localtime())
utc_time = lambda: datetime.now(timezone.utc)


def f_num(number):
    return f"{int(number):n}"


def build_schema(src, raw_schema):
    schema = raw_schema[(raw_schema["source"] == src)].drop(["source"], axis=1)
    schema = StructType(
        [
            StructField(
                schema.loc[column, "field_name"],
                eval(schema.loc[column, "data_type"]),
                True if schema.loc[column, "nullable"] == True else False,
            )
            for column in schema.index
        ]
    )
    return schema

def _get_path_features(path):
    # take in gs://bucket_name/path/to/file
    bucket_name = path.split("/")[2]
    file_path = Path("/".join(path.split("/")[3:]))
    fs = GCSFS(bucket_name=bucket_name)
    if not fs.exists(str(file_path.parent)):
        print('folder does not exist according to file system. create folder with GCSFS')
    print(path, file_path.parent)
    
    return GCSFS(bucket_name=bucket_name), str(file_path)

# write pandas dataframes to google cloud storage
def to_csv(pdf, path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "w") as output_file:
        pdf.to_csv(output_file, **kwargs)


def to_json(pdf, path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "w") as output_file:
        pdf.to_json(output_file, **kwargs)


def to_excel(pdf, path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "wb") as output_file:
        pdf.to_excel(output_file, **kwargs)


def to_pickle(pdf, path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "wb") as output_file:
        pdf.to_pickle(output_file, **kwargs)


def to_parquet(pdf, path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "wb") as output_file:
        pdf.to_parquet(output_file, **kwargs)


def savefig(plt, path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "wb") as output_file:
        plt.savefig(output_file, **kwargs)


# read files from google cloud storage
def read_csv(path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "r") as input_file:
        pdf = pd.read_csv(input_file, **kwargs)
    return pdf


def read_json(path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "r") as input_file:
        pdf = pd.read_json(input_file, **kwargs)
    return pdf


def read_excel(path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "rb") as input_file:
        pdf = pd.read_excel(input_file, **kwargs)
    return pdf


def read_pickle(path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "rb") as input_file:
        pdf = pd.read_pickle(input_file, **kwargs)
    return pdf


def read_parquet(path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "rb") as input_file:
        pdf = pd.read_parquet(input_file, **kwargs)
    return pdf

def read_yaml(path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path) as f:
        conf = yaml.safe_load(f, **kwargs)
    return conf


def save_pickle(pkl, path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "wb") as output_file:
        pickle.dump(pkl, output_file, **kwargs)


def open_pickle(path, **kwargs):
    fs, path = _get_path_features(path)
    with fs.open(path, "rb") as input_file:
        pkl = pickle.load(input_file, **kwargs)
    return pkl


class Timer:
    def __init__(self):
        self.time = time.perf_counter()

    def start(self):
        self.time = time.perf_counter()

    def stop(self):
        self.time = time.perf_counter() - self.time
        return f"{self.time:.3f}"


def get_config(active=False, previous=0, all=False):
    config = read_excel("gs://infusedproduct/config/control_file.xlsx")
    config["version_label"] = config["product_name"] + "_" + config["data_type"]

    if all:
        return config
    if active:
        config = config[config["active"] == 1]

    for i in range(previous):
        remove = (
            config[config["source"].notna()]
            .groupby(["product_name", "data_type"])
            .agg({"date_created": "max"})
            .reset_index()
        )
        remove["remove"] = 1
        config = config.merge(
            remove, "left", ["product_name", "data_type", "date_created"]
        )
        config = config[config["remove"] != 1]
        del config["remove"]

    config = (
        config[config["source"].notna()]
        .groupby(["product_name", "data_type"])
        .agg({"date_created": "max"})
        .reset_index()
        .merge(config, "inner", ["product_name", "data_type", "date_created"])
    )

    return config


def version(version_label, previous=0, config=False):
    if not config:
        config = get_config(active=True, previous=previous)
    return config.loc[(config["version_label"] == version_label), "version_name"].item()


def get_version(version_label, previous=0, config=False):
    if not config:
        config = get_config(previous=previous)

    return config.loc[(config["version_label"] == version_label), "version_name"].item()


def get_schema(version_label, version="", config=False):
    if not config:
        config = get_config(all=True)
    if version == "":
        version = get_version(version_label)
    return config.loc[
        (config["version_label"] == version_label)
        & (config["version_name"] == version),
        "load_schema",
    ].item()


def lock_data(product, data_type, last_version):

    lock_directory = (
        "gs://infusedproduct/product/"
        + product
        + "/vendor/iqvia/locked_data/"
        + data_type
        + "/"
    )
    fs = infusedproduct

    for x in fs.listdir(
        "/product/"
        + product
        + "/vendor/iqvia/version/"
        + last_version
        + "/"
        + data_type
        + "/raw_data/"
    ):
        if "Fact" in x:
            print(x)
            command = [
                "gsutil",
                "cp",
                "gs://infusedproduct/product/"
                + product
                + "/vendor/iqvia/version/"
                + last_version
                + "/"
                + data_type
                + "/raw_data/"
                + x,
                lock_directory,
            ]
            result = run(command, stdout=PIPE, stderr=PIPE, text=True)
    return 0


def has_column(df, col):
    try:
        df[col]
        return True
    except:
        return False


def prep_dataframe(df, include_id=True):

    if include_id:
        df = df.withColumn("monotonic_row_id", f.monotonically_increasing_id())

    df = df.withColumn("date_created", f.to_date(f.lit(date.today()), "yyyy-MM-dd"))

    if "month_id" in df.columns:
        df = df.withColumn("month_id", f.to_date("month_id", "yyyyMM"))
    if "svc_date" in df.columns:
        df = df.withColumn("svc_date", f.to_date("svc_date", "yyyyMMdd"))
    return df


def prep_dataframe_remit(df, include_id=True):

    if include_id:
        df = df.withColumn("monotonic_row_id", f.monotonically_increasing_id())

    df = df.withColumn("date_created", f.to_date(f.lit(date.today()), "yyyy-MM-dd"))

    if "month_id" in df.columns:
        df = df.withColumn("month_id", f.to_date("month_id", "yy-MM-dd"))
    if "svc_date" in df.columns:
        df = df.withColumn("svc_date", f.to_date("svc_date", "yy-MM-dd"))
    return df


class PathController:
    """
    PathController is used as a helper object that will give all paths for the specified market
    """

    def __init__(
        self,
        mode: str,
        market: str,
        vendor: str,
        data_type: str,
        version: str,
        bucket_prefix="gs://infusedproduct/",
    ):
        """
        Constructs a PathController object which will contain everything needed for the specific paths

        Args:
            mode (str): Specify wether 'dev' or 'prod'
            market (str): Specify the drug market 'kxx','tep', or 'upz'
            vendor (str): Specify data vendor, 'iqvia', 'veeva', 'hznp' etc...
            data_type (str): Specify data type, general use is lrx
            version (str): Which data version to use. Monthly releases follow yyyy(m)mm format example 2020m01 for jan 2020
            bucket_prefix (str, optional): which bucket is being used in gcp. Defaults to 'gs://infusedproduct/'.
        """
        self.raw_dir = f"{mode}/{market}/{vendor}/{data_type}/{version}/raw/"
        self.full_dir = f"{mode}/{market}/{vendor}/{data_type}/{version}/full/"
        self.info_dir = f"{mode}/{market}/{vendor}/{data_type}/{version}/info/"
        self.stage_dir = f"{mode}/{market}/{vendor}/{data_type}/{version}/stage/"
        self.proc_dir = f"{mode}/{market}/{vendor}/{data_type}/{version}/processed/"

        self.raw_path = f"{bucket_prefix}{self.raw_dir}"
        self.full_path = f"{bucket_prefix}{self.full_dir}"
        self.info_path = f"{bucket_prefix}{self.info_dir}"
        self.stage_path = f"{bucket_prefix}{self.stage_dir}"
        self.proc_path = f"{bucket_prefix}{self.proc_dir}"

        if not infusedproduct.exists(self.raw_dir):
            print("version has no raw dir ")
        if not infusedproduct.exists(self.full_dir):
            print("version has no full dir ")
        if not infusedproduct.exists(self.info_dir):
            print("version has no info dir ")
        if not infusedproduct.exists(self.stage_dir):
            print("version has no stage dir ")
        if not infusedproduct.exists(self.proc_dir):
            print("version has no processed dir ")

    def makedirs(self):
        """
        Creates all directories for the PathController if they do not already exist
        """
        for x in [
            self.raw_dir,
            self.full_dir,
            self.info_dir,
            self.stage_dir,
            self.proc_dir,
        ]:
            if not infusedproduct.exists(x):
                infusedproduct.makedirs(x)
                print(x, "created")

    def info(self):
        """
        Prints info of the PathController
        """
        print(
            self.bucket_prefix,
            self.mode,
            self.market,
            self.vendor,
            self.data_type,
            self.version,
        )


def get_dataframe_types(df: pyspark.sql.DataFrame) -> dict:
    """
    Returns a dict of key value pairs of the DataFrames column types

    Args:
        df (pyspark.sql.DataFrame): Any pyspark.sql.DataFrame DataFrame

    Returns:
        dict: Key value pairs of the name and type of the DataFrame
    """
    dictionary = {}
    for col in df.schema:
        dictionary[col.name] = type(col.dataType).__name__ + "()"
    return dictionary


def calc_patient_id(df: pyspark.sql.DataFrame, cols: list) -> pyspark.sql.DataFrame:
    """_summary_

    Args:
        df (pyspark.sql.DataFrame): _description_
        cols (list): _description_

    Returns:
        pyspark.sql.DataFrame: _description_
    """
    for col in cols:
        assert col in df.columns, f"{col} not in dataframe"

    assert "patient_id" not in df.columns, "patient_id already exists"

    columns = ["patient_id", *df.columns]
    df = df.withColumn("concat_column", f.concat_ws("||", *cols))
    df = df.withColumn("patient_id", f.md5(f.col("concat_column")))
    df = df.withColumn("patient_id", f.upper(f.col("patient_id")))
    return df[columns]


def apply_parquet_schema(df: pyspark.sql.DataFrame, name, schema):
    """
    Used to apply the schema specified in an xlsx to a Pyspark Dataframe

    Args:
        df (_type_): _description_
        name (_type_): _description_
        schema (_type_): _description_

    Returns:
        _type_: _description_
    """
    curr_schema = schema[schema["source"] == name]

    assert len(df.columns) == len(curr_schema), "column number mismatch"

    for i, x in schema.iterrows():
        df = df.withColumnRenamed(x.original_field_name, x.field_name)
    return df


def reload():
    call(
        [
            "gsutil",
            "-m",
            "cp",
            "-r",
            "gs://horizontherapeutics/resources/pythonpackages/*",
            "/pythonpackages",
        ]
    )
def reload_dev():
    name = os.uname()[1].split('-')[0]
    call(
        [
            "mkdir",
            "-p",
            "/pythonpackages/dev/",
        ]
    )
    # gsutil -m rsync -d -ur -x ".git/*"
    call(
        [
            "gsutil",
            "-m",
            "rsync",
            "-d",
            "-ur",
            f"gs://horizontherapeutics/dev/{name}/",
            "/pythonpackages/dev/",
        ]
    )
    call(
        [
            "touch",
            "/pythonpackages/dev/__init__.py",
        ]
    )



fs = GCSFS(bucket_name='horizontherapeutics')
refresh_sql_after = 1
class connect():
    def __init__(self, db, server, azure):
        self.db = db
        self.server = server
        self.azure = azure
        
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def __str__(self):
        return f"db: {self.db}, server: {self.server}, azure: {self.azure}"

def get_file(result_path:str):
    for _ in range(60):
        if fs.exists(result_path):
            if (datetime.now(tz=pytz.utc) - fs.getinfo(result_path, namespaces=["details"]).modified).days < refresh_sql_after:
                with fs.open(result_path, 'rb') as f:
                    return pd.read_parquet(f)
        
        time.sleep(10)
    raise Exception("Timeout")
    
def read_sql(query:str, conn:connect):
    request = {"query":query, "conn":conn.to_json()}
    hashed_string = hashlib.sha256(json.dumps(request).encode()).hexdigest()
    output = f"auto_queries/results/{hashed_string}.parquet"
    if not fs.exists(output):
        with fs.open(f"auto_queries/requested/{hashed_string}.json", "w") as f:
            json.dump(request, f)
    elif (datetime.now(tz=pytz.utc) - fs.getinfo(output, namespaces=["details"]).modified).days >= refresh_sql_after:
        with fs.open(f"auto_queries/requested/{hashed_string}.json", "w") as f:
            json.dump(request, f)
    return get_file(output)


if __name__ == "__main__":
    print("for import only")