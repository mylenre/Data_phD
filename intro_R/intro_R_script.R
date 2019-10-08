# Numerical Modeling course1 - R Basics
# Learning how to import and explore data, and make graphs about Edinburgh's biodiversity
# Written by Mylene Receveur 07/10/2019 University of Edinburgh

#install.packages("package-name"): need to be installed just one time
#install.packages("dplyr")
#dplyr package to provide extra commands for formatting and manipulating data

#library(package-name)
library(dplyr)
# Note that there are quotation marks when installing a package, but not when loading it
 
#getwd()
setwd("D:/mylen/Documents/phD/Data_phD/intro_R") 
#ls()

#import .csv file 
# If files separated by semicolons, use read.csv2 instead of read.csv ("," as separators)
edidiv <- read.csv("D:/mylen/Documents/phD/Data_phD/intro_R/CC-RBasics-master/edidiv.csv")

# check data structure
head(edidiv)                # Displays the first few rows
tail(edidiv)                # Displays the last rows
str(edidiv)                 # Tells you whether the variables are continuous, integers, categorical or characters

#check and assign specific structure to a variable
head(edidiv$taxonGroup)     # Displays the first few rows of this column only
class(edidiv$taxonGroup)    # Tells you what type of variable we're dealing with: it's character now but we want it to be a factor
edidiv$taxonGroup <- as.factor(edidiv$taxonGroup)     # specify we wanted to transform the character values in the taxonGroup column from the edidiv object)

# More exploration
dim(edidiv)                 # Displays number of rows and columns
summary(edidiv)             # Gives you a summary of the data
summary(edidiv$taxonGroup)  # Gives you a summary of that particular variable (column) in your dataset

# use filter() function from the dplyr package tto split object into multiple ones
# The first argument of the function is the data frame, the second argument is the condition you want to filter on. 
Beetle <- filter(edidiv, taxonGroup == "Beetle")
Bird <- filter(edidiv, taxonGroup == "Bird")  
Butterfly <- filter(edidiv, taxonGroup == "Butterfly") 
Dragonfly <- filter(edidiv, taxonGroup == "Dragonfly") 
Flowering.Plants <- filter(edidiv, taxonGroup == "Flowering.Plants") 
Fungus <- filter(edidiv, taxonGroup == "Fungus") 
Hymenopteran <- filter(edidiv, taxonGroup == "Hymenopteran") 
Lichen <- filter(edidiv, taxonGroup == "Lichen") 
Liverwort <- filter(edidiv, taxonGroup == "Liverwort") 
Mammal <- filter(edidiv, taxonGroup == "Mammal") 
Mollusc <- filter(edidiv, taxonGroup == "Mollusc") 

# identify and count the different species
a <- length(unique(Beetle$taxonName))
b <- length(unique(Bird$taxonName))
c <- length(unique(Butterfly$taxonName))
d <- length(unique(Dragonfly$taxonName))
e <- length(unique(Flowering.Plants$taxonName))
f <- length(unique(Fungus$taxonName))
g <- length(unique(Hymenopteran$taxonName))
h <- length(unique(Lichen$taxonName))
i <- length(unique(Liverwort$taxonName))
j <- length(unique(Mammal$taxonName))
k <- length(unique(Mollusc$taxonName))

# create data vector
biodiv <- c(a,b,c,d,e,f,g,h,i,j,k)
names(biodiv) <- c("Beetle_sp",
                   "Bird_sp",
                   "Butterfly_sp",
                   "Dragonfly_sp",
                   "Flowering.Plants_sp",
                   "Fungus_sp",
                   "Hymenopteran_sp",
                   "Lichen_sp",
                   "Liverwort_sp",
                   "Mammal_sp",
                   "Mollusc_sp")
#plot data (help using help(barplot) or help(par))
barplot(biodiv)
#save file using png() and dev.off()
png("barplot.png", width=1600, height=600)
barplot(biodiv, xlab="Taxa", ylab="Number of species", ylim=c(0,600), cex.names= 1.5, cex.axis=1.5, cex.lab=1.5)
dev.off()

# to create new data frame and save it using write.csv().
# first create an object that contains the names of all the taxa (one column)
taxa <- c("Beetle",
          "Bird",
          "Butterfly",
          "Dragonfly",
          "Flowering.Plants",
          "Fungus",
          "Hymenopteran",
          "Lichen",
          "Liverwort",
          "Mammal",
          "Mollusc")

# Turning this object into a factor, i.e. a categorical variable
taxa_f <- factor(taxa)

# then create another object with all the values for the species richness of each taxon (another column).
# Combining all the values for the number of species in an object called richness
richness <- c(a,b,c,d,e,f,g,h,i,j,k)

# Creating the data frame from the two vectors
biodata <- data.frame(taxa_f, richness) # here display same values as "biodiv" object but in columns format

# Saving the file
write.csv(biodata, file="biodata.csv")  # it will be saved in your working directory

# Plot data specifying which column to plot using $
png("barplot2.png", width=1600, height=600)
barplot(biodata$richness, names.arg=c("Beetle",
                                      "Bird",
                                      "Butterfly",
                                      "Dragonfly",
                                      "Flowering.Plants",
                                      "Fungus",
                                      "Hymenopteran",
                                      "Lichen",
                                      "Liverwort",
                                      "Mammal",
                                      "Mollusc"),
        xlab="Taxa", ylab="Number of species", ylim=c(0,600))
dev.off()

# let's do more
# Calculate the mean wingspan for each bird species. The function to do that is simply: mean()
sparrow <- mean(22, 24, 21)
kingfisher <- mean(26, 23, 25)
eagle <- mean(195, 201, 185)
hummingbird <- mean(8, 9, 9)

# Chain them together in a vector
wingspan <- c(sparrow, kingfisher, eagle, hummingbird)

# Create a bird species vector (careful to match the order of the previous vector!)
bird_sp <- c("sparrow", "kingfisher", "eagle", "hummingbird")

# transform character form to factor:
# (To be honest it does not make any difference to the output here, but it would for some other types of plot. Take good habits early!)
class(bird_sp)                      # currently character
bird_sp <- as.factor(bird_sp)       # transforming into factor
class(bird_sp)                      # now a factor! 

# Then, combine the two vectors in a data frame
wings <- data.frame(bird_sp, wingspan)

# Plot the bar plot & save it to file
png("wingspan_plot.png", width=800, height=600)
barplot(wings$wingspan, names.arg = wings$bird_sp,    # notice how we call the bird_sp column instead of typing all the names
        xlab = "Bird species", 
        ylab = "Average wingspan (cm)",               # adding axis titles
        ylim = c(0, 200),                             # setting the limits of the y axis to fit the eagle
        col = "gold")                                 # changing the colour because why not!
dev.off()
