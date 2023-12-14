import pandas as pd
import os

from pyspark.sql import SparkSession
import pyspark
from delta import DeltaTable
import yaml
 
spark = SparkSession.builder.getOrCreate()
try:
    from pyspark.dbutils import DBUtils
    dbutils = DBUtils(spark)
except:
    print('no dbutils')

file_import = '/dbfs/mnt/import/import/'
file_export = '/dbfs/mnt/export/auto-exports/'
spark_import = 'dbfs:/mnt/import/import/'
spark_export = 'dbfs:/mnt/export/auto-exports/'
dbutils_import = '/mnt/import/import/'
dbutils_export = '/mnt/export/auto-exports/'



def add_file_prefix(path):
    assert check_path(path), "Do not include dbfs:, gs:, s3:, or / at begining of path"
    if is_komodo:
        return f'/dbfs/{path}'
    elif is_gcp:
        return ''
    else:
        return ''

def bucket_prefix():
    if is_komodo:
        return 'dbfs:/'
    elif is_gcp:
        return 'gs://'
    else:
        return ''

def read_yaml(path):
    with open(add_file_prefix(path)) as f:
        return yaml.safe_load(f)

def check_path(path:str) -> bool:
    """Checks if path is valid for write/reading table for platform datastorage

    Args:
        path (str): Path to check

    Returns:
        bool: If path is a valid path
    """
    if path[:5] in ['dbfs:','/dbfs','dbfs/']:
        return False
    elif path[:3] in ['gs:','s3:']:
        return False
    elif path[0] == '/':
        return False
    else:
        return True

def is_mounted(drive):
    try:
        dbutils.fs.ls(f'/mnt/{drive}')
        return True
    except Exception as e:
        return False
    
def mount_drives():
    if is_komodo:
        for drive in ['import','export']:
            if not is_mounted(drive):
                aws_bucket_name = f'kh-sentinel-horizon-{drive}'

                dbutils.fs.mount(f"s3a://{aws_bucket_name}",f"/mnt/{drive}")
                display(dbutils.fs.ls(f"/mnt/{drive}"))
            print(f'{drive} mounted')
def get_user():
    if is_gcp:
        return 'no_user'
    else:
        return dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get().split('@')[0]

def dir_exists(path):
    try:
        dbutils.fs.ls(path)
        return True
    except Exception as e:
        return False

def read_csv(file_path, fs="horizontherapeutics", **kwargs):
    if fs == 'horizontherapeutics':
        prefix = '/dbfs/FileStore/'
    elif fs == 'infusedproduct':
        prefix = '/dbfs/infusedproduct/'
    with open(prefix + file_path, "r") as input_file:
        pdf = pd.read_csv(input_file, **kwargs)
    return pdf

def read_excel(file_path, fs="horizontherapeutics", **kwargs):
    if fs == 'horizontherapeutics':
        prefix = '/dbfs/FileStore/'
    elif fs == 'infusedproduct':
        prefix = '/dbfs/infusedproduct/'
    with open(prefix + file_path, "rb") as input_file:
        pdf = pd.read_excel(input_file, **kwargs)
    return pdf

def read_pickle(file_path, fs="horizontherapeutics", **kwargs):
    if fs == 'horizontherapeutics':
        prefix = '/dbfs/FileStore/'
    elif fs == 'infusedproduct':
        prefix = '/dbfs/infusedproduct/'
    with open(prefix + file_path, "rb") as input_file:
        pdf = pd.read_pickle(input_file, **kwargs)
    return pdf

def read_parquet(file_path, fs="horizontherapeutics", **kwargs):
    if fs == 'horizontherapeutics':
        prefix = '/dbfs/FileStore/'
    elif fs == 'infusedproduct':
        prefix = '/dbfs/infusedproduct/'
    with open(prefix + file_path, "rb") as input_file:
        pdf = pd.read_parquet(input_file, **kwargs)
    return pdf

def to_csv(pdf, path, fs="horizontherapeutics", **kwargs):
    if fs == 'horizontherapeutics':
        prefix = '/dbfs/FileStore/'
    elif fs == 'infusedproduct':
        prefix = '/dbfs/infusedproduct/'
    if path[0]== '/':
        path = path[1:]
    path = prefix + path
    path_dir = '/'.join(path.split('/')[2:-1])
    if not dir_exists(path_dir):
        print('creating',path_dir)
        dbutils.fs.mkdirs(path_dir)
        
    with open(path, "w") as output_file:
        pdf.to_csv(output_file, **kwargs)
        
def to_pickle(pdf, path, fs="horizontherapeutics", **kwargs):
    if fs == 'horizontherapeutics':
        prefix = '/dbfs/FileStore/'
    elif fs == 'infusedproduct':
        prefix = '/dbfs/infusedproduct/'
    if path[0]== '/':
        path = path[1:]
    path = prefix + path
    path_dir = '/'.join(path.split('/')[2:-1])
    if not dir_exists(path_dir):
        print('creating',path_dir)
        dbutils.fs.mkdirs(path_dir)
        
    with open(path, "wb") as output_file:
        pdf.to_pickle(output_file, **kwargs)

