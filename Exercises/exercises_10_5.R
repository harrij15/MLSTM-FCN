library(ISLR)
library(MASS)
library(boot)

# set.seed(1)
set.seed(2)

# Create training set
train = sample(392,196)

# Fit linear regression to training set only
lmfit <- lm(mpg~horsepower, data = Auto, subset = train)

# Estimate the sample responses
attach(Auto)
mean((mpg-predict(lmfit,Auto))[-train]^2)

# Estimate test error for quadratic and cubic regression
# Quadratic
lmfit2 <- lm(mpg~poly(horsepower,2), data = Auto, subset = train)
mean((mpg-predict(lmfit2,Auto))[-train]^2) 

# Cubic
lmfit3 <- lm(mpg~poly(horsepower,3), data = Auto, subset = train) # Cubic
mean((mpg-predict(lmfit3,Auto))[-train]^2)

