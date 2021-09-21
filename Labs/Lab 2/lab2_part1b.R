# Read in EPI data
EPI <- read.csv('DataAnalyticsFall2021_Jonathan_Harris/Data/EPI_data.csv')
attach(EPI)

# Remove NA values 
tf <- is.na(EPI$EPI)
e <- EPI$EPI[!tf]