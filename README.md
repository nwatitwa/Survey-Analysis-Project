# Remote Work Survey Analysis

## Overview
This project analyzes survey data on remote work experiences collected in 2020 and 2021. Our goal is to understand factors affecting remote work productivity, barriers, and organizational support, and to prepare an interactive story-style dashboard to communicate insights.

---

## Data Restructuring
- **Separate yearly datasets** were combined while maintaining unique respondents (`respondent_id`) and year information.
- **Long-format transformation** was applied for time-related variables and survey responses.
- **Normalized column names** across datasets to allow consistent analysis.
- Created key tables:
  1. **Respondents** – demographic info (age, gender, household, metro/regional)
  2. **Job & Organization** – role, industry, org size, management responsibilities
  3. **Remote Work Patterns** – hours spent remote, preferences
  4. **Outcomes & Barriers** – productivity, top barriers, work-life impacts
  5. **Policy & Support** – organizational encouragement, preparedness, autonomy
  6. **Time Use** – activity breakdown (commuting, working, personal, sleep)

---

## Key Concepts
- **Mismatch**: difference between actual remote work and preferred remote work, calculated as a percentage difference.
- **Productivity**: respondents' perceived change in productivity when working remotely (converted from textual Likert or percentage responses to numeric scores).
- **Policy Support Score**: composite score of 4 Likert-scale questions on organizational support and autonomy.

---

## Hypotheses Studied
1. **H1** – Mismatch and productivity: Does working more/less than preferred affect perceived productivity?
2. **H2** – Barriers and mismatch: Which barriers (connectivity, management, IT, etc.) are associated with mismatch?
3. **H3** – Mismatch vs productivity: Spearman correlation and regression analysis.
4. **H4** – Policy & support vs mismatch and productivity: Composite policy score correlated with mismatch; regression with productivity.

*Note*: Columns with qualitative responses (percentages, "more productive," "less productive") were converted to numeric for analysis.

---

## Analysis Approach
- **Exploratory Data Analysis (EDA)**: summary statistics, distributions, correlations.
- **Hypothesis Testing**:
  - Spearman correlations for ordinal variables.
  - Linear regression for relationships with productivity.
- **Data Cleaning Considerations**:
  - Standardized Likert responses.
  - Converted text-based percentages to numeric.
  - Handled missing and inconsistent entries.

---

## Dashboard
The interactive story in PowerBI includes four main tabs:
1. **Remote Work Patterns** – visualizing mismatch and actual vs preferred remote work.
2. **Productivity Insights** – links between mismatch, barriers, and productivity.
3. **Demograpics overview**
4. **Policy & Support** – showing organizational support, autonomy, and potential improvements.

---

## Future Considerations
- Extend analysis to longitudinal comparisons between 2020 and 2021.
- Incorporate sentiment analysis on open-ended responses.
- Evaluate interventions for reducing mismatch and improving productivity.

---

*All analysis was performed in Python, with data cleaning, transformation, and hypothesis testing handled programmatically before exporting cleaned tables for visualization.*
