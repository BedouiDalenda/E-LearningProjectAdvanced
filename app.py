import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from keyword_search import KeywordSearch
from semantic_search import SemanticSearch
from evaluator import SearchEvaluator

# Page config
st.set_page_config(page_title="Search Comparison", layout="wide")

# Initialize searchers (cache)
@st.cache_resource
def load_searchers():
    return KeywordSearch(), SemanticSearch(), SearchEvaluator()

keyword_searcher, semantic_searcher, evaluator = load_searchers()

# Title
st.title("🔍 Semantic Search vs Keyword Search")
st.markdown("Compare two search systems on university courses")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    top_k = st.slider("Number of results", 5, 20, 10)
    
    st.header("📊 Navigation")
    page = st.radio("Select page:", 
                    ["Search Comparison", "Evaluation Report", "A/B Testing"])

# Page 1: Search Comparison
if page == "Search Comparison":
    st.header("Search Comparison")
    
    query = st.text_input("Enter your search query:", "Machine Learning Python")
    
    if st.button("Search", type="primary"):
        col1, col2 = st.columns(2)
        
        # Keyword search
        with col1:
            st.subheader("🔤 Keyword Search (BM25)")
            kw_results = keyword_searcher.search(query, top_k=top_k)
            
            for i, result in enumerate(kw_results, 1):
                with st.expander(f"{i}. {result['title']} (Score: {result['score']:.2f})"):
                    st.write(f"**Level:** {result['level']}")
                    st.write(f"**Rating:** {'⭐' * int(result['rating'])}")
                    st.write(f"**Description:** {result['description'][:150]}...")
        
        # Semantic search
        with col2:
            st.subheader("🧠 Semantic Search (SPARQL)")
            sem_results = semantic_searcher.search(query, top_k=top_k)
            
            for i, result in enumerate(sem_results, 1):
                with st.expander(f"{i}. {result['title']} (Score: {result['score']:.2f})"):
                    st.write(f"**Level:** {result['level']}")
                    st.write(f"**Rating:** {'⭐' * int(result['rating'])}")
                    st.write(f"**Matched terms:** {', '.join(result['matched_terms'])}")
                    st.write(f"**Description:** {result['description'][:150]}...")

# Page 2: Evaluation Report

elif page == "Evaluation Report":
    st.header("📈 Evaluation Report")
    
    # Sidebar filter for query type
    query_types = ["all", "simple", "complex", "ambiguous", "relational"]
    selected_type = st.selectbox("Select query type to display:", query_types, index=0)
    
    # Run evaluation button
    if st.button("Run Evaluation"):
        with st.spinner("Evaluating..."):
            # Evaluate all queries
            results = evaluator.evaluate_all_queries()
        
        # Filter queries by selected type
        if selected_type != "all":
            filtered_queries = [q for q in evaluator.queries if q["type"] == selected_type]
        else:
            filtered_queries = evaluator.queries
            
        results = evaluator.evaluate_filtered_queries(filtered_queries)


        
        # Display metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Keyword Search Metrics")
            kw_metrics = pd.DataFrame([
                {"Metric": k, "Mean": v['mean'], "Std": v['std']}
                for k, v in results['keyword'].items()
            ])
            st.dataframe(kw_metrics, use_container_width=True)
        
        with col2:
            st.subheader("Semantic Search Metrics")
            sem_metrics = pd.DataFrame([
                {"Metric": k, "Mean": v['mean'], "Std": v['std']}
                for k, v in results['semantic'].items()
            ])
            st.dataframe(sem_metrics, use_container_width=True)
        
        # Comparison chart
        st.subheader("Metrics Comparison")
        metrics_names = list(results['keyword'].keys())
        kw_values = [results['keyword'][m]['mean'] for m in metrics_names]
        sem_values = [results['semantic'][m]['mean'] for m in metrics_names]
        
        fig = go.Figure(data=[
            go.Bar(name='Keyword Search', x=metrics_names, y=kw_values),
            go.Bar(name='Semantic Search', x=metrics_names, y=sem_values)
        ])
        fig.update_layout(barmode='group', title=f"Performance Comparison ({selected_type.capitalize()} Queries)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis
        st.subheader("📝 Key Findings")
        better_semantic = sum(1 for i in range(len(kw_values)) if sem_values[i] > kw_values[i])
        st.write(f"Semantic search outperforms on **{better_semantic}/{len(metrics_names)}** metrics")
        
        if better_semantic > len(metrics_names) / 2:
            st.success("✅ Semantic search shows significant advantages for this query type")
        else:
            st.info("ℹ️ Both systems have competitive performance")


# Page 3: A/B Testing
else:
    st.header("🧪 A/B Testing Framework")
    
    st.write("Test both systems side-by-side and provide feedback")
    
    test_query = st.text_input("Test query:", "AI courses for beginners")
    
    if st.button("Run A/B Test"):
        kw_results = keyword_searcher.search(test_query, top_k=5)
        sem_results = semantic_searcher.search(test_query, top_k=5)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("System A")
            for i, r in enumerate(kw_results[:3], 1):
                st.write(f"{i}. {r['title']}")
        
        with col2:
            st.subheader("System B")
            for i, r in enumerate(sem_results[:3], 1):
                st.write(f"{i}. {r['title']}")
        
        # Feedback
        st.subheader("Your Feedback")
        with st.form("feedback_form"):
          preference = st.radio(
          "Which system provided better results?",
             ["System A", "System B", "Equal"]
           )
         
          submit = st.form_submit_button("Submit Feedback")

         
          if submit:
            
            st.success("Thank you for your feedback!")
            
            # Store feedback (in production, save to database)
            st.session_state.setdefault('feedback', []).append({
                'query': test_query,
                'preference': preference
            })

# Footer
st.markdown("---")
st.markdown("**Project:** Semantic Search vs Keyword Search")