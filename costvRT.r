dat <-read.table("costvRT.dat")
options(scipen=5)
par(cex=1)
plot(dat[,1],dat[,2]/1000000,main="Research release time",xlab="% 2015 research release time",ylab="cost [M$]",type="l")
dev.copy2pdf(file="costvRT.pdf")
dev.copy(jpeg,'costvRT.jpg')
dev.off()