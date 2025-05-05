import logging
from pyspark.sql.functions import from_json, col, posexplode
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType, ArrayType

class SparkCreateDataFrameTask:
    """
    Classe pour gérer les tâches de streaming avec Spark, Kafka et BigQuery.
    """

    def create_selection_df_from_kafka(self,spark_df):
        """
        Sélectionne et transforme les données JSON depuis Kafka en colonnes individuelles dans un DataFrame.

        :param spark_df: Le DataFrame Spark contenant les données brutes de Kafka
        :return: Un DataFrame Spark avec les colonnes des données utilisateur
        """
        logging.info("Beginning of Kafka DataFrame transformation...")

        schema = StructType([
            StructField("type", StringType()),
            StructField("incident_id", StringType()),
            StructField("icon_category", IntegerType()),
            StructField("magnitude_of_delay", IntegerType()),
            StructField("start_time", TimestampType()),
            StructField("end_time", TimestampType()),
            StructField("from_location", StringType()),
            StructField("to_location", StringType()),
            StructField("length_meters", DoubleType()),
            StructField("delay_seconds", DoubleType()),
            StructField("time_validity", StringType()),
            StructField("geometry_type", StringType()),
            StructField("coordinates", ArrayType(ArrayType(DoubleType())))
        ])

        try:
            dataframe = (
                spark_df.selectExpr("CAST(value AS STRING)")
                .select(from_json(col('value'), schema).alias('data'))
                .select("data.*")
                # Explosion des coordonnées en lignes puis extraire longitude et latitude en gardant un index pour la reconstitution
                .withColumn("point_index_coordinate", posexplode(col("coordinates")))
                .withColumn("point_index", col("point_index_coordinate").getField("pos"))
                .withColumn("coordinate", col("point_index_coordinate").getField("col"))
                .withColumn("longitude", col("coordinate")[0])
                .withColumn("latitude", col("coordinate")[1])
                .drop("coordinates", "coordinate", "point_index_coordinate")
            )

            logging.info("DataFrame transformed and coordinates exploded successfully!")
            return dataframe

        except Exception as e:
            logging.error(f"Could not transform Kafka DataFrame due to: {e}")
            return None
