# Attendance and CGPA Regression

Assessment/gradepred.xlsx, containing six semester records.


## Rebuild the reading edition

```bash
python -m pip install -r requirements-research.txt
python scripts/build_research_site.py
```

This renders saved notebook outputs without rerunning model training or external APIs. To refresh findings, run the analysis commands above first, update `reports/research-findings.md`, and rebuild.

<!-- research-edition:start -->
## Research edition

[Research report and final visual results](research/report.md) · [Browser-ready notebook catalogue](research/notebooks.html)

The supplied workbook contains **six semester observations**. The original least-squares fit reports a slope of **0.03805779 CGPA per attendance percentage point**, an intercept of **5.24699972**, and **training R-squared 0.94951765**. These describe the six-point fit only; no independent test performance or causal attendance effect is established.


The `research/` folder contains a professional static reading edition. The Pages workflow deploys it after GitHub Pages is enabled with **GitHub Actions** as the publishing source. Intended URL: `https://adeen1607.github.io/LINEAR_REGRESSION/`. Deployment status must be checked in Actions before treating that address as live.

<!-- research-edition:end -->
