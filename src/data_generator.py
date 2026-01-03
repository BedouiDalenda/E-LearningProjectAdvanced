import json
import os

def generate_courses():
    """Génère 120 cours avec des mots-clés RÉELS dans les titres"""
    
    # Courses réalistes avec keywords visibles
    course_templates = [
        # AI/ML - 20 cours
        {"title": "Introduction to Python Programming", "category": "Programming", "skills": ["Python", "Programming"], "level": "Beginner", "duration": 40, "rating": 4.8},
        {"title": "Advanced Python Programming", "category": "Programming", "skills": ["Python", "OOP"], "level": "Advanced", "duration": 60, "rating": 4.7},
        {"title": "Python for Data Science", "category": "Data Science", "skills": ["Python", "Data Analysis"], "level": "Intermediate", "rating": 4.6},
        {"title": "Machine Learning with Python", "category": "AI/ML", "skills": ["Machine Learning", "Python"], "level": "Intermediate", "duration": 50, "rating": 4.9},
        {"title": "Deep Learning Fundamentals", "category": "AI/ML", "skills": ["Deep Learning", "Neural Networks"], "level": "Advanced", "duration": 70, "rating": 4.8},
        {"title": "Computer Vision with Python", "category": "AI/ML", "skills": ["Computer Vision", "Python"], "level": "Advanced", "duration": 65, "rating": 4.7},
        {"title": "Natural Language Processing", "category": "AI/ML", "skills": ["NLP", "Machine Learning"], "level": "Advanced", "duration": 60, "rating": 4.6},
        {"title": "Introduction to Artificial Intelligence", "category": "AI/ML", "skills": ["AI", "Machine Learning"], "level": "Beginner", "duration": 45, "rating": 4.5},
        {"title": "Neural Networks from Scratch", "category": "AI/ML", "skills": ["Neural Networks", "Python"], "level": "Advanced", "duration": 55, "rating": 4.7},
        {"title": "Reinforcement Learning", "category": "AI/ML", "skills": ["Reinforcement Learning", "AI"], "level": "Advanced", "duration": 60, "rating": 4.6},
        
        # Web Development - 20 cours
        {"title": "Web Development Bootcamp", "category": "Web Dev", "skills": ["HTML", "CSS", "JavaScript"], "level": "Beginner", "duration": 80, "rating": 4.8},
        {"title": "Frontend Development with React", "category": "Web Dev", "skills": ["React", "JavaScript"], "level": "Intermediate", "duration": 50, "rating": 4.7},
        {"title": "Backend Development with Node.js", "category": "Web Dev", "skills": ["Node.js", "JavaScript"], "level": "Intermediate", "duration": 55, "rating": 4.6},
        {"title": "Full Stack Web Development", "category": "Web Dev", "skills": ["React", "Node.js"], "level": "Advanced", "duration": 100, "rating": 4.9},
        {"title": "JavaScript Essentials", "category": "Web Dev", "skills": ["JavaScript", "Programming"], "level": "Beginner", "duration": 35, "rating": 4.5},
        {"title": "HTML and CSS Fundamentals", "category": "Web Dev", "skills": ["HTML", "CSS"], "level": "Beginner", "duration": 30, "rating": 4.4},
        {"title": "Advanced CSS Techniques", "category": "Web Dev", "skills": ["CSS", "Web Design"], "level": "Intermediate", "duration": 40, "rating": 4.5},
        {"title": "React Native Mobile Development", "category": "Web Dev", "skills": ["React", "Mobile"], "level": "Advanced", "duration": 60, "rating": 4.6},
        {"title": "Web Security Best Practices", "category": "Web Dev", "skills": ["Security", "Web"], "level": "Advanced", "duration": 45, "rating": 4.7},
        {"title": "RESTful API Development", "category": "Web Dev", "skills": ["API", "Backend"], "level": "Intermediate", "duration": 40, "rating": 4.6},
        
        # Data Science - 20 cours
        {"title": "Data Analysis with Python", "category": "Data Science", "skills": ["Data Analysis", "Python"], "level": "Beginner", "duration": 45, "rating": 4.8},
        {"title": "Data Visualization Masterclass", "category": "Data Science", "skills": ["Data Visualization", "Python"], "level": "Intermediate", "duration": 35, "rating": 4.6},
        {"title": "Statistics for Data Science", "category": "Data Science", "skills": ["Statistics", "Data Analysis"], "level": "Beginner", "duration": 40, "rating": 4.5},
        {"title": "Big Data with Hadoop", "category": "Data Science", "skills": ["Big Data", "Hadoop"], "level": "Advanced", "duration": 60, "rating": 4.7},
        {"title": "SQL for Data Analysis", "category": "Data Science", "skills": ["SQL", "Databases"], "level": "Beginner", "duration": 30, "rating": 4.6},
        {"title": "Advanced SQL Queries", "category": "Data Science", "skills": ["SQL", "Database"], "level": "Intermediate", "duration": 35, "rating": 4.5},
        {"title": "Data Mining Techniques", "category": "Data Science", "skills": ["Data Mining", "Machine Learning"], "level": "Advanced", "duration": 50, "rating": 4.7},
        {"title": "Business Analytics", "category": "Data Science", "skills": ["Analytics", "Business"], "level": "Intermediate", "duration": 45, "rating": 4.4},
        {"title": "Introduction to Data Science", "category": "Data Science", "skills": ["Data Science", "Python"], "level": "Beginner", "duration": 50, "rating": 4.8},
        {"title": "Time Series Analysis", "category": "Data Science", "skills": ["Time Series", "Statistics"], "level": "Advanced", "duration": 40, "rating": 4.6},
        
        # Programming - 30 cours
        {"title": "Java Programming Fundamentals", "category": "Programming", "skills": ["Java", "Programming"], "level": "Beginner", "duration": 45, "rating": 4.5},
        {"title": "Advanced Java Programming", "category": "Programming", "skills": ["Java", "OOP"], "level": "Advanced", "duration": 55, "rating": 4.6},
        {"title": "C++ for Beginners", "category": "Programming", "skills": ["C++", "Programming"], "level": "Beginner", "duration": 40, "rating": 4.4},
        {"title": "Object-Oriented Programming", "category": "Programming", "skills": ["OOP", "Programming"], "level": "Intermediate", "duration": 35, "rating": 4.6},
        {"title": "Data Structures and Algorithms", "category": "Programming", "skills": ["Algorithms", "Data Structures"], "level": "Intermediate", "duration": 60, "rating": 4.8},
        {"title": "Design Patterns in Programming", "category": "Programming", "skills": ["Design Patterns", "OOP"], "level": "Advanced", "duration": 45, "rating": 4.7},
        {"title": "Python for Automation", "category": "Programming", "skills": ["Python", "Automation"], "level": "Intermediate", "duration": 30, "rating": 4.5},
        {"title": "Git and Version Control", "category": "Programming", "skills": ["Git", "DevOps"], "level": "Beginner", "duration": 20, "rating": 4.6},
        {"title": "Introduction to Programming", "category": "Programming", "skills": ["Programming", "Logic"], "level": "Beginner", "duration": 40, "rating": 4.7},
        {"title": "Functional Programming", "category": "Programming", "skills": ["Functional", "Programming"], "level": "Advanced", "duration": 50, "rating": 4.5},
        
        # DevOps - 30 cours
        {"title": "Docker Fundamentals", "category": "DevOps", "skills": ["Docker", "Containers"], "level": "Intermediate", "duration": 25, "rating": 4.7},
        {"title": "Kubernetes Essentials", "category": "DevOps", "skills": ["Kubernetes", "DevOps"], "level": "Advanced", "duration": 35, "rating": 4.8},
        {"title": "CI/CD Pipeline Development", "category": "DevOps", "skills": ["CI/CD", "Automation"], "level": "Intermediate", "duration": 30, "rating": 4.6},
        {"title": "AWS Cloud Computing", "category": "DevOps", "skills": ["AWS", "Cloud"], "level": "Intermediate", "duration": 50, "rating": 4.7},
        {"title": "Azure Cloud Platform", "category": "DevOps", "skills": ["Azure", "Cloud"], "level": "Intermediate", "duration": 45, "rating": 4.6},
        {"title": "Google Cloud Platform", "category": "DevOps", "skills": ["GCP", "Cloud"], "level": "Intermediate", "duration": 45, "rating": 4.5},
        {"title": "Infrastructure as Code", "category": "DevOps", "skills": ["IaC", "Terraform"], "level": "Advanced", "duration": 40, "rating": 4.7},
        {"title": "Linux System Administration", "category": "DevOps", "skills": ["Linux", "System Admin"], "level": "Intermediate", "duration": 50, "rating": 4.6},
        {"title": "Monitoring and Logging", "category": "DevOps", "skills": ["Monitoring", "DevOps"], "level": "Advanced", "duration": 30, "rating": 4.5},
        {"title": "DevOps Best Practices", "category": "DevOps", "skills": ["DevOps", "Best Practices"], "level": "Intermediate", "duration": 35, "rating": 4.6},
    ]
    
    courses = []
    for i, template in enumerate(course_templates, 1):
        course = {
            "id": f"Course_{i}",
            "title": template["title"],
            "description": f"Learn {template['title']}. Master {', '.join(template['skills'])} with hands-on projects and real-world examples. Suitable for {template['level']} level students.",
            "level": template["level"],
            "category": template["category"],
            "skills": template["skills"],
            "duration": template.get("duration", 40 + (i % 60)),
            "difficulty": ["Beginner", "Intermediate", "Advanced"].index(template["level"]) + 1,
            "rating": template.get("rating", 4.0 + (i % 10) / 10),
            "price": 100 + (i * 10) % 500
        }
        courses.append(course)
    
    # Dupliquer pour atteindre 120 cours (avec variantes)
    variations = ["Practical", "Complete", "Crash Course in"]
    while len(courses) < 120:
        base_course = courses[len(courses) % len(course_templates)]
        variant = variations[len(courses) % len(variations)]
        
        new_course = base_course.copy()
        new_course["id"] = f"Course_{len(courses) + 1}"
        new_course["title"] = f"{variant} {base_course['title']}"
        new_course["description"] = f"{variant} guide to {base_course['title'].lower()}. {base_course['description']}"
        new_course["duration"] = base_course["duration"] + 10
        new_course["price"] = base_course["price"] + 50
        
        courses.append(new_course)
    
    return courses[:120]

