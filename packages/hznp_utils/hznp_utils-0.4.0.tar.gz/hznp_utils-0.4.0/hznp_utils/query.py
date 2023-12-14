import helper_functions as hf
import pyspark.sql.functions as f
import pandas as pd
pd.set_option('display.max_columns', None)
from IPython.core.magic import (register_line_magic,
                                    register_cell_magic)
from IPython.core.display import HTML, display
from pyspark.sql import SparkSession
 
spark = SparkSession.builder.getOrCreate()

@register_cell_magic
def query(line, cell):
    if spark.sql(cell).count() > 2_000_000:
        print("Query returned too many rows. Please limit to 2 million rows or less.")
    else:
        df = spark.sql(cell).toPandas()
        if line:
            hf.to_excel(df, f'queries/{line}.xlsx',index=False)
            display(HTML(f"""<div><a href='https://storage.cloud.google.com/horizontherapeutics/queries/{line}.xlsx'>Download {line}.xlsx</a></div>"""))
        return df

def register_tables(tables):
    for key in tables:
        try:
            df = spark.read.parquet(tables[key])
            df.createOrReplaceTempView(key)
        except:
            print(f"Could not register {key} at {tables[key]}")
    print("Available tables: " )
    pad = max([len(key) for key in tables]) + 2
    
    for key in tables:
        print(key.ljust(pad) + tables[key])

        
tables_old = {
          "kxx_claims":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/processed_tables/claims_table.parquet",
          "kxx_detail_match_result":f"gs://horizontherapeutics/data/sql_push/current/kxx_detail_match_result.parquet",
          "kxx_detail_remit_claims":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/full_data/dxfact.parquet",
          "kxx_detail_plan":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/full_data/plan.parquet",
          "kxx_detail_providers":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/full_data/provider.parquet",
          "kxx_detail_rx_claims":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/full_data/rxfact.parquet",
          "kxx_detail_diagnosis":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/full_data/diagnosis.parquet",
          "kxx_detail_product":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/full_data/product.parquet",
          "kxx_detail_procedure":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/full_data/procedure.parquet",
          "kxx_patients":f"gs://infusedproduct/product/kxx/vendor/iqvia/version/2023m09/lrx/processed_tables/patient_table.parquet",
          "tep_claims":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/processed_tables/claims_table.parquet",
          "tep_detail_match_result":f"gs://horizontherapeutics/data/sql_push/current/tep_detail_match_result.parquet",
          "tep_detail_remit_claims":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/full_data/dxfact.parquet",
          "tep_detail_plan":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/full_data/plan.parquet",
          "tep_detail_providers":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/full_data/provider.parquet",
          "tep_detail_rx_claims":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/full_data/rxfact.parquet",
          "tep_detail_diagnosis":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/full_data/diagnosis.parquet",
          "tep_detail_product":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/full_data/product.parquet",
          "tep_detail_procedure":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/full_data/procedure.parquet",
          "tep_patients":f"gs://infusedproduct/product/tep/vendor/iqvia/version/2023m09/lrx/processed_tables/patient_table.parquet",
          "upz_claims":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/processed_tables/claims_table.parquet",
          "upz_detail_remit_claims":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/full_data/dxfact.parquet",
          "upz_detail_plan":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/full_data/plan.parquet",
          "upz_detail_providers":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/full_data/provider.parquet",
          "upz_detail_rx_claims":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/full_data/rxfact.parquet",
          "upz_detail_diagnosis":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/full_data/diagnosis.parquet",
          "upz_detail_product":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/full_data/product.parquet",
          "upz_detail_procedure":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/full_data/procedure.parquet",
          "upz_patients":f"gs://infusedproduct/product/upz/vendor/iqvia/version/2023m09/lrx/processed_tables/patient_table.parquet",
      }

tables = {
    "kxx_claims": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/processed/claims_table.parquet",
    "kxx_detail_match_result": f"gs://horizontherapeutics/data/sql_push/current/kxx_detail_match_result.parquet",
    "kxx_detail_remit_claims": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/full/dxfact.parquet",
    "kxx_detail_plan": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/full/plan.parquet",
    "kxx_detail_providers": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/full/provider.parquet",
    "kxx_detail_rx_claims": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/full/old_rxfact.parquet",
    "kxx_detail_diagnosis": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/full/diagnosis.parquet",
    "kxx_detail_product": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/full/product.parquet",
    "kxx_detail_procedure": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/full/procedure.parquet",
    "kxx_patients": f"gs://infusedproduct/dev/kxx/iqvia/lrx/{hf.get_version('kxx_lrx')}/processed/patient_table.parquet",
    "tep_claims": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/processed/claims_table.parquet",
    "tep_detail_match_result": f"gs://horizontherapeutics/data/sql_push/current/tep_detail_match_result.parquet",
    "tep_detail_remit_claims": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/full/dxfact.parquet",
    "tep_detail_plan": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/full/plan.parquet",
    "tep_detail_providers": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/full/provider.parquet",
    "tep_detail_rx_claims": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/full/old_rxfact.parquet",
    "tep_detail_diagnosis": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/full/diagnosis.parquet",
    "tep_detail_product": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/full/product.parquet",
    "tep_detail_procedure": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/full/procedure.parquet",
    "tep_patients": f"gs://infusedproduct/dev/tep/iqvia/lrx/{hf.get_version('tep_lrx')}/processed/patient_table.parquet",
    "upz_claims": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/processed/claims_table.parquet",
    "upz_detail_remit_claims": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/full/dxfact.parquet",
    "upz_detail_plan": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/full/plan.parquet",
    "upz_detail_providers": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/full/provider.parquet",
    "upz_detail_rx_claims": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/full/old_rxfact.parquet",
    "upz_detail_diagnosis": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/full/diagnosis.parquet",
    "upz_detail_product": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/full/product.parquet",
    "upz_detail_procedure": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/full/procedure.parquet",
    "upz_patients": f"gs://infusedproduct/dev/upz/iqvia/lrx/{hf.get_version('upz_lrx')}/processed/patient_table.parquet"
    

}

register_tables(tables)