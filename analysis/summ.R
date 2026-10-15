suppressPackageStartupMessages({library(brms); library(dplyr); library(tidyr); library(posterior)})
setwd("/home/user/childrvc/analysis")
lev <- function(d){ d$result <- factor(d$result, levels=c("full","zero")); d$age <- factor(d$age, levels=c("4yo","5yo","adult")); d }
q <- function(x) sprintf("%.2f [%.2f, %.2f]", median(x), quantile(x,.025), quantile(x,.975))
pp <- function(x) sprintf("%.3f", mean(x > 0))
diag <- function(m, name){ s <- summary(m); rh <- max(rhat(m), na.rm=TRUE); ne <- min(neff_ratio(m), na.rm=TRUE)
  nd <- sum(nuts_params(m)$Value[nuts_params(m)$Parameter=="divergent__"])
  cat(sprintf("%s: max Rhat = %.3f, min neff ratio = %.2f, divergences = %d\n", name, rh, ne, nd)) }
grid_pred <- function(m, nd){ list(p = posterior_epred(m, newdata=nd, re_formula=NA), l = posterior_linpred(m, newdata=nd, re_formula=NA)) }
sink("out/summary.txt")
## ---------- Model 1 ----------
for (nm in c("m1_8","m1_10")) { m <- readRDS(paste0("out/",nm,".rds")); diag(m, nm)
  nd <- expand.grid(form=c("RVC","V1"), result=c("full","zero"), age=c("4yo","5yo","adult")); g <- grid_pred(m, nd)
  cat("\n==", nm, "fixed effects ==\n"); print(round(fixef(m), 2))
  cat("\nPredicted acceptance:\n"); for (i in 1:nrow(nd)) cat(sprintf("%s %s %s: %s\n", nd$form[i], nd$result[i], nd$age[i], q(g$p[,i])))
  idx <- function(f,r,a) which(nd$form==f & nd$result==r & nd$age==a)
  for (a in c("4yo","5yo","adult")) { for (f in c("RVC","V1")) {
      d <- g$p[,idx(f,"full",a)] - g$p[,idx(f,"zero",a)]; cat(sprintf("full-zero %s %s: prob %s\n", f, a, q(d))) }
    dd <- (g$l[,idx("RVC","full",a)]-g$l[,idx("RVC","zero",a)]) - (g$l[,idx("V1","full",a)]-g$l[,idx("V1","zero",a)])
    ddp <- (g$p[,idx("RVC","full",a)]-g$p[,idx("RVC","zero",a)]) - (g$p[,idx("V1","full",a)]-g$p[,idx("V1","zero",a)])
    cat(sprintf("Form x Result (RVC minus V1 full-zero) %s: logit %s P(>0)=%s; prob %s\n", a, q(dd), pp(dd), q(ddp))) }
  fx <- function(a) (g$l[,idx("RVC","full",a)]-g$l[,idx("RVC","zero",a)]) - (g$l[,idx("V1","full",a)]-g$l[,idx("V1","zero",a)])
  ch <- (fx("4yo")+fx("5yo"))/2; cat(sprintf("Form x Result: children minus adults (logit) %s P(<0)=%.3f\n", q(ch-fx("adult")), mean(ch-fx("adult")<0)))
  cat(sprintf("Form x Result: 5yo minus 4yo (logit) %s P(>0)=%s\n", q(fx("5yo")-fx("4yo")), pp(fx("5yo")-fx("4yo"))))
  v1z <- function(a) g$p[,idx("V1","zero",a)]; cat(sprintf("V1 zero: adults minus children (prob) %s P(>0)=%s\n", q(v1z("adult")-(v1z("4yo")+v1z("5yo"))/2), pp(v1z("adult")-(v1z("4yo")+v1z("5yo"))/2)))
  rz <- function(a) g$p[,idx("RVC","zero",a)]; cat(sprintf("RVC zero: children minus adults (prob) %s P(>0)=%s\n", q((rz("4yo")+rz("5yo"))/2-rz("adult")), pp((rz("4yo")+rz("5yo"))/2-rz("adult"))))
  cat("\n") }
