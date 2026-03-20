# Literary Psychology — Computational Biographical Analysis

**Karimov, K. Sh. (2026)**

Computational biographical analysis of 567 top-rated literary authors (Goodreads)
spanning three centuries (XIX–XXI), annotated across 38 psychological and
life-circumstance dimensions using a structured LLM prompting schema.
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19140071.svg)](https://doi.org/10.5281/zenodo.19140071)
Paper: [Zenodo](https://doi.org/10.5281/zenodo.19140071)
Dashboard: [[Streamlit](https://literary-writers-abjwqyrtxh8h5v8mc6ku8r.streamlit.app/)]

---

## Key findings

- Median standardness score = 5.0 / 9 — non-standardness is the norm, not the exception
- Childhood trauma present in 63.4% of authors; depression in 34.7%
- XIX/XX authors score significantly higher than XXI (r = 0.38–0.42, p < 0.001), attributed to documentation bias
- Male authors score higher than female (p < 0.001); largest gaps in self-destructive patterns and war experience
- Dominant idiosyncratic pattern: *mortality-driven urgency* (n = 115) — death awareness as creative catalyst
- Tag-based logistic regression: CV ROC-AUC = **0.941 ± 0.015**
- Biography embeddings (nomic-embed-text-v1.5, 8192 tokens): CV AUC = **0.787**
- Mediation: childhood trauma effect mediated through depression (109.8%) and self-destructive patterns (127.2%) — suppression effect

---

## Repository structure

```
.
├── 01_eda_and_stats.ipynb          # EDA, statistics, clustering, hypotheses
├── 02_modelling.ipynb              # Embeddings, model comparison, SHAP, mediation
├── app.py                          # Streamlit interactive dashboard
├── authors_annotated.json          # Dataset: 600 authors, 63 fields
├── annotation_prompt.md            # Full LLM annotation prompt (DeepSeek-V3-0324)
├── requirements.txt
└── figures/                        # All output figures (PNG)
```

---

## Dataset

**File:** `authors_annotated.json` — 600 records, 63 fields

| Field | Description |
|-------|-------------|
| `author_name` | Full name |
| `era` | Publication era: XIX / XX / XXI |
| `standardness_score` | Ordinal 0–9 atypicality score |
| `confidence` | Annotation confidence 0–1 |
| `tag_*` | 38 binary psychological/biographical tags |
| `custom_tags_json` | Free-form idiosyncratic patterns |
| `life_pattern_summary` | Short narrative biography |
| `most_defining_trait` | Single most characteristic trait |
| `avg_rating`, `ratings_count` | Goodreads metrics |

---

## Quickstart

```bash
git clone https://github.com/kalli23/literary-writers
cd literary-writers
pip install -r requirements.txt
streamlit run app.py
```

Run notebooks top to bottom. Figures save to `figures/`.  
`02_modelling.ipynb` requires GPU — recommended: Google Colab with T4.

---

## Methods

| Component | Approach |
|-----------|----------|
| Annotation | DeepSeek-V3-0324, structured prompting (see `annotation_prompt.md`) |
| Group comparisons | Mann-Whitney U + Holm-Bonferroni correction |
| Co-occurrence | Null-masked Jaccard similarity |
| Correlation | Partial Spearman controlling for era |
| Clustering | K-modes with Hamming distance |
| Prediction | Logistic regression, 5-fold stratified CV |
| Embeddings | nomic-embed-text-v1.5 (8192 tokens), chunk-and-mean pooling |
| Interpretability | SHAP LinearExplainer on TF-IDF model |
| Mediation | Baron-Kenny method, 1000 bootstrap iterations |

---

## Results summary

| Metric | Value |
|--------|-------|
| N authors | 567 (with score) |
| Score median | 5.0, IQR [3, 6] |
| Score >= 5 | 50.3% |
| Score >= 7 | 23.5% |
| Top tag | childhood_trauma (63.4%) |
| Tag-based CV AUC | 0.941 ± 0.015 |
| Embedding CV AUC | 0.787 ± 0.030 |
| TF-IDF CV AUC | 0.846 ± 0.038 |

---

## Citation

```bibtex
@misc{karimov2026literary,
  title   = {Psychological Non-Standardness in Top Literary Authors},
  author  = {Karimov, K. Sh.},
  year    = {2026},
  doi     = {10.5281/zenodo.19140071},
  url     = {https://zenodo.org/records/19140071}
}
```

---

## Limitations

- Survivorship bias: only Goodreads-ranked authors included
- Single LLM annotator: no human inter-rater reliability check
- XXI era documentation gap: living authors have shorter Wikipedia articles
- Wikipedia coverage bias: non-Western authors have shorter biographical texts

---

## License

MIT
