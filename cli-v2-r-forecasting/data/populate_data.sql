drop table if exists dbo.stock_daily;

create table [dbo].[stock_daily](
 ticker nvarchar(10)
,per nvarchar(1)
,date nvarchar(8)
,time nvarchar(8)
,[open] money
,high money
,low money
,[close] money
,vol bigint
,openint nvarchar(1)
);

GO

IF EXISTS(SELECT * FROM sys.external_data_sources WHERE name = 'AzureBlobStorageNoKey')
    drop EXTERNAL data source AzureBlobStorageNoKey;

CREATE EXTERNAL DATA SOURCE AzureBlobStorageNoKey
WITH 
(
    TYPE = BLOB_STORAGE,
    LOCATION = '$(StorageUrl)',
);

GO

bulk insert dbo.stock_daily
from '$(FilePath)'
with( DATA_SOURCE = 'AzureBlobStorageNoKey', FORMAT='CSV' , FIRSTROW=2);