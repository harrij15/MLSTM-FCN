# Read in data
getwd()
p <- read.csv('Labs/Lab 1/Data/2010EPI_data.csv',skip=1)

# Specify column
col = 'EPI'
data <- p[col]
daly <- p['DALY']

# Remove NA values
tf = is.na(data)
t <- data[!tf]

tf = is.na(daly)
daly <- daly[!tf]

# Visualize/analyze data
summary(t)

# Tukey's five number summary
fivenum(t, na.rm = TRUE)

# Stem-and-leaf plot
stem(t)

# Histogram

hist(t, main=sprintf("Histogram of %s",col), xlab=sprintf("%s",col))
hist(t, seq(30., 95. ,1.0), prob=TRUE, main=sprintf("Histogram of %s",col), xlab=sprintf("%s",col))
lines(density(t,na.rm=TRUE,bw='SJ'))
rug(t)

# CDF 
plot(ecdf(t), do.points=FALSE, verticals=TRUE, main=sprintf("Cumulative Density Function of %s", col), xlab=sprintf("%s", col), ylab="Cumulative Density")

# Quantile-Quantile
par(pty='s')
qqnorm(t, main=sprintf("Quantile-Quantile of %s",col), xlab=sprintf("%s",col))
qqline(t)

x <- seq(30,95,1)
qqplot(qt(ppoints(250), df=5), x, main=sprintf("Quantile-Quantile of %s (seq)",col), xlab = "Q-Q plot for t dsn")
qqline(x)

# Box plot comparison
boxplot(t,daly, main=sprintf("Box-plot comparison between %s and DALY",col))
qqplot(t,daly, main=sprintf("Q-Q plot of %s and DALY",col), xlab=sprintf("%s",col), ylab="DALY")

# Inter-comparison
vars <- c('EPI','ENVHEALTH','ECOSYSTEM','DALY','AIR_H','WATER_H','AIR_E','WATER_E','BIODIVERSITY')
subset <- p[vars]

for (i in 1:(ncol(subset)-1)) {
  for (j in (i+1):(ncol(subset)-1)) {
    
    var1 <- vars[i]
    var2 <- vars[j]
    
    if (var1 == var2) {next}
    
    data1 <- subset[var1]
    data2 <- subset[var2]
    
    tf = is.na(data1)
    data1 <- data1[!tf]
    
    tf = is.na(data2)
    data2 <- data2[!tf]
    
    # Box-plot
    boxplot(data1,data2, main=sprintf("Box-plot comparison between %s and %s",var1,var2))
    #readline()
    qqplot(data1,data2, main=sprintf("Q-Q plot of %s and %s",var1,var2), xlab=sprintf("%s",var1), ylab=sprintf("%s",var2))    
    #readline()
    
  }
}

# Conditional filtering
cond_var = "Landlock"
cond <- p[cond_var]
tland <- t[!cond]
tland <- tland[!is.na(tland)]
hist(tland, main=sprintf("Histogram of %s",col), xlab=sprintf("%s",col))
hist(tland, seq(30., 95. ,1.0), prob=TRUE, main=sprintf("Histogram of %s",col), xlab=sprintf("%s",col))

lines(density(tland,na.rm=TRUE,bw='SJ'))
rug(tland)

# CDF 
plot(ecdf(tland), do.points=FALSE, verticals=TRUE, main=sprintf("Cumulative Density Function of %s", col), xlab=sprintf("%s", col), ylab="Cumulative Density")

# Quantile-Quantile
par(pty='s')
qqnorm(tland, main=sprintf("Quantile-Quantile of %s",col), xlab=sprintf("%s",col))
qqline(tland)

# Box plot comparison
boxplot(tland,daly, main=sprintf("Box-plot comparison between %s and DALY",col))
qqplot(tland,daly, main=sprintf("Q-Q plot of %s and DALY",col), xlab=sprintf("%s",col), ylab="DALY")

# Subregions
region = "Europe"
cond <- p[p$EPI_regions == region,]

tregion <- t[cond$EPI]
tregion