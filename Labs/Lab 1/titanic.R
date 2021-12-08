# rpart
require(rpart)
data(Titanic)

titanic_rpart <- rpart(Survived ~ .,data=Titanic)
plot(titanic_rpart,margin=0.2) 
text(titanic_rpart)

# ctree
require(party)

treeSwiss<-ctree(Species ~ ., data=iris)
plot(treeSwiss)

# hclust
treeClust <- hclust(dist(Titanic))
plot(treeClust)
