require(rpart)

fitM <- rpart(Mileage~Price+Country+Reliability+Type, method="anova", data=cu.summary)

printcp(fitM) 
plotcp(fitM)
summary(fitM)
par(mfrow=c(1,2)) 

rsq.rpart(fitM) 

plot(fitM, uniform=TRUE, main="Regression Tree for Mileage")
text(fitM, use.n=TRUE, all=TRUE, cex=.8)

pfitM<- prune(fitM, cp=0.1) # from cptable??? adjust this to see the effect

plot(pfitM, uniform=TRUE, main="Pruned Regression Tree for Mileage")
text(pfitM, use.n=TRUE, all=TRUE, cex=.8)
post(pfitM, file = "ptree2.ps", title = "Pruned Regression Tree for Mileage")
