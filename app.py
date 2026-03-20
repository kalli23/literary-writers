"""
Psychological Non-Standardness in Top Literary Authors
Interactive dashboard — K. Sh. Karimov, 2026

Run with:
    pip install streamlit plotly pandas numpy scikit-learn kmodes
    streamlit run app.py
"""

import json
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from itertools import combinations

warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Literary Psychology",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Minimal CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #fafaf8; }
    .stSelectbox label, .stMultiSelect label { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
TAGS = [
    'tag_depression','tag_bipolar','tag_schizophrenia','tag_anxiety',
    'tag_ptsd','tag_substance_abuse','tag_suicide','tag_suicide_attempt',
    'tag_institutionalized','tag_childhood_trauma','tag_war_experience',
    'tag_poverty_extreme','tag_chronic_illness','tag_disability',
    'tag_occultism','tag_spiritualism','tag_religious_mania',
    'tag_cult_involvement','tag_theosophy_mysticism',
    'tag_non_traditional_relationship','tag_homosexuality_taboo_era',
    'tag_obsessive_attachment','tag_celibacy_pathological',
    'tag_incest_adjacent','tag_alter_ego_documented',
    'tag_depersonalization','tag_voluntary_isolation',
    'tag_pathological_gambling','tag_legal_troubles',
    'tag_imprisonment','tag_exile','tag_extremist_views',
    'tag_violence_documented','tag_self_destructive_pattern',
    'tag_eating_disorder','tag_paranoia','tag_messiah_complex',
    'tag_nihilism_explicit',
]
TAG_SHORT    = {t: t.replace('tag_', '') for t in TAGS}
ERA_COLORS   = {'XIX': '#3B6D11', 'XX': '#185FA5', 'XXI': '#993C1D'}
GENDER_COLORS = {'M': '#185FA5', 'F': '#993556', 'Unknown': '#888780'}

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import re
    with open('authors_annotated.json', encoding='utf-8') as f:
        df = pd.DataFrame(json.load(f))

    ERA_MAP = {'19': 'XIX', '20': 'XX', '21': 'XXI'}
    df['era'] = df['era'].astype(str).map(ERA_MAP).fillna('Unknown')
    df['score'] = pd.to_numeric(df['standardness_score'], errors='coerce')
    df['conf']  = pd.to_numeric(df['confidence'], errors='coerce')

    def parse_born(val):
        if pd.isna(val) or str(val).strip() == '': return np.nan
        m = re.search(r'\b(1[678]\d{2}|19[0-9]\d|200\d)\b', str(val))
        return int(m.group()) if m else np.nan

    df['birth_year'] = df['born'].apply(parse_born) if 'born' in df.columns else np.nan
    df['decade'] = (df['birth_year'] // 10 * 10).astype('Int64')

    gender_map = {'male': 'M', 'female': 'F', 'unknown': 'Unknown',
                  'M': 'M', 'F': 'F', 'Unknown': 'Unknown'}
    df['gender'] = df['gender'].map(gender_map).fillna('Unknown')

    bool_map = {True: True, False: False, 'true': True, 'false': False,
                1: True, 0: False, 'True': True, 'False': False,
                'null': False, 'None': False, None: False}
    for t in TAGS:
        if t in df.columns:
            df[t] = df[t].map(bool_map).fillna(False).astype(bool)

    for col in ['avg_rating', 'ratings_count', 'rank']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    cluster_tags = [t for t in TAGS if t in df.columns and df[t].sum() >= 10]
    X_bin = df[cluster_tags].astype(int)
    try:
        from kmodes.kmodes import KModes
        km = KModes(n_clusters=2, init='Huang', n_init=10, random_state=42)
        df['cluster'] = km.fit_predict(X_bin)
        df['cluster_name'] = df['cluster'].map({
            0: 'Cluster 0 — High adversity',
            1: 'Cluster 1 — Lower burden'
        })
    except ImportError:
        df['cluster'] = 0
        df['cluster_name'] = 'N/A (install kmodes)'

    return df[df['score'].notna()].copy(), cluster_tags

df, cluster_tags = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Filters")
st.sidebar.markdown("---")

sel_era    = st.sidebar.multiselect("Era",    options=sorted(df['era'].unique()), default=sorted(df['era'].unique()))
sel_gender = st.sidebar.multiselect("Gender", options=sorted(df['gender'].unique()), default=sorted(df['gender'].unique()))
score_range = st.sidebar.slider("Score range", int(df['score'].min()), int(df['score'].max()),
                                 (int(df['score'].min()), int(df['score'].max())))
conf_min = st.sidebar.slider("Min confidence", 0.0, 1.0, 0.0, 0.05)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** 567 authors · 38 tags · 3 eras")
st.sidebar.markdown("**Paper:** Karimov, K. Sh. (2026)")

mask = (
    df['era'].isin(sel_era if sel_era else df['era'].unique()) &
    df['gender'].isin(sel_gender if sel_gender else df['gender'].unique()) &
    df['score'].between(*score_range) &
    df['conf'].ge(conf_min)
)
dff = df[mask].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Psychological Non-Standardness in Top Literary Authors")
st.markdown(
    "**K. Sh. Karimov, 2026** — "
    "Computational biographical analysis of 567 top-rated authors (Goodreads) "
    "across three centuries, annotated across 38 psychological and life-circumstance tags."
)
st.markdown("---")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Authors shown", len(dff))
c2.metric("Median score", f"{dff['score'].median():.1f} / 9")
c3.metric("Score >= 5", f"{(dff['score']>=5).mean()*100:.1f}%")
c4.metric("Childhood trauma", f"{dff['tag_childhood_trauma'].mean()*100:.1f}%")
c5.metric("Avg confidence", f"{dff['conf'].mean():.2f}")
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Score Overview",
    "Era & Gender",
    "Tag Co-occurrence",
    "Author Explorer",
    "Clustering",
    "Predictive Model",
])