## ---------- Model 2 ----------
m2sum <- function(m, nm, full=TRUE){ diag(m, nm)
  nd <- expand.grid(assoc=c("stronger","weaker"), result=c("full","zero"), age=c("4yo","5yo","adult")); g <- grid_pred(m, nd)
  idx <- function(s,r,a) which(nd$assoc==s & nd$result==r & nd$age==a)
  if (full) { cat("\n==", nm, "fixed effects ==\n"); print(round(fixef(m), 2))
    cat("\nPredicted acceptance:\n"); for (i in 1:nrow(nd)) cat(sprintf("%s %s %s: %s\n", nd$assoc[i], nd$result[i], nd$age[i], q(g$p[,i]))) }
  ae <- function(r,a,s="l") g[[s]][,idx("weaker",r,a)] - g[[s]][,idx("stronger",r,a)]
  for (a in c("4yo","5yo","adult")) { cat(sprintf("Assoc effect zero %s: logit %s P(>0)=%s; prob %s\n", a, q(ae("zero",a)), pp(ae("zero",a)), q(ae("zero",a,"p"))))
    if (full) { cat(sprintf("Assoc effect full %s: prob %s\n", a, q(ae("full",a,"p"))))
    ix <- ae("zero",a)-ae("full",a); cat(sprintf("Assoc x Result %s: logit %s P(>0)=%s\n", a, q(ix), pp(ix))) } }
  allz <- (ae("zero","4yo")+ae("zero","5yo")+ae("zero","adult"))/3; cat(sprintf("Assoc effect zero, averaged: logit %s P(>0)=%s\n", q(allz), pp(allz)))
  chz <- (ae("zero","4yo")+ae("zero","5yo"))/2; d <- chz - ae("zero","adult")
  chzp <- (ae("zero","4yo","p")+ae("zero","5yo","p"))/2; dp <- chzp - ae("zero","adult","p")
  cat(sprintf("Assoc x Age (children minus adults), zero: logit %s P(>0)=%s; prob %s P(>0)=%s\n", q(d), pp(d), q(dp), pp(dp)))
  d54 <- ae("zero","5yo")-ae("zero","4yo"); cat(sprintf("Assoc effect zero, 5yo minus 4yo: logit %s\n", q(d54)))
  if (full) { for (s in c("stronger","weaker")) { ag <- g$p[,idx(s,"zero","adult")] - (g$p[,idx(s,"zero","4yo")]+g$p[,idx(s,"zero","5yo")])/2
      agl <- g$l[,idx(s,"zero","adult")] - (g$l[,idx(s,"zero","4yo")]+g$l[,idx(s,"zero","5yo")])/2
      cat(sprintf("Adults minus children, zero, %s: prob %s P(>0)=%s; logit %s\n", s, q(ag), pp(ag), q(agl))) } }
  invisible(list(allz=allz, d=d)) }
m2 <- readRDS("out/m2_8.rds"); m2sum(m2, "m2_8"); cat("\n"); if (file.exists("out/m2_10.rds")) m2sum(readRDS("out/m2_10.rds"), "m2_10"); cat("\n== Leave-one-pair-out ==\n")
for (f in Sys.glob("out/m2_lopo_*.rds")) { m <- readRDS(f); cat(basename(f), "\n"); m2sum(m, basename(f), full=FALSE) }
## ---------- Production ----------
for (nm in c("p_rvc","p_target","p_rvc_8","p_target_8")) { f <- paste0("out/",nm,".rds"); if (!file.exists(f)) next; m <- readRDS(f); diag(m, nm)
  nd <- expand.grid(result=c("full","zero"), age=c("4yo","5yo","adult")); g <- grid_pred(m, nd)
  if (!grepl("_8", nm)) { cat("\n==", nm, "fixed ==\n"); print(round(fixef(m),2)) }
  for (i in 1:nrow(nd)) cat(sprintf("%s %s %s: %s\n", nm, nd$result[i], nd$age[i], q(g$p[,i])))
  idx <- function(r,a) which(nd$result==r & nd$age==a)
  for (a in c("4yo","5yo","adult")) { d <- g$l[,idx("full",a)]-g$l[,idx("zero",a)]; dp <- g$p[,idx("full",a)]-g$p[,idx("zero",a)]
    cat(sprintf("full-zero %s: logit %s P(>0)=%s; prob %s\n", a, q(d), pp(d), q(dp))) }
  ef <- function(a) g$l[,idx("full",a)]-g$l[,idx("zero",a)]; ch <- (ef("4yo")+ef("5yo"))/2
  cat(sprintf("Result effect children minus adults (logit) %s\n", q(ch-ef("adult"))))
  ma <- function(a) (g$p[,idx("full",a)]+g$p[,idx("zero",a)])/2; cat(sprintf("Overall adults minus children (prob) %s\n", q(ma("adult")-(ma("4yo")+ma("5yo"))/2)))
  cat(sprintf("Overall 5yo minus 4yo (prob) %s\n", q(ma("5yo")-ma("4yo")))); cat("\n") }
sink()
