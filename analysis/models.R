suppressPackageStartupMessages({library(brms); library(dplyr); library(tidyr); library(lme4)})
options(mc.cores = 4, brms.backend = "rstan")
setwd("/home/user/childrvc/analysis")
args <- commandArgs(TRUE); which <- if (length(args)) args[1] else "all"
pri <- c(prior(normal(0, 1.5), class = "Intercept"), prior(normal(0, 1.5), class = "b"),
         prior(exponential(1), class = "sd"), prior(lkj(2), class = "cor"))
ctl <- list(adapt_delta = 0.95)
fitb <- function(f, d, file) brm(f, data = d, family = bernoulli(), prior = pri, chains = 4, iter = 3000, warmup = 1000,
                                 control = ctl, seed = 2026, file = file, refresh = 0)
setc <- function(d) {
  d$form <- factor(d$form, levels = c("RVC", "V1")); d$result <- factor(d$result, levels = c("full", "zero"))
  d$age <- factor(d$age, levels = c("4yo", "5yo", "adult")); if ("assoc" %in% names(d)) d$assoc <- factor(d$assoc, levels = c("stronger", "weaker"))
  for (v in intersect(c("form", "result", "age", "assoc"), names(d))) contrasts(d[[v]]) <- contr.sum(nlevels(d[[v]]))
  d }
comp <- read.csv("comp.csv") %>% setc(); comp$retained <- comp$retained %in% c("True", "TRUE", TRUE)
c8 <- setc(droplevels(subset(comp, retained))); v8 <- setc(droplevels(subset(c8, form == "V1"))); v10 <- setc(droplevels(subset(comp, form == "V1")))
f1 <- accept ~ form * result * age + (1 + result | subj) + (1 + form + result + age | item) + (1 | pair)
f2 <- accept ~ assoc * result * age + (1 + result | subj) + (1 + result + age | item) + (1 + assoc | pair)
if (which %in% c("all", "m1")) { m1 <- fitb(f1, c8, "out/m1_8"); m1_10 <- fitb(f1, comp, "out/m1_10") }
if (which %in% c("all", "m2")) { m2 <- fitb(f2, v8, "out/m2_8"); m2_10 <- fitb(f2, v10, "out/m2_10") }
if (which %in% c("all", "cov")) {
  nv <- read.csv("norming_video.csv")
  addvc <- function(d) { d <- left_join(d, nv[, c("pair", "assoc", "all")], by = c("pair", "assoc")); d$vc <- d$all - mean(nv$all[!nv$pair %in% c(7, 8)]); setc(d) }
  c8v <- addvc(c8); v8v <- addvc(v8)
  m1c <- fitb(update(f1, . ~ . + vc + vc:result), c8v, "out/m1_8_cov")
  m2c <- fitb(update(f2, . ~ . + vc + vc:result), v8v, "out/m2_8_cov") }
if (which %in% c("all", "lopo")) {
  m2 <- fitb(f2, v8, "out/m2_8")
  for (pp in sort(unique(v8$pair))) { d <- droplevels(subset(v8, pair != pp)); d <- setc(d)
    fit <- update(m2, newdata = d, recompile = FALSE, chains = 4, iter = 2000, warmup = 1000, seed = 2026, refresh = 0)
    saveRDS(fit, sprintf("out/m2_lopo_%d.rds", pp)) } }
if (which %in% c("all", "prod")) {
  prod <- read.csv("prod.csv"); prod$result <- factor(prod$result, levels = c("full", "zero")); prod$age <- factor(prod$age, levels = c("4yo", "5yo", "adult"))
  contrasts(prod$result) <- contr.sum(2); contrasts(prod$age) <- contr.sum(3)
  fp <- function(y) as.formula(paste(y, "~ result * age + (1 + result | subj) + (1 + result + age | item) + (1 | pair)"))
  p_rvc <- fitb(fp("rvc"), prod, "out/p_rvc"); p_tgt <- fitb(fp("target"), prod, "out/p_target")
  p8 <- droplevels(subset(prod, !pair %in% c(7, 8))); contrasts(p8$result) <- contr.sum(2); contrasts(p8$age) <- contr.sum(3)
  p_rvc8 <- update(p_rvc, newdata = p8, recompile = FALSE, seed = 2026, refresh = 0); saveRDS(p_rvc8, "out/p_rvc_8.rds")
  p_tgt8 <- update(p_tgt, newdata = p8, recompile = FALSE, seed = 2026, refresh = 0); saveRDS(p_tgt8, "out/p_target_8.rds")
}
if (which %in% c("all", "freq")) {
  sink("out/freq.txt")
  ctrl <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
  try({g1 <- glmer(accept ~ form * result * age + (1 + result | subj) + (1 + form + result | item), data = c8, family = binomial, control = ctrl); print(summary(g1)); print(g1@optinfo$conv$lme4$messages)})
  try({g2 <- glmer(accept ~ assoc * result * age + (1 + result | subj) + (1 | item) + (1 | pair), data = v8, family = binomial, control = ctrl); print(summary(g2)); print(g2@optinfo$conv$lme4$messages)})
  try({g2z <- glmer(accept ~ assoc * age + (1 | subj) + (1 | item), data = subset(v8, result == "zero"), family = binomial, control = ctrl); print(summary(g2z)); print(car::Anova(g2z))})
  sink()
}