# ── Tab 1: Score Overview ─────────────────────────────────────────────────────
with tab1:
    st.header("Score Distribution & Tag Prevalence")
    col_a, col_b = st.columns(2)

    with col_a:
        fig_hist = px.histogram(
            dff, x='score', nbins=10,
            title=f"Score distribution  (N={len(dff)}, median={dff['score'].median():.0f})",
            labels={'score': 'Standardness score'},
            color_discrete_sequence=['#378ADD'],
        )
        fig_hist.add_vline(x=dff['score'].median(), line_dash='dash',
                           line_color='#E24B4A', annotation_text='Median')
        fig_hist.update_layout(bargap=0.08, plot_bgcolor='white',
                               paper_bgcolor='white', height=380)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        xs = np.sort(dff['score'].dropna())
        fig_cdf = go.Figure()
        fig_cdf.add_trace(go.Scatter(
            x=xs, y=np.arange(1, len(xs)+1)/len(xs),
            mode='lines', line=dict(color='#378ADD', width=2.5),
            fill='tozeroy', fillcolor='rgba(55,138,221,0.08)', name='CDF'
        ))
        fig_cdf.add_vline(x=dff['score'].median(), line_dash='dash',
                          line_color='#E24B4A', annotation_text='p50')
        fig_cdf.update_layout(
            title="Cumulative distribution",
            xaxis_title="Score", yaxis_title="Cumulative fraction",
            yaxis_tickformat='.0%', plot_bgcolor='white',
            paper_bgcolor='white', height=380
        )
        st.plotly_chart(fig_cdf, use_container_width=True)

    st.subheader("Tag prevalence (% of authors)")
    tag_prev = pd.DataFrame({
        'tag': [TAG_SHORT[t] for t in TAGS if t in dff.columns],
        'pct': [dff[t].mean() * 100 for t in TAGS if t in dff.columns]
    }).sort_values('pct', ascending=True)
    fig_tags = px.bar(
        tag_prev, x='pct', y='tag', orientation='h',
        labels={'pct': '% True', 'tag': ''},
        color='pct', color_continuous_scale='Teal', height=700,
    )
    fig_tags.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                           coloraxis_showscale=False)
    st.plotly_chart(fig_tags, use_container_width=True)

