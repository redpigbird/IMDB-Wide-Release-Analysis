derp <- read.csv("C:/IMDB_Data.csv")
head(derp)
herp <- derp[2:3]
library(dplyr)
herp <- filter(herp,Year<2017)
names(count_by_year) <- c("Year","Count")
tail(herp,20)
cleaned <- group_by(herp,Year) %>% summarize(average = mean(Rating), sd = sd(Rating))
lm(formula = cleaned$Year ~ cleaned$average)
#Producing very wrong results for some reason, have to regress by hand
R_Score <- cor(cleaned$Year,cleaned$average)
#-.65, fairly strong negative correlation
sd_x <- sd(cleaned$Year)
sd_y <- sd(cleaned$average)
slope <- R_Score*(sd_y/sd_x)
#Slope is -.0068
intercept <- mean(cleaned$average)- slope*mean(cleaned$Year)
plot(cleaned$Year,cleaned$average,xlab="Year",ylab="Average Rating",main="Average Movie Rating by Year",col="Red")
lines(loess.smooth(cleaned$Year,cleaned$average),col="Blue")
abline(intercept,slope,col="Green")
plot(cleaned$Year,cleaned$sd,xlab="Year",ylab="SD",main="Standard Deviation of Movie Ratings by Year", col="Red")
R_Score_SD <- cor(cleaned$Year,cleaned$sd)
#.040 so fairly weak positive correlation