def generate_queries():
    """Génère 20 requêtes de test"""
    queries = [
        # Simple (5)
        {"id": 1, "query": "Python programming", "type": "simple"},
        {"id": 2, "query": "Machine Learning course", "type": "simple"},
        {"id": 3, "query": "Web development", "type": "simple"},
        {"id": 4, "query": "Data analysis", "type": "simple"},
        {"id": 5, "query": "Introduction to AI", "type": "simple"},
        
        # Complex (7)
        {"id": 6, "query": "Advanced AI courses with Python", "type": "complex"},
        {"id": 7, "query": "Beginner data science courses", "type": "complex"},
        {"id": 8, "query": "Machine learning courses for intermediate level", "type": "complex"},
        {"id": 9, "query": "Courses related to web development and databases", "type": "complex"},
        {"id": 10, "query": "Advanced programming with high rating", "type": "complex"},
        {"id": 11, "query": "Deep learning courses requiring Python", "type": "complex"},
        {"id": 12, "query": "DevOps courses for cloud computing", "type": "complex"},
        
        # Ambiguous (5)
        {"id": 13, "query": "AI courses", "type": "ambiguous"},
        {"id": 14, "query": "Programming", "type": "ambiguous"},
        {"id": 15, "query": "Data", "type": "ambiguous"},
        {"id": 16, "query": "Advanced courses", "type": "ambiguous"},
        {"id": 17, "query": "Practical learning", "type": "ambiguous"},
        
        # Relational (3)
        {"id": 18, "query": "Courses after learning Python", "type": "relational"},
        {"id": 19, "query": "Similar to Machine Learning", "type": "relational"},
        {"id": 20, "query": "Prerequisites for Deep Learning", "type": "relational"}
    ]
    return queries

if __name__ == "__main__":
    print("🚀 Génération des données...")
    
    # Créer dossier
    os.makedirs("data", exist_ok=True)
    
    # Générer cours
    courses = generate_courses()
    with open("data/courses_data.json", 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(courses)} cours sauvegardés")
    
    # Vérification
    python_count = sum(1 for c in courses if "python" in c['title'].lower() or "python" in ' '.join(c['skills']).lower())
    print(f"   → {python_count} cours contiennent 'Python'")
    
    ml_count = sum(1 for c in courses if "machine learning" in c['title'].lower() or "machine learning" in ' '.join(c['skills']).lower())
    print(f"   → {ml_count} cours contiennent 'Machine Learning'")
    
    # Générer requêtes
    queries = generate_queries()
    with open("data/queries.json", 'w', encoding='utf-8') as f:
        json.dump(queries, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(queries)} requêtes sauvegardées")
    
    print("\n✅ Génération terminée!")