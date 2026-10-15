suppressPackageStartupMessages({library(brms); library(dplyr)})
setwd("/home/user/childrvc/analysis")
q <- function(x) sprintf("%.2f [%.2f, %.2f]", median(x), quantile(x,.025), quantile(x,.975)); pp <- function(x) sprintf("%.3f", mean(x > 0))
diag <- function(m, name){ nd <- sum(nuts_params(m)$Value[nuts_params(m)$Parameter=="divergent__"])
  cat(sprintf("%s: max Rhat = %.3f, divergences = %d\n", name, max(rhat(m), na.rm=TRUE), nd)) }
sink("out/cov_summary.txt")
m <- readRDS("out/m1_8_cov.rds"); diag(m, "m1_8_cov"); print(round(fixef(m)[grep("vc", rownames(fixef(m))), , drop=FALSE], 2))
nd <- expand.grid(form=c("RVC","V1"), result=c("full","zero"), age=c("4yo","5yo","adult")); nd$vc <- 0
l <- posterior_linpred(m, newdata=nd, re_formula=NA); idx <- function(f,r,a) which(nd$form==f & nd$result==r & nd$age==a)
for (a in c("4yo","5yo","adult")) { dd <- (l[,idx("RVC","full",a)]-l[,idx("RVC","zero",a)]) - (l[,idx("V1","full",a)]-l[,idx("V1","zero",a)])
  cat(sprintf("FxR %s: logit %s P(>0)=%s\n", a, q(dd), pp(dd))) }
m <- readRDS("out/m2_8_cov.rds"); diag(m, "m2_8_cov"); print(round(fixef(m)[grep("vc", rownames(fixef(m))), , drop=FALSE], 2))
nd <- expand.grid(assoc=c("stronger","weaker"), result=c("full","zero"), age=c("4yo","5yo","adult")); nd$vc <- 0
l <- posterior_linpred(m, newdata=nd, re_formula=NA); p <- posterior_epred(m, newdata=nd, re_formula=NA)
idx <- function(s,r,a) which(nd$assoc==s & nd$result==r & nd$age==a)
ae <- function(a, x=l) x[,idx("weaker","zero",a)] - x[,idx("stronger","zero",a)]
for (a in c("4yo","5yo","adult")) cat(sprintf("Assoc zero %s: logit %s P(>0)=%s\n", a, q(ae(a)), pp(ae(a))))
av <- (ae("4yo")+ae("5yo")+ae("adult"))/3; cat(sprintf("Assoc zero averaged: logit %s P(>0)=%s\n", q(av), pp(av)))
d <- (ae("4yo")+ae("5yo"))/2 - ae("adult"); dp <- (ae("4yo",p)+ae("5yo",p))/2 - ae("adult",p)
cat(sprintf("Assoc x Age children-adults: logit %s; prob %s\n", q(d), q(dp)))
sink()