# ── Tab 2: Era & Gender ───────────────────────────────────────────────────────
with tab2:
    st.header("Score by Era and Gender")
    col_a, col_b = st.columns(2)

    with col_a:
        fig_era = px.box(
            dff[dff['era'].isin(['XIX','XX','XXI'])],
            x='era', y='score', color='era',
            color_discrete_map=ERA_COLORS, points='all',
            title="Score by era (median + IQR)",
            labels={'score': 'Standardness score', 'era': 'Era'},
            category_orders={'era': ['XIX','XX','XXI']},
        )
        fig_era.update_traces(marker_size=3, marker_opacity=0.25)
        fig_era.update_layout(showlegend=False, plot_bgcolor='white',
                              paper_bgcolor='white', height=420)
        st.plotly_chart(fig_era, use_container_width=True)
        st.caption("XIX vs XXI: r=0.38, p<0.001 · XX vs XXI: r=0.42, p<0.001 (Holm-corrected)")

    with col_b:
        fig_gen = px.box(
            dff[dff['gender'].isin(['M','F'])],
            x='gender', y='score', color='gender',
            color_discrete_map=GENDER_COLORS, points='all',
            title="Score by gender",
            labels={'score': 'Standardness score', 'gender': 'Gender'},
        )
        fig_gen.update_traces(marker_size=3, marker_opacity=0.25)
        fig_gen.update_layout(showlegend=False, plot_bgcolor='white',
                              paper_bgcolor='white', height=420)
        st.plotly_chart(fig_gen, use_container_width=True)
        st.caption("M median=5.0 vs F median=4.0, U=39499, p<0.001")

    st.subheader("Temporal trend: median score by birth decade")
    decade_df = dff[dff['decade'].notna()].copy()
    dec_stats = decade_df.groupby('decade')['score'].agg(
        median='median',
        q25=lambda x: x.quantile(0.25),
        q75=lambda x: x.quantile(0.75),
        count='count'
    ).reset_index()
    dec_stats = dec_stats[dec_stats['count'] >= 5]

    fig_dec = go.Figure()
    fig_dec.add_trace(go.Scatter(
        x=list(dec_stats['decade']) + list(dec_stats['decade'])[::-1],
        y=list(dec_stats['q75']) + list(dec_stats['q25'])[::-1],
        fill='toself', fillcolor='rgba(55,138,221,0.15)',
        line=dict(color='rgba(0,0,0,0)'), name='IQR', showlegend=True
    ))
    fig_dec.add_trace(go.Scatter(
        x=dec_stats['decade'], y=dec_stats['median'],
        mode='lines+markers', line=dict(color='#378ADD', width=2.5),
        marker=dict(size=6), name='Median'
    ))
    fig_dec.update_layout(xaxis_title='Birth decade', yaxis_title='Score (median)',
                          plot_bgcolor='white', paper_bgcolor='white', height=350)
    st.plotly_chart(fig_dec, use_container_width=True)

