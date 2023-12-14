

import pandas as pd
import os

from pyspark.sql import SparkSession
import pyspark
try:
    from delta import DeltaTable
except:
    print('no delta')
import yaml
 
spark = SparkSession.builder.getOrCreate()
try:
    from pyspark.dbutils import DBUtils
    dbutils = DBUtils(spark)
    from ds.helper_functions.komodo import *
except:
    from ds.helper_functions.gcp import *

    print('no dbutils')
    
def sys_type():
    try:
        if dbutils:
            with open('/dbfs/FileStore/tables/config/SYSTEM_TYPE','r') as f:
                return f.read()
        else:
            return 'NOT RECOGNIZED'
    except:
        return 'GCP'
    
is_komodo = sys_type() == "KOMODO"
is_gcp = sys_type() == "GCP"

def bucket_prefix():
    if is_komodo:
        return 'dbfs:/'
    elif is_gcp:
        return 'gs://'
    else:
        return ''