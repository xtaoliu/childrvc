suppressPackageStartupMessages({library(dplyr); library(ggplot2); library(tidyr)})
setwd("/home/user/childrvc/analysis")
pal <- c("4-year-olds"="#2a78d6","5-year-olds"="#eb6834","Adults"="#1baf7a"); shp <- c("4-year-olds"=16,"5-year-olds"=17,"Adults"=15)
agel <- c("4yo"="4-year-olds","5yo"="5-year-olds","adult"="Adults")
th <- theme_minimal(base_size = 11, base_family = "serif") + theme(panel.grid.minor = element_blank(), panel.grid.major.x = element_blank(),
  legend.position = "top", legend.title = element_blank(), strip.text = element_text(face = "bold"))
boot <- function(x, B = 2000) { m <- replicate(B, mean(sample(x, replace = TRUE))); c(lo = unname(quantile(m, .025)), hi = unname(quantile(m, .975))) }
set.seed(1)
c <- read.csv("comp.csv"); c$retained <- c$retained %in% c("True","TRUE",TRUE); c8 <- subset(c, retained)
ps <- c8 %>% group_by(subj, age, form, result) %>% summarise(a = mean(accept), .groups = "drop")
s1 <- ps %>% group_by(age, form, result) %>% summarise(m = mean(a), lo = boot(a)[1], hi = boot(a)[2], .groups = "drop") %>%
  mutate(age = agel[age], form = ifelse(form == "RVC", "RVC descriptions", "V1 descriptions"), result = ifelse(result == "full", "Full result", "Zero result"))
g1 <- ggplot(s1, aes(result, m, colour = age, shape = age, group = age)) + geom_line(position = position_dodge(.3), linewidth = .6) +
  geom_errorbar(aes(ymin = lo, ymax = hi), width = 0, position = position_dodge(.3), linewidth = .6) + geom_point(size = 2.6, position = position_dodge(.3)) +
  facet_wrap(~form) + scale_colour_manual(values = pal) + scale_shape_manual(values = shp) + scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  labs(x = NULL, y = "Acceptance") + th
ggsave("fig/fig2_comprehension.png", g1, width = 6.5, height = 3.6, dpi = 300)
v <- subset(c8, form == "V1")
ps2 <- v %>% group_by(subj, age, assoc, result) %>% summarise(a = mean(accept), .groups = "drop")
s2 <- ps2 %>% group_by(age, assoc, result) %>% summarise(m = mean(a), lo = boot(a)[1], hi = boot(a)[2], .groups = "drop") %>%
  mutate(age = agel[age], assoc = ifelse(assoc == "stronger", "Stronger association", "Weaker association"), result = ifelse(result == "full", "Full result", "Zero result"))
g2 <- ggplot(s2, aes(result, m, colour = age, shape = age, group = age)) + geom_line(position = position_dodge(.3), linewidth = .6) +
  geom_errorbar(aes(ymin = lo, ymax = hi), width = 0, position = position_dodge(.3), linewidth = .6) + geom_point(size = 2.6, position = position_dodge(.3)) +
  facet_wrap(~assoc) + scale_colour_manual(values = pal) + scale_shape_manual(values = shp) + scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  labs(x = NULL, y = "Acceptance of V1 descriptions") + th
ggsave("fig/fig3_association.png", g2, width = 6.5, height = 3.6, dpi = 300)
# item level, zero result, V1
lab <- c(`1`="P1 剥/捏",`2`="P2 掀/拍",`3`="P3 掰/按",`4`="P4 撕/扯",`5`="P5 吹/挥",`6`="P6 踢/推",`9`="P9 擦/冲",`10`="P10 夹/锤")
lab <- c(`1`="1 lychee",`2`="2 stool",`3`="3 finger",`4`="4 paper",`5`="5 candle",`6`="6 bottle",`9`="9 mirror",`10`="10 walnut")
it <- v %>% filter(result == "zero") %>% mutate(grp = ifelse(age == "adult", "Adults", "Children")) %>% group_by(pair, assoc, grp) %>%
  summarise(m = mean(accept), n = n(), .groups = "drop") %>% mutate(pair = factor(lab[as.character(pair)], levels = lab), assoc = ifelse(assoc == "stronger", "Stronger", "Weaker"))
pal2 <- c(Children="#2a78d6", Adults="#1baf7a"); shp2 <- c(Children=16, Adults=15)
g3 <- ggplot(it, aes(assoc, m, colour = grp, shape = grp, group = grp)) + geom_line(linewidth = .6) + geom_point(size = 2.4) +
  facet_wrap(~pair, nrow = 2) + scale_colour_manual(values = pal2) + scale_shape_manual(values = shp2) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1), breaks = c(0, .5, 1)) +
  labs(x = "V1 association with the target result", y = "Acceptance in zero-result events") + th
ggsave("fig/fig4_items.png", g3, width = 6.5, height = 4.2, dpi = 300)
pr <- read.csv("prod.csv")
pp <- pr %>% pivot_longer(c(rvc, target), names_to = "measure", values_to = "y") %>% group_by(subj, age, result, measure) %>% summarise(a = mean(y), .groups = "drop")
s3 <- pp %>% group_by(age, result, measure) %>% summarise(m = mean(a), lo = boot(a)[1], hi = boot(a)[2], .groups = "drop") %>%
  mutate(age = agel[age], measure = factor(ifelse(measure == "rvc", "Responses with an RVC", "Responses mentioning the target result"), levels = c("Responses with an RVC", "Responses mentioning the target result")), result = ifelse(result == "full", "Full result", "Zero result"))
g4 <- ggplot(s3, aes(result, m, colour = age, shape = age, group = age)) + geom_line(position = position_dodge(.3), linewidth = .6) +
  geom_errorbar(aes(ymin = lo, ymax = hi), width = 0, position = position_dodge(.3), linewidth = .6) + geom_point(size = 2.6, position = position_dodge(.3)) +
  facet_wrap(~measure) + scale_colour_manual(values = pal) + scale_shape_manual(values = shp) + scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  labs(x = NULL, y = "Proportion of responses") + th
ggsave("fig/fig5_production.png", g4, width = 6.5, height = 3.6, dpi = 300)
cat("figs done\n")
