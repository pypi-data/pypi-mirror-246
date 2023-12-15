import os
from google.cloud import bigquery
from google.cloud import storage
import pandas as pd

class GcpBigQuery:
    """
    Instantiate a GCP BigQuery connector.

    Args:
        credential_file (str): Credential json file
        quota_project (str): Quota project ID
        proxy (str): Proxy address
    """
    def __init__(self, credential_file, quota_project, proxy=''):
        self.credential_file = credential_file
        self.proxy = proxy
        self.quota_project = quota_project
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_file
        if proxy != '':
            os.environ['HTTP_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy

    def query_to_dataframe(self, query, timeout=3600, method=1):
        """
        Submit query to BigQuery and store result into pandas dataframe

        Args:
            query (str): SQL query
            timeout (int): Query timeout in seconds
            method (int): API that will be used to query (1: google-cloud-bigquery, 2: pandas-gbq)

        Returns:
            result (dataframe)): Result in pandas dataframe
        """
        df = pd.DataFrame()
        bqclient = bigquery.Client(project=self.quota_project)
        query_job = bqclient.query(query)
        if method == 2:
            df = pd.read_gbq(query=query, project_id=self.quota_project)
        else:
            rows = list(query_job.result(timeout=timeout))
            df = pd.DataFrame(data=[list(x.values()) for x in rows], columns=list(rows[0].keys()))
        return df

    def query_non_dql(self, query):
        """
        Submit non Data Query Language (DQL) type of query to BigQuery. Example: CREATE, DROP, TRUNCATE, INSERT, UPDATE, DELETE

        Args:
            project_id (str): Project ID
            query (str): SQL query

        Returns:
            result (result): Iterator of row data. Reference: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJob.html?highlight=job%20result#google.cloud.bigquery.job.QueryJob.result
        """
        bqclient = bigquery.Client(project=self.quota_project)
        query_job = bqclient.query(query)
        results = query_job.result()
        return results

    def bq_export_table_to_gcs(self, project_id, dataset_id, table_id, gcs_uri, format='CSV', delimiter=',', enable_compression=True, compression='GZIP', overwrite=True, region='northamerica-northeast1'):
        """
        Export BigQuery table into Google Cloud Storage (GCS)

        Args:
            project_id (str): Project ID
            table_id (str): Table ID
            dataset_id (str): Dataset ID
            gcs_uri (str): GCS URI as destination. Example: 'gs://my-bucket/my-dir/tickets-20220101-*.csv.gz'
            format (str): File format (CSV, JSON, Avro, Parquet). Default: 'CSV'
            delimiter (str): CSV delimiter character. Default: ','
            enable_compression (boolean): Files will be compressed if the value is True. Default: True
            compression (str): Compression format. Default: GZIP. Reference: https://cloud.google.com/bigquery/docs/exporting-data#export_formats_and_compression_types
            overwrite (boolean): GCS URI destination will be overwritten if the value is True. Default: True
            region (str): Region to run the process. Default: 'northamerica-northeast1'

        Returns:
            result (result): Iterator of row data. Reference: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJob.html?highlight=job%20result#google.cloud.bigquery.job.QueryJob.result
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        table_ref = dataset_ref.table(table_id)
        job_config = bigquery.job.ExtractJobConfig()
        if enable_compression == True:
            if compression == 'DEFLATE':
                job_config.compression = bigquery.Compression.DEFLATE
            if compression == 'SNAPPY':
                job_config.compression = bigquery.Compression.SNAPPY
            else:
                job_config.compression = bigquery.Compression.GZIP

        extract_job = bqclient.extract_table(table_ref, gcs_uri, location=region, job_config=job_config)
        results = extract_job.result()
        return results

    # Load dataframe into BigQuery table
    def bq_load_dataframe(self, project_id, dataset_id, table_id, dataframe, write_disposition='WRITE_TRUNCATE', location='northamerica-northeast1'):
        """
        Load dataframe into BigQuery table

        Args:
            project_id (str): Project ID
            table_id (str): Table ID
            dataset_id (str): Dataset ID
            dataframe (dataframe): Dataframe to be loaded
            write_disposition (str): Write disposition. Default: 'WRITE_TRUNCATE'. Options: 'WRITE_TRUNCATE', 'WRITE_APPEND', 'WRITE_EMPTY'
            location (str): Region to run the process. Default: 'northamerica-northeast1'

        Returns:
            result (result): Iterator of row data. Reference: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJob.html?highlight=job%20result
        """
        bqclient = bigquery.Client(project=project_id)
        dataset_ref = bqclient.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = write_disposition
        job_config.location = location
        job = bqclient.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
        results = job.result()
        return results
    

    # Get list of tables in a dataset
    def get_table_list(self, project_id, dataset_id):
        """
        Get list of tables in a dataset

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID

        Returns:
            result (list): List of tables in a dataset
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        tables = bqclient.list_tables(dataset_ref)
        table_list = [table.table_id for table in tables]
        return table_list
    
    # Get list of datasets in a project
    def get_dataset_list(self, project_id):
        """
        Get list of datasets in a project

        Args:
            project_id (str): Project ID

        Returns:
            result (list): List of datasets in a project
        """
        bqclient = bigquery.Client(project=project_id)
        datasets = bqclient.list_datasets()
        dataset_list = [dataset.dataset_id for dataset in datasets]
        return dataset_list
    
    # Get list of partitions in a table
    def get_table_properties(self, project_id, dataset_id, table_id):
        """
        Get table properties

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (list): List of partitions in a table
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = bqclient.get_table(table_ref)
        return table

    # Get users who have access to a dataset
    def get_dataset_access(self, project_id, dataset_id):
        """
        Get users who have access to a dataset

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID

        Returns:
            result (list): List of users who have access to a dataset
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        dataset = bqclient.get_dataset(dataset_ref)
        access_list = dataset.access_entries
        return access_list
    
    # Get users who have access to a table
    def get_table_access(self, project_id, dataset_id, table_id):
        """
        Get users who have access to a table

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (list): List of users who have access to a table
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = bqclient.get_table(table_ref)
        access_list = table.access_entries
        return access_list
    
    # Get table schema
    def get_table_schema(self, project_id, dataset_id, table_id):
        """
        Get table schema

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (List of SchemaField): Table schema object
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = bqclient.get_table(table_ref)
        schema = table.schema
        return schema
    
    # Get table schema and export to a dataframe
    def get_table_schema_to_dataframe(self, project_id, dataset_id, table_id):
        """
        Get table schema and export to a dataframe

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (dataframe): Table schema in a dataframe
        """
        schema = self.get_table_schema(project_id, dataset_id, table_id)
        field_list = []
        for field in schema:
            field_list.append({'name': field.name, 'type': field.field_type, 'mode': field.mode, 'description': field.description})
        df = pd.DataFrame(field_list)
        return df
    
    # Get table description
    def get_table_description(self, project_id, dataset_id, table_id):
        """
        Get table description
        
        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (str): Table description
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = bqclient.get_table(table_ref)
        description = table.description
        return description
    
    # Get row count of a table
    def get_table_row_count(self, project_id, dataset_id, table_id):
        """
        Get row count of a table

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (int): Row count of a table
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = bqclient.get_table(table_ref)
        row_count = table.num_rows
        return row_count
    
    # Get table size in bytes
    def get_table_size(self, project_id, dataset_id, table_id):
        """
        Get table size in bytes

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (int): Table size in bytes
        """
        bqclient = bigquery.Client(project=self.quota_project)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = bqclient.get_table(table_ref)
        size = table.num_bytes
        return size
    

    # Get the partitions information of a dataset
    def get_dataset_partitions(self, project_id, dataset_id, export_to_dict=False):
        """
        Get partition list of a dataset

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            export_to_dict (boolean): Export result to dictionary. Default: False

        Returns:
            result (dataframe): Dataframe of partitions information in a dataset
        """
        query = f"SELECT * FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS"
        result = self.query_to_dataframe(query, timeout=3600, method=1)
        if export_to_dict == True:
            result = result.to_dict(orient='records')
        return result
    
    # Get the partitions information of a table
    def get_table_partitions(self, project_id, dataset_id, table_id, export_to_dict=False):
        """
        Get partition list of a table

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID
            export_to_dict (boolean): Export result to dictionary. Default: False

        Returns:
            result (dataframe): Dataframe of partitions information in a table
        """
        query = f"SELECT * FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS WHERE table_name = '{table_id}'"
        result = self.query_to_dataframe(query, timeout=3600, method=1)
        if export_to_dict == True:
            result = result.to_dict(orient='records')
        return result

    # Get partition list of a table
    def get_table_partition_list(self, project_id, dataset_id, table_id):
        """
        Get partition list of a table

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (list): List of partitions in a table
        """
        query = f"""SELECT FORMAT_DATE("%Y-%m-%d", PARSE_DATE("%Y%m%d", partition_id)) partition_id FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS WHERE table_name = '{table_id}' AND partition_id != '__NULL__' ORDER BY partition_id DESC"""
        df = self.query_to_dataframe(query, timeout=3600, method=1)
        result = df['partition_id'].tolist()
        return result
    
    # Get the latest partition of a table
    def get_table_latest_partition(self, project_id, dataset_id, table_id):
        """
        Get the latest partition of a table

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (str): Latest partition of a table
        """
        query = f"""SELECT FORMAT_DATE("%Y-%m-%d", PARSE_DATE("%Y%m%d", partition_id)) partition_id FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS WHERE table_name = '{table_id}' AND partition_id != '__NULL__' ORDER BY partition_id DESC LIMIT 1"""
        df = self.query_to_dataframe(query, timeout=3600, method=1)
        result = df['partition_id'].iloc[0]
        return result
    
    # Get the row count of latest partition of a table
    def get_table_latest_partition_row_count(self, project_id, dataset_id, table_id):
        """
        Get the row count of latest partition of a table

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (int): Row count of latest partition of a table
        """
        query = f"""SELECT row_count FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS WHERE table_name = '{table_id}' AND partition_id != '__NULL__' ORDER BY partition_id DESC LIMIT 1"""
        df = self.query_to_dataframe(query, timeout=3600, method=1)
        result = df['row_count'].iloc[0]
        return result
    
    # Get column list of a table
    def get_table_column_list(self, project_id, dataset_id, table_id):
        """
        Get column list of a table

        Args:
            project_id (str): Project ID
            dataset_id (str): Dataset ID
            table_id (str): Table ID

        Returns:
            result (list): List of columns in a table
        """
        query = f"""SELECT column_name FROM {project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_id}'"""
        df = self.query_to_dataframe(query, timeout=3600, method=1)
        result = df['column_name'].tolist()
        return result
    
    