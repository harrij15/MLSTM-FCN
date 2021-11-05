aba <- read.csv('~/DataAnalyticsFall2021_Jonathan_Harris/Data/abalone.csv')
attach(aba)
fitK <- rpart(Rings ~ Length + Diameter + Height + Whole.weight + Shucked.weight + Viscera.weight + Shell.weight, method="class", data=aba)

printcp(fitK)
plotcp(fitK) 
summary(fitK) 

plot(fitK, uniform=TRUE, main="Classification Tree for Abalone")
text(fitK, all=TRUE, cex=.8)

post(fitK, file = "abalone.ps", title = "Classification Tree for Abalone") # might need to convert to PDF (distill)

pfitK<- prune(fitK, cp=fitK$cptable[which.min(fitK$cptable[,"xerror"]),"CP"])
plot(pfitK, uniform=TRUE, main="Pruned Classification Tree for Abalone")
text(pfitK, all=TRUE, cex=.8)
post(pfitK, file = "ptree.ps", title = "Pruned Classification Tree for Abalone")
