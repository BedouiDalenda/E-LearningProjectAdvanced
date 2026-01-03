import json

def generate_relevance_judgments():
    """
    Génère les relevance judgments pour toutes les requêtes
    Format: {query_id: {course_id: relevance_score}}
    
    Relevance scores:
    - 3: Highly relevant (parfaitement adapté à la requête)
    - 2: Relevant (correspond bien)
    - 1: Slightly relevant (partiellement pertinent)
    - 0: Not relevant (non pertinent)
    """
    
    # Charger les cours et requêtes
    with open("data/courses_data.json", 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    with open("data/queries.json", 'r', encoding='utf-8') as f:
        queries = json.load(f)
    
    relevance = {}
    
    # Définir les critères pour chaque requête
    query_criteria = {
        1: {  # "Python programming"
            "keywords": ["python", "programming"],
            "exact_match_bonus": ["python programming"],
            "min_keywords": 1
        },
        2: {  # "Machine Learning course"
            "keywords": ["machine learning", "ml"],
            "exact_match_bonus": ["machine learning"],
            "min_keywords": 1
        },
        3: {  # "Web development"
            "keywords": ["web", "frontend", "backend", "html", "css", "javascript"],
            "exact_match_bonus": ["web development", "web dev"],
            "min_keywords": 1
        },
        4: {  # "Data analysis"
            "keywords": ["data analysis", "data", "analytics"],
            "exact_match_bonus": ["data analysis"],
            "min_keywords": 1
        },
        5: {  # "Introduction to AI"
            "keywords": ["artificial intelligence", "ai", "introduction"],
            "levels": ["Beginner"],
            "min_keywords": 1
        },
        6: {  # "Advanced AI courses with Python"
            "keywords": ["ai", "artificial intelligence", "python"],
            "levels": ["Advanced"],
            "min_keywords": 2
        },
        7: {  # "Beginner data science courses"
            "keywords": ["data science", "data analysis", "data"],
            "levels": ["Beginner"],
            "min_keywords": 1
        },
        8: {  # "Machine learning courses for intermediate level"
            "keywords": ["machine learning", "ml"],
            "levels": ["Intermediate"],
            "min_keywords": 1
        },
        9: {  # "Courses related to web development and databases"
            "keywords": ["web", "database", "sql", "backend"],
            "min_keywords": 1
        },
        10: {  # "Advanced programming with high rating"
            "keywords": ["programming", "advanced"],
            "levels": ["Advanced"],
            "min_rating": 4.5,
            "min_keywords": 1
        },
        11: {  # "Deep learning courses requiring Python"
            "keywords": ["deep learning", "python", "neural networks"],
            "min_keywords": 2
        },
        12: {  # "DevOps courses for cloud computing"
            "keywords": ["devops", "cloud", "aws", "azure", "gcp"],
            "min_keywords": 1
        },
        13: {  # "AI courses"
            "keywords": ["ai", "artificial intelligence", "machine learning", "deep learning", "neural networks"],
            "min_keywords": 1
        },
        14: {  # "Programming"
            "keywords": ["programming", "python", "java", "c++", "javascript"],
            "min_keywords": 1
        },
        15: {  # "Data"
            "keywords": ["data", "data science", "data analysis", "big data"],
            "min_keywords": 1
        },
        16: {  # "Advanced courses"
            "levels": ["Advanced"],
            "min_keywords": 0
        },
        17: {  # "Practical learning"
            "keywords": ["practical", "hands-on", "projects"],
            "min_keywords": 1
        },
        18: {  # "Courses after learning Python"
            "keywords": ["machine learning", "data science", "web", "advanced python"],
            "exclude_keywords": ["introduction", "beginner"],
            "min_keywords": 1
        },
        19: {  # "Similar to Machine Learning"
            "keywords": ["machine learning", "ai", "deep learning", "data science"],
            "min_keywords": 1
        },
        20: {  # "Prerequisites for Deep Learning"
            "keywords": ["python", "machine learning", "mathematics", "linear algebra"],
            "levels": ["Beginner", "Intermediate"],
            "min_keywords": 1
        }
    }
    
    # Calculer la pertinence pour chaque requête
    for query_id, criteria in query_criteria.items():
        relevance[query_id] = {}
        
        for course in courses:
            # Construire le texte de recherche
            search_text = (
                f"{course['title']} "
                f"{course['description']} "
                f"{course['category']} "
                f"{' '.join(course.get('skills', []))}"
            ).lower()
            
            # Compter les matches
            keyword_matches = 0
            exact_match = False
            
            if "keywords" in criteria:
                for keyword in criteria["keywords"]:
                    if keyword.lower() in search_text:
                        keyword_matches += 1
            
            if "exact_match_bonus" in criteria:
                for exact in criteria["exact_match_bonus"]:
                    if exact.lower() in search_text:
                        exact_match = True
            
            # Vérifier les exclusions
            if "exclude_keywords" in criteria:
                excluded = any(ex.lower() in search_text for ex in criteria["exclude_keywords"])
                if excluded:
                    continue
            
            # Vérifier le niveau
            level_match = True
            if "levels" in criteria:
                level_match = course["level"] in criteria["levels"]
            
            # Vérifier le rating
            rating_match = True
            if "min_rating" in criteria:
                rating_match = course["rating"] >= criteria["min_rating"]
            
            # Calculer le score de pertinence
            min_keywords = criteria.get("min_keywords", 1)
            
            if exact_match and level_match and rating_match:
                relevance[query_id][course["id"]] = 3  # Highly relevant
            elif keyword_matches >= min_keywords + 1 and level_match and rating_match:
                relevance[query_id][course["id"]] = 3  # Highly relevant
            elif keyword_matches >= min_keywords and level_match and rating_match:
                relevance[query_id][course["id"]] = 2  # Relevant
            elif keyword_matches > 0 and (level_match or rating_match):
                relevance[query_id][course["id"]] = 1  # Slightly relevant
    
    return relevance

def save_relevance_judgments():
    """Sauvegarde les relevance judgments"""
    relevance = generate_relevance_judgments()
    
    with open("data/relevance_judgments.json", 'w', encoding='utf-8') as f:
        json.dump(relevance, f, indent=2)
    
    # Statistiques
    print("✅ Relevance judgments générés et sauvegardés\n")
    print("📊 Statistiques par requête:")
    
    with open("data/queries.json", 'r', encoding='utf-8') as f:
        queries = json.load(f)
    
    for query in queries:
        qid = query['id']
        if qid in relevance:
            relevant_courses = relevance[qid]
            highly_relevant = sum(1 for score in relevant_courses.values() if score == 3)
            relevant = sum(1 for score in relevant_courses.values() if score == 2)
            slightly = sum(1 for score in relevant_courses.values() if score == 1)
            
            print(f"\nQuery {qid}: {query['query']}")
            print(f"  Highly relevant (3): {highly_relevant}")
            print(f"  Relevant (2): {relevant}")
            print(f"  Slightly relevant (1): {slightly}")
            print(f"  Total: {len(relevant_courses)}")

if __name__ == "__main__":
    save_relevance_judgments()