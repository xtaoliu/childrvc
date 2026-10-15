# Figures in the style of the author's OSF scripts (comprehensioncodesosf.R, productioncodesosf.R):
# participant-level proportions as jittered transparent points, condition means as large diamonds
# connected by a path, faceted by age group; theme_classic, Times-style serif font.
suppressPackageStartupMessages({library(dplyr); library(ggplot2); library(tidyr); library(patchwork)})
setwd("/home/user/childrvc/analysis")
fam <- "Liberation Serif"   # metric-compatible with Times New Roman
cols <- c("#5BB5AC", "#DE526C")
agel <- c("4yo" = "4-year-olds", "5yo" = "5-year-olds", "adult" = "Adults")
my_theme <- theme_classic(base_size = 12, base_family = fam) +
  theme(axis.title = element_text(size = 12), axis.text = element_text(size = 11), strip.text = element_text(size = 12),
        plot.title = element_text(size = 12, hjust = 0), strip.background = element_blank(), legend.position = "none")
yscale <- scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, 0.1), labels = scales::percent_format(accuracy = 1))
set.seed(2026)
panel <- function(d, xvar, title, xlab, ylab, lv) {
  d[[xvar]] <- factor(d[[xvar]], levels = lv)
  ggplot(d, aes(.data[[xvar]], p)) + facet_grid(. ~ age) +
    geom_point(aes(color = .data[[xvar]]), position = position_jitter(0.1, 0), size = 1.2, alpha = 0.2) +
    stat_summary(fun = "mean", geom = "path", aes(group = 1)) +
    stat_summary(aes(fill = .data[[xvar]]), fun = "mean", geom = "point", size = 4, shape = 23, color = "#313135", stroke = 0.7) +
    scale_color_manual(values = cols) + scale_fill_manual(values = cols) + yscale +
    labs(title = title, x = xlab, y = ylab) + my_theme
}
c <- read.csv("comp.csv"); c$retained <- c$retained %in% c("True", "TRUE", TRUE); c8 <- subset(c, retained)
c8 <- c8 %>% mutate(age = factor(agel[age], levels = agel), Result = ifelse(result == "full", "Full", "Zero"),
                    Assoc = ifelse(assoc == "stronger", "Stronger", "Weaker"))
# Figure 2: RVC and V1 questions by result realization
pr <- c8 %>% group_by(subj, age, form, Result) %>% summarise(p = mean(accept), .groups = "drop")
a <- panel(filter(pr, form == "RVC"), "Result", "a) RVC questions", "Result Realization", "Proportion of Yes Responses\nto RVC Questions", c("Full", "Zero"))
b <- panel(filter(pr, form == "V1"), "Result", "b) V1 questions", "Result Realization", "Proportion of Yes Responses\nto V1 Questions", c("Full", "Zero"))
ggsave("fig/fig2_comprehension.png", a / b, width = 6.5, height = 8, dpi = 300)
# Figure 3: V1 questions by association, separately for full- and zero-result events
pv <- c8 %>% filter(form == "V1") %>% group_by(subj, age, Assoc, Result) %>% summarise(p = mean(accept), .groups = "drop")
a <- panel(filter(pv, Result == "Full"), "Assoc", "a) Full-result events", "Action\u2013Result Association", "Proportion of Yes Responses\nto V1 Questions", c("Stronger", "Weaker"))
b <- panel(filter(pv, Result == "Zero"), "Assoc", "b) Zero-result events", "Action\u2013Result Association", "Proportion of Yes Responses\nto V1 Questions", c("Stronger", "Weaker"))
ggsave("fig/fig3_association.png", a / b, width = 6.5, height = 8, dpi = 300)
# Figure 4: item level, V1 questions in zero-result events (children pooled)
lab <- c(`1` = "1 lychee", `2` = "2 stool", `3` = "3 finger", `4` = "4 paper", `5` = "5 candle", `6` = "6 bottle", `9` = "9 mirror", `10` = "10 walnut")
it <- c8 %>% filter(form == "V1", Result == "Zero") %>% mutate(grp = factor(ifelse(age == "Adults", "Adults", "Children"), levels = c("Children", "Adults"))) %>%
  group_by(pair, Assoc, grp) %>% summarise(p = mean(accept), .groups = "drop") %>% mutate(pair = factor(lab[as.character(pair)], levels = lab))
g4 <- ggplot(it, aes(Assoc, p)) + facet_grid(grp ~ pair) + geom_path(aes(group = 1)) +
  geom_point(aes(fill = Assoc), size = 3, shape = 23, color = "#313135", stroke = 0.6) +
  scale_fill_manual(values = cols) + scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, 0.25), labels = scales::percent_format(accuracy = 1)) +
  scale_x_discrete(labels = c("S", "W")) + labs(x = "Action\u2013Result Association (S = Stronger, W = Weaker)", y = "Proportion of Yes Responses to V1 Questions") + my_theme +
  theme(strip.text = element_text(size = 10), axis.text = element_text(size = 9))
ggsave("fig/fig4_items.png", g4, width = 6.5, height = 4, dpi = 300)
# Figure 5: production, all 10 pairs
pd <- read.csv("prod.csv") %>% mutate(age = factor(agel[age], levels = agel), Result = ifelse(result == "full", "Full", "Zero"))
pp <- pd %>% group_by(subj, age, Result) %>% summarise(rvc = mean(rvc), target = mean(target), .groups = "drop")
a <- panel(rename(pp, p = rvc), "Result", "a) Responses containing an RVC", "Result Realization", "Proportion of RVCs", c("Full", "Zero"))
b <- panel(rename(pp, p = target), "Result", "b) Responses mentioning the target result", "Result Realization", "Proportion of Responses\nMentioning the Target Result", c("Full", "Zero"))
ggsave("fig/fig5_production.png", a / b, width = 6.5, height = 8, dpi = 300)
cat("figs done\n")
