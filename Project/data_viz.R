library(ggplot2)

# Alerts, Precipitation and Temperature
data <- read.csv('~/DataAnalyticsFall2021_Jonathan_Harris/Project/data.csv')
attach(data)
Days <- seq(1,length(data$Date))
ggplot(data, aes(x=Days,y=Alert, group=1)) +
  geom_line(color="purple") + 
  ylab("CCHFF Outbreak Alert") 
ggplot(data, aes(x=Days,y=Near.Surface.Air.Temperature, group=1)) +
  geom_line(color="red") + 
  ylab("Average Daily Temperature (in K)") 
ggplot(data, aes(x=Days,y=Precipitation, group=1)) +
  geom_line(color="blue") + 
  ylab("Average Daily Precipitation (in mm/hr)")

# Reports
reports <- read.csv('~/DataAnalyticsFall2021_Jonathan_Harris/Project/Country Reports.csv')
attach(reports)

summary(reports)

ggplot(data=reports, aes(x=reorder(Country, Reports), y=Reports, fill=Reports)) +
  geom_bar(stat="identity") + coord_flip() + xlab("Country") + ylab("# of Reports") 

# Locations
locations <- read.csv('~/DataAnalyticsFall2021_Jonathan_Harris/Project/Country Locations.csv')
attach(locations)

ggplot(data=locations, aes(x=reorder(Country, Locations), y=Locations, fill=Locations)) +
  geom_bar(stat="identity") + coord_flip() + xlab("Country") + ylab("# of Locations")

# Coordinates
coordinates <- read.csv('~/DataAnalyticsFall2021_Jonathan_Harris/Project/Reports per Location.csv')
attach(coordinates)

ggplot(data=coordinates, aes(x=reorder(Location, Count), y=Count, fill=Count)) +
  geom_bar(stat="identity") + coord_flip() + xlab("Location") + ylab("Report Count") +
  scale_fill_gradient(low='slateblue4',high='slateblue')
