# Read in EPI data
EPI <- read.csv('DataAnalyticsFall2021_Jonathan_Harris/Data/EPI_data.csv')

# Specify region
library(dplyr)
EPI <- filter(EPI, EPI_regions=='Latin America and Caribbean')
attach(EPI)

# Box plot
boxplot(EPI$ENVHEALTH,EPI$DALY,EPI$AIR_H,EPI$WATER_H,EPI$AIR_E,EPI$CLIMATE)

# Standardization
EPI$ENVHEALTH <- scale(EPI$ENVHEALTH)
EPI$DALY <- scale(EPI$DALY)
EPI$AIR_H <- scale(EPI$AIR_H)
EPI$WATER_H <- scale(EPI$WATER_H)
EPI$AIR_E <- scale(EPI$AIR_E)
EPI$CLIMATE <- scale(EPI$CLIMATE)

# Linear model
lmENVH <- lm(ENVHEALTH~DALY+AIR_H+WATER_H+AIR_E+CLIMATE)
lmENVH
summary(lmENVH)

# Model coefficients
cENVH<-coef(lmENVH)
cENVH

# Predict
DALY_NEW <- c(sample(500,231))
AIR_HNEW <- c(sample(500,231))
WATER_HNEW <- c(sample(500,231))
NEW <- data.frame(DALY_NEW,AIR_HNEW,WATER_HNEW)

pENV <- predict(lmENVH,NEW,interval="prediction")
cENV <- predict(lmENVH,NEW,interval="confidence")
View(pENV)
