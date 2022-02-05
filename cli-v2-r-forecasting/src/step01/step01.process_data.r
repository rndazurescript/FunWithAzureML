# optparse for arguments passed by AzureML job
library(optparse)

# Keyvault and other Azure related libraries
library(AzureAuth)
library(AzureKeyVault)

# Your script libraries
library(RODBC)
library(tseries)

# Parse input arguments from AzureML job
options <- list(
  make_option(c("-s", "--start_date", default=19000101)),
  make_option(c("-k", "--keyvault"), default="mykeyvault"),
  make_option(c("-o", "--output_folder"), default="./output/")
)
opt_parser <- OptionParser(option_list = options)
opt <- parse_args(opt_parser)

# Read keyvault secrets 
kv_token <- get_managed_token("https://vault.azure.net")
vault <- key_vault(opt$keyvault, token=kv_token)
sql_connection_string <- toString(vault$secrets$get('SQL-CONNECTION')$value)

# Connect to SQL Server
SQLServer <- odbcDriverConnect(connection = sql_connection_string)

# Read and process data
my_query <- paste("SELECT [date],[high] FROM [dbo].[stock_daily] where Cast(date as int) >= '", opt$start_date, "'")
sqlResult <- sqlQuery(SQLServer, my_query)
sqlResult$date <- as.Date(as.character(sqlResult$date), format = "%Y%m%d")

min_date <- min(sqlResult$date, na.rm=TRUE)
max_date <- max(sqlResult$date, na.rm=TRUE)
# Log something to see on the logs of the AzureML job
cat("\nNumber of rows:", nrow(sqlResult), "\n")

head(sqlResult)

cat("\nTime series data from ", format(min_date, '%Y-%m-%d'), " to ", format(max_date, '%Y-%m-%d'), "\n")
timeseries_data <- ts(sqlResult$high, start= min_date, end=max_date) 
cat("\nNumber of observations:", length(timeseries_data), "\n")
head(timeseries_data)


# Dump data in intermediate file
saveRDS(timeseries_data, file = file.path(opt$output_folder, "tsdata.rds"))
# To restore the object readRDS(file = "my_data.rds")

close(SQLServer)