import logging

from pyspark.sql.session import SparkSession
from patient_notes.config import TABLE_CONFIG, WORKER_COUNT, CORE_COUNT
from patient_notes.datalake import (
    DatalakeZone,
    construct_uri,
    read_delta_table,
    overwrite_delta_table,
)
from patient_notes.monitoring import initialize_logging
from patient_notes.stages.pseudonymisation.presidio import (
    broadcast_presidio_with_anonymise_udf,
)
from patient_notes.stages.pseudonymisation.transform import pseudo_transform

if __name__ == "__main__":
    spark_session = SparkSession.builder.getOrCreate()
    initialize_logging()

    anonymise_udf = broadcast_presidio_with_anonymise_udf(spark_session)

    for table_name, table_config in TABLE_CONFIG.items():
        logging.info(f"Processing table for pseudonymisation: {table_name}")

        # Read from bronze
        df = read_delta_table(
            spark_session, construct_uri(spark_session, DatalakeZone.BRONZE, table_name)
        )

        if df.isEmpty():
            logging.warning(f"Skipping pseudonymisation for table {table_name} as DF is empty")
        else:
            # Increase partition count for parallel processing
            initial_partitions = df.rdd.getNumPartitions()
            df = df.repartition(max(WORKER_COUNT * CORE_COUNT, initial_partitions))

            # Pseudonymise
            df = pseudo_transform(df, table_name, table_config, anonymise_udf)

        # Write to silver
        overwrite_delta_table(df, construct_uri(spark_session, DatalakeZone.SILVER, table_name))
        logging.info(
            f"Wrote pseudonymisation outputs to {table_name} in Datalake silver zone"
            f" ({df.count()} rows)."
        )