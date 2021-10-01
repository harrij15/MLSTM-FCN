library(gdata) 
#faster xls reader but requires perl!
# bronx1<-read.xls(file.choose(),pattern="BOROUGH",stringsAsFactors=FALSE,sheet=1,perl="<SOMEWHERE>/perl/bin/perl.exe") 
# bronx1<-bronx1[which(bronx1$GROSS.SQUARE.FEET!="0" & bronx1$LAND.SQUARE.FEET!="0" & bronx1$SALE.PRICE!="$0"),]

#alternate
# library("xlsx", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library")
library(xlsx)
bronx1<-read.xlsx("~/DataAnalyticsFall2021_Jonathan_Harris/Data/rollingsales_bronx.xls",pattern="BOROUGH",stringsAsFactors=FALSE,sheetIndex=1,startRow=5,header=TRUE)
View(bronx1)
#
attach(bronx1) # If you choose to attach, leave out the "data=." in lm regression
SALE.PRICE<-sub("\\$","",SALE.PRICE) 
SALE.PRICE<-as.numeric(gsub(",","", SALE.PRICE)) 
GROSS.SQUARE.FEET<-as.numeric(gsub(",","", GROSS.SQUARE.FEET)) 
LAND.SQUARE.FEET<-as.numeric(gsub(",","", LAND.SQUARE.FEET)) 
plot(log(GROSS.SQUARE.FEET), log(SALE.PRICE)) 

# Remove rows containing zeros
library(dplyr)
combination <- data.frame(SALE.PRICE,GROSS.SQUARE.FEET)
combination <- filter(combination, SALE.PRICE > 0, GROSS.SQUARE.FEET > 0)
m1<-lm(log(combination$SALE.PRICE)~log(combination$GROSS.SQUARE.FEET))
summary(m1)
abline(m1,col="red",lwd=2)
plot(resid(m1))

# Model 2
combination <- data.frame(bronx1$SALE.PRICE,bronx1$GROSS.SQUARE.FEET,bronx1$LAND.SQUARE.FEET,bronx1$NEIGHBORHOOD)
combination <- filter(combination, bronx1$SALE.PRICE > 0, bronx1$GROSS.SQUARE.FEET > 0, bronx1$LAND.SQUARE.FEET > 0, bronx1$NEIGHBORHOOD > 0)
m2<-lm(log(combination$bronx1.SALE.PRICE)~log(combination$bronx1.GROSS.SQUARE.FEET)+log(combination$bronx1.LAND.SQUARE.FEET)+factor(combination$bronx1.NEIGHBORHOOD))
summary(m2)
plot(resid(m2))
# Suppress intercept - using "0+ ..."
m2a<-lm(log(combination$bronx1.SALE.PRICE)~0+log(combination$bronx1.GROSS.SQUARE.FEET)+log(combination$bronx1.LAND.SQUARE.FEET)+factor(combination$bronx1.NEIGHBORHOOD))
summary(m2a)
plot(resid(m2a))

# Model 3
combination <- data.frame(bronx1$SALE.PRICE,bronx1$GROSS.SQUARE.FEET,bronx1$LAND.SQUARE.FEET,bronx1$NEIGHBORHOOD,bronx1$BUILDING.CLASS.CATEGORY)
combination <- filter(combination, bronx1$SALE.PRICE > 0, bronx1$GROSS.SQUARE.FEET > 0, bronx1$LAND.SQUARE.FEET > 0, bronx1$NEIGHBORHOOD > 0, bronx1$BUILDING.CLASS.CATEGORY > 0)
m3<-lm(log(combination$bronx1.SALE.PRICE)~0+log(combination$bronx1.GROSS.SQUARE.FEET)+log(combination$bronx1.LAND.SQUARE.FEET)+factor(combination$bronx1.NEIGHBORHOOD)+factor(combination$bronx1.BUILDING.CLASS.CATEGORY))
summary(m3)
plot(resid(m3))

# Model 4
m4<-lm(log(combination$bronx1.SALE.PRICE)~0+log(combination$bronx1.GROSS.SQUARE.FEET)+log(combination$bronx1.LAND.SQUARE.FEET)+factor(combination$bronx1.NEIGHBORHOOD)*factor(combination$bronx1.BUILDING.CLASS.CATEGORY))
summary(m4)
plot(resid(m4))
#