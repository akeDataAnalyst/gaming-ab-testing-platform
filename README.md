# Executive Summary  
Gaming A/B Test – Streak Multiplier Rewards  

**Project Overview**  
End-to-end analytics project simulating a casual/instant game A/B test  

**Experiment Setup**  
- Variant A: Standard daily login rewards (control)  
- Variant B: New streak multiplier rewards (treatment)  
- Synthetic dataset: 100,000 users (~50k per variant)  
- Install dates: 2023-04-01 to 2025-10-30  
- Key tracked metrics: D1/D7/D30 retention, revenue, sessions D1, levels D7, payer conversion

**Key Results – Overall (full dataset)**

| KPI                  | Variant A | Variant B | Relative Uplift | Statistical Significance |
|----------------------|-----------|-----------|------------------|---------------------------|
| D7 Retention         | 24.49%    | 31.95%    | +30.5%           | p << 0.001                |
| D30 Retention        | 10.29%    | 16.27%    | +58.1%           | p << 0.001                |
| Avg Revenue per User | $0.49     | $0.58     | +18.4%           | p << 0.001                |
| Payer Conversion     | 3.09%     | 5.20%     | +68.3%           | p << 0.001                |
| Sessions D1          | 2.68      | 3.11      | +16.2%           | p << 0.001                |
| Levels D7            | 14.99     | 18.58     | +24.0%           | p << 0.001                |

**Conclusion from significance testing**  
All major KPIs show **extremely strong statistical evidence** of improvement (p-values effectively 0.0 with ~100k users).  
The observed uplifts are **highly unlikely to be due to random chance**.

**Recent Cohorts Insight (Aug–Oct 2025, 91 daily cohorts)**  
- Average D7 retention uplift remains strong (+20–40% on most days)  
- Daily statistical significance varies due to small cohort sizes (50–70 users per variant/day)  
→ Normal and expected behavior — pooled/overall test is the decisive one

**Business Recommendation**  
**Strong recommendation to roll out Variant B (streak multiplier rewards) to 100% of players.**

**Expected impact** (conservative estimates)  
- +25–35% medium-term retention (D7) → higher LTV & engagement  
- +15–20% revenue per user → meaningful monetization lift  
- +50–70% payer conversion → substantial increase in paying users  
