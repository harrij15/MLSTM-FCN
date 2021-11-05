require(rpart)
swiss_rpart <- rpart(Fertility ~ Agriculture + Education + Catholic, data = swiss)
plot(swiss_rpart, uniform = TRUE, branch = 0.4, compress=TRUE, margin=0.109) # try some different plot options
text(swiss_rpart,splits=FALSE) # try some different text options
