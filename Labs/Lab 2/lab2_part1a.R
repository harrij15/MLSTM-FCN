# Function for mode
Mode <- function(x) {
  u <- unique(x)
  t <- tabulate(match(u,x))
  u[which.max(t)]
}

dev.off()


# Read in EPI data
EPI <- read.csv('DataAnalyticsFall2021_Jonathan_Harris/Data/EPI_data.csv')
attach(EPI)

# Remove NA values 
tf <- is.na(EPI$EPI)
e <- EPI$EPI[!tf]

tf <- is.na(EPI$DALY)
d <- EPI$DALY[!tf]

# Generate Central Tendency
mean(e, na.rm = TRUE)
median(e, na.rm = TRUE)
Mode(e)

mean(d, na.rm = TRUE)
median(d, na.rm = TRUE)
Mode(d)

# Read in EPI 2010 data
EPI2010 <- read.csv('DataAnalyticsFall2021_Jonathan_Harris/Data/2010EPI_data.csv',skip=1)
attach(EPI2010)

# Remove NA values 
tf <- is.na(EPI2010$EPI)
e2010 <- EPI2010$EPI[!tf]

tf <- is.na(EPI2010$DALY)
d2010 <- EPI2010$DALY[!tf]

# hist(e2010, main=sprintf("Histogram of %s",col), xlab=sprintf("%s",col))
library(ggplot2)
ggplot(EPI2010, aes(x=EPI)) + geom_histogram() + 
  ggtitle("Histogram of EPI (EPI2010)") +
  theme(plot.title = element_text(hjust=0.5))
ggplot(EPI2010, aes(x=DALY)) + geom_histogram() + 
  ggtitle("Histogram of DALY (EPI2010)") +
  theme(plot.title = element_text(hjust=0.5))

# Box plot, quantile-quantile plot
boxplot(ENVHEALTH,ECOSYSTEM)
qqplot(ENVHEALTH,ECOSYSTEM)