def to_parquet(pdf, path, fs="horizontherapeutics", **kwargs):
    if fs == 'horizontherapeutics':
        prefix = '/dbfs/FileStore/'
    elif fs == 'infusedproduct':
        prefix = '/dbfs/infusedproduct/'
    if path[0]== '/':
        path = path[1:]
    path = prefix + path
    path_dir = '/'.join(path.split('/')[2:-1])
    if not dir_exists(path_dir):
        print('creating',path_dir)
        dbutils.fs.mkdirs(path_dir)
        
    with open(path, "wb") as output_file:
        pdf.to_parquet(output_file, **kwargs)
        
def get_config(active=False, previous=0, all=False):
    config = read_excel("config/control_file.xlsx", fs="infusedproduct")
    config["version_label"] = config["vendor"] + "_" + config["product_name"] + "_" + config["data_type"]

    if all:
        return config
    if active:
        config = config[config["active"] == 1]

    for i in range(previous):
        remove = (
            config.groupby(["vendor", "product_name", "data_type"])
            .agg({"date_created": "max"})
            .reset_index()
        )
        remove["remove"] = 1
        config = config.merge(
            remove, "left", ["vendor", "product_name", "data_type", "date_created"]
        )
        config = config[config["remove"] != 1]
        del config["remove"]

    config = (
        config.groupby(["vendor", "product_name", "data_type"])
        .agg({"date_created": "max"})
        .reset_index()
        .merge(config, "inner", ["vendor", "product_name", "data_type", "date_created"])
    )

    return config

def get_version(version_label, previous=0, config=False):
    if not config:
        config = get_config(previous=previous)
    try:
        return config.loc[(config["version_label"] == version_label), "version_name"].item()
    except:
        return 'no_version'

def exists(path:str) -> bool:
    """checks if the file or directory exists

    Args:
        path (str): 

    Returns:
        bool: if the path exists or not
    """
    if is_komodo:
        try:
            if dbutils.fs.ls(path):
                return True
            else:
                return False
        except:
            return False
    elif is_gcp:
        ... # to do
    else:
        return False


# distributed compute read write functions

def write_table(spark_df: pyspark.sql.DataFrame, path:str) -> None:
    """ This will save a spark dataframe using the appropriate storage format for the platform being used
        Note: will always overwrite 

    Args:
        spark_df (pyspark.sql.DataFrame): Dataframe to be saved
        path (str): Location of the dataframe to be saved. omit any dbfs:/, gs://, s3://, /
    """
    assert check_path(path), "Do not include dbfs:, gs:, s3:, or / at begining of path"
    spark_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{bucket_prefix()}{path}")

def read_table(path:str) -> pyspark.sql.DataFrame:
    """ Will read a stored table into a spark dataframe

    Args:
        path (str): Location of stored table. omit any dbfs:/, gs://, s3://, /

    Returns:
        pyspark.sql.DataFrame: spark DataFrame of requested table
    """
    assert check_path(path), "Do not include dbfs:, gs:, s3:, or / at begining of path"
    return spark.read.format("delta").load(f"{bucket_prefix()}{path}")
    
def optimize_table(path:str) -> None:
    """Optimizes table stored at path. Works only for delta tables

    Args:
        path (str): Location of deleta table, omit any dbfs:/, gs://, s3://, /
    """
    assert check_path(path), "Do not include dbfs:, gs:, s3:, or / at begining of path"    
    delta_table = DeltaTable.forPath(spark, f"{bucket_prefix()}{path}")
    delta_table.optimize().executeCompaction()

def read_snowflake(query:str) -> pyspark.sql.DataFrame:
    """Will read a query into a spark dataframe

    Args:
        query (str): The query to be run on the snowflake instance

    Returns:
        pyspark.sql.DataFrame: The result of the query
    """
    with open('/dbfs/infusedproduct/config/config.yaml') as f:
        config = yaml.safe_load(f)
    return spark.read.format('snowflake').options(**config['spark_options']).option("query", query).load()

def write_snowflake(spark_df:pyspark.sql.DataFrame, table_name:str, schema:str, mode='overwrite') -> None:
    """Will write spark dataframe into snowflake to {table_name} in the {schema} in the database DSVC_HORIZON_PRIVATE

    Args:
        spark_df (pyspark.sql.DataFrame): Spark dataframe to write
        table_name (str): What table to write to
        schema (str): Which schema the table should be written to
        mode (str, optional): Can specify to append. Defaults to 'overwrite'.
    """
    with open('/dbfs/infusedproduct/config/config.yaml') as f:
        config = yaml.safe_load(f)
    cust_options = config['spark_options']
    cust_options['sfSchema'] = schema
    cust_options['sfDatabase'] = 'DSVC_HORIZON_PRIVATE'
    spark_df.write.format('snowflake').options(**cust_options).option('dbtable',table_name).mode(mode).options(header=True).save()


