library(kernlab)
data(iris)
irismodel <- ksvm(Species ~ ., data = iris,
                  type = "C-bsvc", kernel = "rbfdot",
                  kpar = list(sigma = 0.1), C = 10,
                  prob.model = TRUE)
irismodel

predict(irismodel, iris[c(3, 10, 56, 68, 107, 120), -5], type = "probabilities")
predict(irismodel, iris[c(3, 10, 56, 68, 107, 120), -5], type = "decision")

k <- function(x, y) {
  (sum(x * y) + 1) * exp(0.001 * sum((x - y)^2))
}

class(k) <- "kernel"
data(promotergene)
gene <- ksvm(Class ~ ., data = promotergene,
             kernel = k, C = 10, cross = 5)
gene

x <- rbind(matrix(rnorm(120), , 2), matrix(rnorm(120, mean = 3), , 2))
y <- matrix(c(rep(1, 60), rep(-1, 60)))
svp <- ksvm(x, y, type = "C-svc", kernel = "rbfdot",kpar = list(sigma = 2))
plot(svp)                           
