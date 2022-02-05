# optparse for arguments passed by AzureML job
library(optparse)

# Your script libraries
library(forecast)

# Parse input arguments from AzureML job
options <- list(
  make_option(c("-d", "--data"), default="./output/"),
  make_option(c("-m", "--model"), default="./output/"),
  make_option(c("-o", "--outputs"), default="./output/")
)
opt_parser <- OptionParser(option_list = options)
opt <- parse_args(opt_parser)

# Read data
data <- readRDS(file = file.path(opt$data, "tsdata.rds"))

# Fitting model using arima model 
fit <- auto.arima(data)

# Dump model in intermediate file
saveRDS(fit, file = file.path(opt$model, "model.rds"))

# Save model summary in intermediate file
png(file.path(opt$outputs,"forecast.png"))
autoplot(forecast(fit))
dev.off()

png(file.path(opt$outputs,"residuals.png"))
checkresiduals(fit)
dev.off()

fcast <- predict(fit, n.ahead=6)
write.csv2(fcast, file.path(opt$outputs, "forecast.csv"))