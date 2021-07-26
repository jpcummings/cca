library(ggplot2)

dat <-read.table("dat/costvRT.dat")
g<-qplot(dat[,1],dat[,2]/1000000,geom="line",main="Instructional salary cost vs. release time",xlab="% 2015 release time",ylab="Instructional Salaries [M$]", ylim=c(0,30)) +
	scale_x_continuous(breaks = round(seq(0,100,10))) 
print(g)
dev.copy2pdf(file="plots/costvRT.pdf")
readline(prompt="Press [enter] to continue")

dat <-read.table("dat/costvsab.dat")
g<-qplot(dat[,1],dat[,2]/1000000,geom="line",main="Instructional salary cost vs. sabbaticals",xlab="% 2015 sabbaticals",ylab="Instructional Salaries [M$]", ylim=c(0,30)) +
	scale_x_continuous(breaks = round(seq(0,100,10))) 
print(g)
dev.copy2pdf(file="plots/costvsab.pdf")
readline(prompt="Press [enter] to continue")

dat <-read.table("dat/costvsize.dat")
g<-qplot(dat[,1],dat[,2]/1000000,geom="line",main="Instructional salary cost vs. class size",xlab="average class size",ylab="Instructional Salaries [M$]", ylim=c(0,30)) +
	scale_x_continuous(breaks = round(seq(0,100,10))) 
print(g)
dev.copy2pdf(file="plots/costvsize.pdf")
readline(prompt="Press [enter] to continue")

dat <-read.table("dat/costvvis.dat")
g<-qplot(dat[,1],dat[,2]/1000000,geom="line",main="Replacing visitors with adjuncts",xlab="% 2015 visitors",ylab="Instructional Salaries [M$]", ylim=c(0,30)) +
	scale_x_continuous(breaks = round(seq(0,100,10))) 
print(g)
dev.copy2pdf(file="plots/costvvis.pdf")
readline(prompt="Press [enter] to continue")

school<-c(rep("AD",6),rep("BD",6),rep("SD",6))
rank<-c(rep(c("Adjunct","Instructor","Visitor","Assistant","Associate","Full"),3))
fraction<-c(0.0976, 0.0000, 0.0457, 0.0831, 0.1039, 0.1246, 0.0507, 0.0166, 0.0083, 0.0499, 0.0831, 0.0499, 0.0332, 0.0291, 0.0374, 0.0499, 0.0706, 0.0665)
frac<-data.frame(school,rank,fraction)
gfrac<-ggplot(frac, aes(fill=rank, y=fraction, x=school)) + 
    geom_bar( stat="identity",position="dodge")
print(gfrac)
dev.copy2pdf(file="plots/fracN.pdf")
readline(prompt="Press [enter] to continue")


salary<-c(20400.00, 0.00, 63100.00, 63100.00, 69917.00, 87796.00, 20400.00, 35057.00, 63100.00, 80590.00, 92339.00, 101158.00, 20400.00, 42741.00, 64566.00, 64566.00, 72012.00, 97446.00)
health<-c(0.00, 0.00, 25240.00, 25240.00, 27966.80, 35118.40, 0.00, 14022.80, 25240.00, 32236.00, 36935.60, 40463.20, 0.00, 17096.40, 25826.40, 25826.40, 28804.80, 38978.40)
comp<-salary+health
costfrac<-comp*fraction*240
cfrac<-data.frame(school,rank,costfrac)
gcfrac<-ggplot(frac, aes(fill=rank, y=costfrac, x=school)) + 
    geom_bar( stat="identity",position="dodge")
print(gcfrac)
dev.copy2pdf(file="plots/fracSal.pdf")
readline(prompt="Press [enter] to continue")
