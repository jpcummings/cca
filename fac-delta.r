library(ggplot2)
library(reshape2)

faculty<-read.csv("fac-delta.csv")
df<-data.frame(faculty)

meltdf<-melt(df,id="size")
g<-ggplot(meltdf,aes(x=size,y=value,xlab="average section size",colour=variable,group=variable)) + geom_line()
gg<-g+xlab("ave. section size")+ylab("number of faculty")
ggg<-gg+coord_cartesian(ylim=c(0,50),xlim=c(20,31))+scale_x_continuous(breaks = round(seq(20,31))) +scale_y_continuous(breaks = round(seq(0,50,2))) + theme(axis.text=element_text(size=12), axis.title=element_text(size=14,face="bold"))+ theme(legend.text=element_text(size=12)) +scale_linetype_discrete(name="Rank")

#ggplot(meltdf,aes(x=size,y=value,colour=variable,group=variable)) + geom_line()
# dev.copy2pdf(file="fac-delta.pdf")
