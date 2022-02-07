library(optparse)

# Parse input arguments from AzureML job
options <- list(
  make_option(c("-i", "--input"), default="default value")
)
opt_parser <- OptionParser(option_list = options)
opt <- parse_args(opt_parser)

cat(opt$input)
