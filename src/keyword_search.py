import json
from rank_bm25 import BM25Okapi
import re

class KeywordSearch:
    def __init__(self, courses_file="data/courses_data.json"):
        """Initialize BM25 with courses"""
        with open(courses_file, 'r', encoding='utf-8') as f:
            self.courses = json.load(f)
        
        # Prepare corpus
        self.corpus = []
        for course in self.courses:
            text = f"{course['title']} {course['description']} {course['category']}"
            self.corpus.append(text)
        
        # Tokenize
        tokenized_corpus = [self._tokenize(doc) for doc in self.corpus]
        
        # Build BM25 index
        self.bm25 = BM25Okapi(tokenized_corpus)
        print(f"✅ BM25 index créé avec {len(self.courses)} cours")
    
    def _tokenize(self, text):
        """Simple tokenization"""
        text = text.lower()
        tokens = re.findall(r'\w+', text)
        return tokens
    
    def search(self, query, top_k=10):
        """Search courses using BM25"""
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top-k results
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "course_id": self.courses[idx]["id"],
                "title": self.courses[idx]["title"],
                "description": self.courses[idx]["description"],
                "score": float(scores[idx]),
                "level": self.courses[idx]["level"],
                "rating": self.courses[idx]["rating"]
            })
        
        return results

# Test
if __name__ == "__main__":
    searcher = KeywordSearch()
    
    # Test query
    results = searcher.search("Machine Learning Python", top_k=5)
    
    print("\n🔍 Résultats pour 'Machine Learning Python':")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Score: {result['score']:.2f}")
        print(f"   Level: {result['level']}")