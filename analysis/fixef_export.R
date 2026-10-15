suppressPackageStartupMessages({library(brms); library(posterior)})
setwd("/home/user/childrvc/analysis")
out <- list()
for (nm in c("m1_8","m2_8","p_rvc","p_target")) {
  m <- readRDS(paste0("out/", nm, ".rds")); s <- summary(m)$fixed
  nd <- sum(nuts_params(m)$Value[nuts_params(m)$Parameter=="divergent__"])
  out[[nm]] <- data.frame(model=nm, term=rownames(s), est=s$Estimate, se=s$Est.Error, lo=s$`l-95% CI`, hi=s$`u-95% CI`, rhat=s$Rhat, ess=s$Bulk_ESS, div=nd)
}
write.csv(do.call(rbind, out), "out/fixef_all.csv", row.names=FALSE)
