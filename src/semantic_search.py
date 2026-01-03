import json
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

ONT = Namespace("http://www.elearning-platform.org/ontology#")

class SemanticSearch:
    def __init__(self, ontology_file="data/ontology_with_courses.owl", 
                 courses_file="data/courses_data.json"):
        """Initialize SPARQL with ontology"""
        self.g = Graph()
        self.g.parse(ontology_file, format="xml")
        self.g.bind("ontology", ONT)
        
        with open(courses_file, 'r', encoding='utf-8') as f:
            self.courses = json.load(f)
        
        print(f"✅ Ontologie chargée: {len(self.g)} triples")
    
    def _expand_query(self, query):
        """Expand query using ontology relationships"""
        query_lower = query.lower()
        expansions = []
        
        # AI expansion
        if "ai" in query_lower or "artificial intelligence" in query_lower:
            expansions.extend(["Machine Learning", "Deep Learning", "Neural Networks", 
                             "Computer Vision", "NLP", "AI"])
        
        # ML expansion
        if "machine learning" in query_lower or "ml" in query_lower:
            expansions.extend(["Machine Learning", "Deep Learning", "AI", 
                             "Data Science", "Algorithms"])
        
        # Web dev expansion
        if "web" in query_lower:
            expansions.extend(["HTML", "CSS", "JavaScript", "React", "Frontend", 
                             "Backend", "Full Stack"])
        
        # Data expansion
        if "data" in query_lower:
            expansions.extend(["Data Science", "Data Analysis", "Big Data", 
                             "Analytics", "Statistics"])
        
        # Programming expansion
        if "programming" in query_lower or "coding" in query_lower:
            expansions.extend(["Python", "Java", "C++", "JavaScript", 
                             "Programming", "OOP"])
        
        return list(set(expansions)) if expansions else [query]
    
    def _extract_level(self, query):
        """Extract level from query"""
        query_lower = query.lower()
        if "beginner" in query_lower or "introduction" in query_lower:
            return "Beginner"
        elif "advanced" in query_lower:
            return "Advanced"
        elif "intermediate" in query_lower:
            return "Intermediate"
        return None
    
    def search(self, query, top_k=10):
        """Semantic search with SPARQL and query expansion"""
        
        # Expand query
        expanded_terms = self._expand_query(query)
        level_filter = self._extract_level(query)
        
        results = []
        seen_ids = set()
        
        for course in self.courses:
            score = 0
            
            # Match expanded terms
            course_text = f"{course['title']} {course['description']} {course['category']}".lower()
            for term in expanded_terms:
                if term.lower() in course_text:
                    score += 2  # Higher weight for expanded terms
            
            # Original query match
            if query.lower() in course_text:
                score += 3
            
            # Level match
            if level_filter and course['level'] == level_filter:
                score += 2
            
            # Rating boost
            score += course['rating'] * 0.5
            
            if score > 0 and course['id'] not in seen_ids:
                results.append({
                    "course_id": course["id"],
                    "title": course["title"],
                    "description": course["description"],
                    "score": float(score),
                    "level": course["level"],
                    "rating": course["rating"],
                    "matched_terms": [t for t in expanded_terms if t.lower() in course_text]
                })
                seen_ids.add(course['id'])
        
        # Sort by score
        results = sorted(results, key=lambda x: x['score'], reverse=True)[:top_k]
        
        return results
    
    def find_prerequisites(self, course_title):
        """Find prerequisites using SPARQL"""
        query = f"""
        PREFIX ont: <http://www.elearning-platform.org/ontology#>
        
        SELECT ?prereq ?title
        WHERE {{
            ?course ont:hasTitle ?courseTitle .
            FILTER(contains(lcase(?courseTitle), lcase("{course_title}")))
            ?course ont:hasPrerequisite ?prereq .
            ?prereq ont:hasTitle ?title .
        }}
        """
        
        results = []
        for row in self.g.query(query):
            results.append({
                "prerequisite": str(row.title)
            })
        
        return results
    
    def find_related_courses(self, skill):
        """Find courses teaching specific skill"""
        query = f"""
        PREFIX ont: <http://www.elearning-platform.org/ontology#>
        
        SELECT ?course ?title
        WHERE {{
            ?course ont:teachesSkill ont:{skill} .
            ?course ont:hasTitle ?title .
        }}
        """
        
        results = []
        for row in self.g.query(query):
            results.append({
                "title": str(row.title)
            })
        
        return results

# Test
if __name__ == "__main__":
    searcher = SemanticSearch()
    
    # Test query
    results = searcher.search("AI courses", top_k=5)
    
    print("\n🔍 Résultats pour 'AI courses':")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Score: {result['score']:.2f}")
        print(f"   Matched terms: {', '.join(result['matched_terms'])}")