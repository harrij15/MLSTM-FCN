data("iris")

library(ggplot2)
library(e1071)

qplot(Petal.Length,Petal.Width,data=iris,color=Species)

svm_model3 <- svm(Species~.,data=iris,kernel="polynomial")
summary(svm_model3)

plot(svm_model3,data=iris,Petal.Width~Petal.Length,slice=list(Sepal.Width=3,Sepal.Length=4))

pred3 <- predict(svm_model3, iris)

table3 <- table(Predicted=pred3,Actual=iris$Species)
table3

Model3_accuracyRate = sum(diag(table3))/sum(table3)
Model3_accuracyRate

Model3_MisclassificationRate = 1 - Model3_accuracyRate
Model3_MisclassificationRate