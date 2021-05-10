#!/usr/bin/env Rscript

# This is a sample R script that will be performing an action on top of a file.
library(optparse)

option_list = list( make_option(c("-f", "--file"), 
                                type="character", default=NULL, 
                                help="dataset file name",        
                                metavar="character"),
                    make_option(c("-o", "--out_folder"), 
                                type="character", default="outputs", 
                                help="output folder [default=     
                                      %default]", metavar="character")
                  ); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

if (is.null(opt$file)){
    print_help(opt_parser)
    stop("At least one argument must be supplied (input file).n",    
    call.=FALSE)
}

cat("\nInput file is:", opt$file)
cat("\nOutput folder is:", opt$out_folder)

output_file_name = paste0(basename(opt$file),".csv")

sample_output = data.frame(seq(2))
write.csv2(sample_output, file.path(opt$out_folder, output_file_name))
