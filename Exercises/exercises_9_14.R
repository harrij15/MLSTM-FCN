library(tidyverse)
library(dplyr)
View(diamonds)

x_data <- data.frame(diamonds['x'])
y_data <- diamonds['y']
z_data <- diamonds['z']

tf = is.na(x_data)
print(dim(tf))
print(dim(x_data))
x_data <- x_data[!tf]


tf = is.na(y_data)
y_data <- y_data[!tf]

tf = is.na(z_data)
z_data <- z_data[!tf]

fivenum(x_data, na.rm = TRUE)
fivenum(y_data, na.rm = TRUE)
fivenum(z_data, na.rm = TRUE)

ggplot(data = diamonds, mapping = aes(x = price)) + geom_histogram(binwidth = 1)

print(nrow(diamonds %>% filter(carat == 0.99)))
print(nrow(diamonds %>% filter(carat == 1)))

subset <- diamonds %>% filter(carat == 0.99)
subset_ <- diamonds %>% filter(carat == 1)
print(fivenum(subset$price,na.rm=TRUE))
print(fivenum(subset_$price,na.rm=TRUE))

ggplot(data = subset_, mapping = aes(x = price)) + geom_histogram(binwidth=1) 

diamonds2 <- diamonds %>% mutate(y = ifelse(y < 3 | y > 20, NA, y))
ggplot(data = diamonds2, mapping = aes(x = price)) + geom_histogram(binwidth=1) 
ggplot(data = diamonds2, mapping = aes(x = color)) + geom_bar(aes(y = 1),stat="identity") 

mean(diamonds2$price)
mean(diamonds2$price, na.rm = TRUE)
sum(diamonds2$price)
sum(diamonds2$price, na.rm = TRUE)
