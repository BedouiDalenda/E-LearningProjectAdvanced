import json
import numpy as np
from keyword_search import KeywordSearch
from semantic_search import SemanticSearch

class SearchEvaluator:
    def __init__(self, relevance_file="data/relevance_judgments.json", queries_file="data/queries.json"):
        self.keyword_searcher = KeywordSearch()
        self.semantic_searcher = SemanticSearch()
        
        # Charger les relevance judgments depuis le fichier JSON
        self.relevance = self._load_relevance_judgments(relevance_file)

        # Charger toutes les queries et stocker comme attribut
        try:
            with open(queries_file, 'r', encoding='utf-8') as f:
                self.queries = json.load(f)
            print(f"✅ {len(self.queries)} queries chargées depuis {queries_file}")
        except FileNotFoundError:
            print(f"⚠️ Fichier {queries_file} introuvable. Veuillez créer le fichier queries.json")
            self.queries = []

    def _load_relevance_judgments(self, relevance_file):
        """Load relevance judgments from JSON file"""
        try:
            with open(relevance_file, 'r', encoding='utf-8') as f:
                relevance = json.load(f)
            
            # Convertir les clés string en int pour query_id
            relevance = {int(k): v for k, v in relevance.items()}
            
            print(f"✅ Relevance judgments chargés: {len(relevance)} requêtes")
            return relevance
        except FileNotFoundError:
            print(f"⚠️ Fichier {relevance_file} introuvable. Génération automatique...")
            return self._create_relevance_judgments()
    
    def _create_relevance_judgments(self):
        """Fallback: Create basic relevance judgments if file doesn't exist"""
        print("⚠️ Utilisez 'python generate_relevance_judgments.py' pour créer le fichier")
        return {}

    
    # Metrics
  
    def precision_at_k(self, results, relevant_docs, k):
        if k == 0:
            return 0.0
        top_k = results[:k]
        relevant_retrieved = sum(1 for r in top_k if r['course_id'] in relevant_docs)
        return relevant_retrieved / k
    
    def recall_at_k(self, results, relevant_docs, k):
        if not relevant_docs:
            return 0.0
        top_k = results[:k]
        relevant_retrieved = sum(1 for r in top_k if r['course_id'] in relevant_docs)
        return relevant_retrieved / len(relevant_docs)
    
    def mrr(self, results, relevant_docs):
        for i, result in enumerate(results, 1):
            if result['course_id'] in relevant_docs:
                return 1.0 / i
        return 0.0
    
    def ndcg_at_k(self, results, relevance_scores, k):
        def dcg(scores):
            return sum(score / np.log2(i + 2) for i, score in enumerate(scores))
        
        result_scores = []
        for i, result in enumerate(results[:k]):
            score = relevance_scores.get(result['course_id'], 0)
            result_scores.append(score)
        
        if not result_scores or sum(result_scores) == 0:
            return 0.0
        
        ideal_scores = sorted(relevance_scores.values(), reverse=True)[:k]
        dcg_val = dcg(result_scores)
        idcg_val = dcg(ideal_scores)
        
        return dcg_val / idcg_val if idcg_val > 0 else 0.0

 
    def evaluate_query(self, query_id, query_text, k=10):
        """Evaluate both systems on a single query"""
        relevant_docs = self.relevance.get(query_id, {})
        keyword_results = self.keyword_searcher.search(query_text, top_k=k)
        semantic_results = self.semantic_searcher.search(query_text, top_k=k)
        
        metrics = {
            "keyword": {
                "precision@5": self.precision_at_k(keyword_results, relevant_docs, 5),
                "precision@10": self.precision_at_k(keyword_results, relevant_docs, 10),
                "recall@5": self.recall_at_k(keyword_results, relevant_docs, 5),
                "recall@10": self.recall_at_k(keyword_results, relevant_docs, 10),
                "mrr": self.mrr(keyword_results, relevant_docs),
                "ndcg@10": self.ndcg_at_k(keyword_results, relevant_docs, 10)
            },
            "semantic": {
                "precision@5": self.precision_at_k(semantic_results, relevant_docs, 5),
                "precision@10": self.precision_at_k(semantic_results, relevant_docs, 10),
                "recall@5": self.recall_at_k(semantic_results, relevant_docs, 5),
                "recall@10": self.recall_at_k(semantic_results, relevant_docs, 10),
                "mrr": self.mrr(semantic_results, relevant_docs),
                "ndcg@10": self.ndcg_at_k(semantic_results, relevant_docs, 10)
            }
        }
        
        return metrics, keyword_results, semantic_results

    def evaluate_all_queries(self):
        """Evaluate all queries"""
        all_metrics = {
            "keyword": {"precision@5": [], "precision@10": [], "recall@5": [], 
                       "recall@10": [], "mrr": [], "ndcg@10": []},
            "semantic": {"precision@5": [], "precision@10": [], "recall@5": [], 
                        "recall@10": [], "mrr": [], "ndcg@10": []}
        }
        
        for query in self.queries:
            if query['id'] not in self.relevance:
                continue
            metrics, _, _ = self.evaluate_query(query['id'], query['query'])
            for system in ["keyword", "semantic"]:
                for metric_name, value in metrics[system].items():
                    all_metrics[system][metric_name].append(value)
        
        # Calculate averages
        results = {}
        for system in ["keyword", "semantic"]:
            results[system] = {}
            for metric_name, values in all_metrics[system].items():
                results[system][metric_name] = {
                    "mean": np.mean(values) if values else 0,
                    "std": np.std(values) if values else 0
                }
        return results

    def evaluate_filtered_queries(self, filtered_queries):
        """Evaluate only a subset of queries"""
        all_metrics = {
            "keyword": {"precision@5": [], "precision@10": [], "recall@5": [], 
                       "recall@10": [], "mrr": [], "ndcg@10": []},
            "semantic": {"precision@5": [], "precision@10": [], "recall@5": [], 
                        "recall@10": [], "mrr": [], "ndcg@10": []}
        }

        for query in filtered_queries:
            if query['id'] not in self.relevance:
                continue
            metrics, _, _ = self.evaluate_query(query['id'], query['query'])
            for system in ["keyword", "semantic"]:
                for metric_name, value in metrics[system].items():
                    all_metrics[system][metric_name].append(value)

        # Calculate averages
        results = {}
        for system in ["keyword", "semantic"]:
            results[system] = {}
            for metric_name, values in all_metrics[system].items():
                results[system][metric_name] = {
                    "mean": np.mean(values) if values else 0,
                    "std": np.std(values) if values else 0
                }
        return results


if __name__ == "__main__":
    evaluator = SearchEvaluator()
    
    metrics, kw_results, sem_results = evaluator.evaluate_query(1, "Python programming")
    
    print("\n📊 Métriques pour 'Python programming':")
    print("\nKeyword Search:")
    for metric, value in metrics['keyword'].items():
        print(f"  {metric}: {value:.3f}")
    
    print("\nSemantic Search:")
    for metric, value in metrics['semantic'].items():
        print(f"  {metric}: {value:.3f}")