# ── Tab 3: Tag Co-occurrence ──────────────────────────────────────────────────
with tab3:
    st.header("Tag Co-occurrence — Null-masked Jaccard")

    valid_tags  = [t for t in TAGS if t in dff.columns]
    short_names = [TAG_SHORT[t] for t in valid_tags]
    n_tags      = len(valid_tags)

    @st.cache_data
    def compute_jaccard(data_hash):
        jac = np.zeros((n_tags, n_tags))
        for i, t1 in enumerate(valid_tags):
            for j, t2 in enumerate(valid_tags):
                if i >= j: continue
                m = dff[t1].notna() & dff[t2].notna()
                s1 = dff.loc[m, t1].eq(True)
                s2 = dff.loc[m, t2].eq(True)
                both   = (s1 & s2).sum()
                either = (s1 | s2).sum()
                v = both / either if either > 0 else 0.0
                jac[i, j] = v; jac[j, i] = v
        np.fill_diagonal(jac, 1.0)
        return jac

    jac        = compute_jaccard(len(dff))
    jac_masked = np.where(np.triu(np.ones_like(jac, dtype=bool)), np.nan, jac)

    fig_heat = go.Figure(go.Heatmap(
        z=jac_masked, x=short_names, y=short_names,
        colorscale='YlOrRd', zmin=0, zmax=0.5,
        colorbar=dict(title='Jaccard'),
    ))
    fig_heat.update_layout(
        title="Tag co-occurrence (lower triangle)", height=700,
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(tickfont=dict(size=9), tickangle=90),
        yaxis=dict(tickfont=dict(size=9)),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("Top co-occurring pairs")
    pairs = [{'Tag A': s1, 'Tag B': s2, 'Jaccard': round(jac[i,j], 3)}
             for i, s1 in enumerate(short_names)
             for j, s2 in enumerate(short_names) if i < j]
    st.dataframe(pd.DataFrame(pairs).sort_values('Jaccard', ascending=False).head(15),
                 use_container_width=True, hide_index=True)

# ── Tab 4: Author Explorer ────────────────────────────────────────────────────
with tab4:
    st.header("Author Explorer")

    col_s, col_c = st.columns([2, 1])
    with col_s:
        search = st.text_input("Search author name", "")
    with col_c:
        color_by = st.selectbox("Color by", ['era', 'gender', 'cluster_name', 'score'])

    from sklearn.decomposition import PCA
    X_pca  = dff[[t for t in cluster_tags if t in dff.columns]].astype(int)
    coords = PCA(n_components=2, random_state=42).fit_transform(X_pca - X_pca.mean())
    dff['pca1'] = coords[:, 0]
    dff['pca2'] = coords[:, 1]

    plot_df = dff[mask].copy()
    if search:
        plot_df = plot_df[plot_df['author_name'].str.contains(search, case=False, na=False)]

    color_map = ERA_COLORS if color_by == 'era' else (GENDER_COLORS if color_by == 'gender' else None)

    fig_scatter = px.scatter(
        plot_df, x='pca1', y='pca2', color=color_by,
        hover_name='author_name',
        hover_data={'score': True, 'era': True, 'gender': True,
                    'conf': ':.2f', 'pca1': False, 'pca2': False},
        color_discrete_map=color_map,
        color_continuous_scale='RdYlGn' if color_by == 'score' else None,
        title=f"Authors in PCA space (colored by {color_by})",
        labels={'pca1': 'PC1 (21.4%)', 'pca2': 'PC2 (8.2%)'},
        height=550,
    )
    fig_scatter.update_traces(marker=dict(size=6, opacity=0.7))
    fig_scatter.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Author details")
    top_n     = st.slider("Show top N authors by score", 5, 50, 20)
    show_cols = [c for c in ['author_name','era','gender','score','conf',
                              'evidence_quality','cluster_name','most_defining_trait']
                 if c in plot_df.columns]
    st.dataframe(plot_df.nlargest(top_n, 'score')[show_cols].reset_index(drop=True),
                 use_container_width=True)

# ── Tab 5: Clustering ─────────────────────────────────────────────────────────
with tab5:
    st.header("K-modes Clustering (K=2, Hamming distance)")
    col_a, col_b = st.columns(2)

    with col_a:
        cc = dff['cluster_name'].value_counts().reset_index()
        cc.columns = ['Cluster', 'Count']
        fig_pie = px.pie(
            cc, names='Cluster', values='Count', color='Cluster',
            color_discrete_map={
                'Cluster 0 — High adversity': '#7F77DD',
                'Cluster 1 — Lower burden':   '#1D9E75',
            },
            title="Cluster sizes",
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        cs = dff.groupby('cluster_name')['score'].describe()[['50%','25%','75%','count']].round(2)
        cs.columns = ['Median', 'Q25', 'Q75', 'N']
        st.subheader("Score statistics per cluster")
        st.dataframe(cs, use_container_width=True)
        st.markdown("""
**Cluster 0** (n≈257, median=6.0): enriched for non_traditional_relationship,
self_destructive_pattern, depression, chronic_illness, childhood_trauma.

**Cluster 1** (n≈310, median=3.0): depleted across most clinical tags;
dominated by XXI-century authors with thinner biographical coverage.
        """)

    st.subheader("Cluster profiles — top discriminating tags")
    overall_mean = dff[[t for t in cluster_tags if t in dff.columns]].astype(int).mean()
    for c in sorted(dff['cluster'].unique()):
        mask_c = dff['cluster'] == c
        sub    = dff.loc[mask_c, [t for t in cluster_tags if t in dff.columns]].astype(int)
        lift   = (sub.mean() - overall_mean).sort_values(ascending=False)
        lift.index = [t.replace('tag_', '') for t in lift.index]
        top8   = lift.head(8).reset_index()
        top8.columns = ['tag', 'delta']
        cname  = dff.loc[mask_c, 'cluster_name'].iloc[0] if mask_c.any() else f'Cluster {c}'
        fig_c  = px.bar(top8, x='delta', y='tag', orientation='h',
                        title=f"{cname}  (delta from overall mean)",
                        color='delta', color_continuous_scale='RdYlGn',
                        labels={'delta': 'Delta from mean', 'tag': ''})
        fig_c.update_layout(coloraxis_showscale=False, plot_bgcolor='white',
                            paper_bgcolor='white', height=320)
        st.plotly_chart(fig_c, use_container_width=True)

# ── Tab 6: Predictive Model ───────────────────────────────────────────────────
with tab6:
    st.header("Predictive Model — Logistic Regression")
    st.markdown(
        "**Task:** predict high standardness score (>= 5) from 32 binary tags.  \n"
        "**5-fold CV ROC-AUC = 0.941 +/- 0.015** · Accuracy = 0.866 +/- 0.022"
    )

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_curve, roc_auc_score

    y    = (dff['score'] >= 5).astype(int)
    X_lr = dff[[t for t in cluster_tags if t in dff.columns]].astype(int)

    if len(X_lr) > 20:
        lr = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
        lr.fit(X_lr, y)

        coef_df = pd.DataFrame({
            'tag':  [t.replace('tag_', '') for t in X_lr.columns],
            'coef': lr.coef_[0],
            'OR':   np.exp(lr.coef_[0])
        }).sort_values('coef', ascending=True)

        col_a, col_b = st.columns(2)

        with col_a:
            fig_coef = px.bar(
                coef_df, x='coef', y='tag', orientation='h',
                color='coef', color_continuous_scale='RdYlGn',
                title="Feature importance (logistic regression coefficients)",
                labels={'coef': 'Coefficient', 'tag': ''}, height=650,
            )
            fig_coef.add_vline(x=0, line_color='black', line_width=0.8)
            fig_coef.update_layout(coloraxis_showscale=False,
                                   plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig_coef, use_container_width=True)

        with col_b:
            y_prob         = lr.predict_proba(X_lr)[:, 1]
            fpr, tpr, _    = roc_curve(y, y_prob)
            auc_val        = roc_auc_score(y, y_prob)
            fig_roc        = go.Figure()
            fig_roc.add_trace(go.Scatter(
                x=fpr, y=tpr, mode='lines',
                line=dict(color='#378ADD', width=2.5),
                fill='tozeroy', fillcolor='rgba(55,138,221,0.1)',
                name=f'Full-data AUC = {auc_val:.3f}'
            ))
            fig_roc.add_trace(go.Scatter(
                x=[0,1], y=[0,1], mode='lines',
                line=dict(color='gray', dash='dash'), name='Random'
            ))
            fig_roc.update_layout(
                title="ROC curve  (CV AUC = 0.941 +/- 0.015)",
                xaxis_title='False positive rate',
                yaxis_title='True positive rate',
                plot_bgcolor='white', paper_bgcolor='white',
                height=420, legend=dict(x=0.55, y=0.1)
            )
            st.plotly_chart(fig_roc, use_container_width=True)

            st.subheader("Top-5 predictors")
            top5 = coef_df.sort_values('coef', ascending=False).head(5)[['tag','coef','OR']].round(3)
            top5.columns = ['Tag', 'Coefficient', 'Odds Ratio']
            st.dataframe(top5, use_container_width=True, hide_index=True)
    else:
        st.warning("Not enough data with current filters to fit model. Adjust the sidebar filters.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Karimov, K. Sh. (2026). *Psychological Non-Standardness in Top Literary Authors.* "
    "arXiv preprint. "
    "Data: Goodreads top authors + Wikipedia. "
    "Code: [GitHub](https://github.com/kalli23/literary-psychology). "
    "Built with Streamlit + Plotly."
)