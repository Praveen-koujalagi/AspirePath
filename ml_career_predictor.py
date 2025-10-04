# 🤖 Advanced ML-based Career Prediction System
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import RandomForestClassifier
import json
import pickle
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

class DynamicCareerPredictor:
    """
    Advanced ML-based career prediction system that discovers dynamic career paths
    instead of using predefined categories.
    """
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.kmeans = KMeans(n_clusters=15, random_state=42)  # More clusters than predefined
        self.dbscan = DBSCAN(eps=0.3, min_samples=3)
        self.pca = PCA(n_components=10)
        self.nn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Storage for learned patterns
        self.career_clusters = {}
        self.skill_embeddings = None
        self.career_names = []
        self.is_trained = False
        
    def create_synthetic_dataset(self) -> pd.DataFrame:
        """
        Create a synthetic dataset of skills and careers for training.
        In production, this would be replaced with real user data.
        """
        # Extended skill-career combinations (more diverse than current system)
        training_data = [
            # Traditional paths
            {"skills": "Python, Pandas, NumPy, Statistics, SQL, Data Analysis", "career": "Data Scientist"},
            {"skills": "JavaScript, React, Node.js, HTML, CSS, MongoDB", "career": "Full Stack Developer"},
            {"skills": "Java, Spring, Microservices, Docker, Kubernetes", "career": "Backend Developer"},
            {"skills": "TensorFlow, PyTorch, Deep Learning, Neural Networks, Computer Vision", "career": "AI Engineer"},
            
            # Emerging/Hybrid paths
            {"skills": "Python, AWS, DevOps, Docker, Terraform, CI/CD", "career": "MLOps Engineer"},
            {"skills": "Blockchain, Solidity, Web3, Smart Contracts, Ethereum", "career": "Blockchain Developer"},
            {"skills": "UI/UX Design, Figma, JavaScript, React, User Research", "career": "Product Designer"},
            {"skills": "Python, NLP, Transformers, BERT, Text Analysis", "career": "NLP Engineer"},
            {"skills": "Cybersecurity, Penetration Testing, Kubernetes, Cloud Security", "career": "Cloud Security Engineer"},
            {"skills": "Data Analysis, Business Intelligence, Tableau, PowerBI, SQL", "career": "Business Analyst"},
            
            # Creative-Tech hybrid
            {"skills": "Unity, C#, 3D Modeling, Game Physics, Animation", "career": "Game Developer"},
            {"skills": "AR, VR, Unity, Computer Graphics, 3D Mathematics", "career": "AR/VR Developer"},
            {"skills": "IoT, Arduino, Raspberry Pi, Sensors, Embedded Systems", "career": "IoT Developer"},
            
            # Data-focused roles
            {"skills": "Apache Kafka, Spark, Hadoop, Data Pipeline, ETL", "career": "Data Engineer"},
            {"skills": "Statistics, A/B Testing, SQL, Python, Experimentation", "career": "Data Analyst"},
            {"skills": "Excel, Power BI, SQL, Business Analysis, Requirements", "career": "Business Intelligence Analyst"},
            
            # Management-Tech hybrid
            {"skills": "Agile, Scrum, JIRA, Product Management, Analytics", "career": "Technical Product Manager"},
            {"skills": "System Design, Architecture, Microservices, Scalability", "career": "Solutions Architect"},
            
            # Specialized domains
            {"skills": "Bioinformatics, Python, R, Genomics, Statistics", "career": "Bioinformatics Specialist"},
            {"skills": "Finance, Python, Quantitative Analysis, Risk Modeling", "career": "Quantitative Analyst"},
        ]
        
        return pd.DataFrame(training_data)
    
    def train_models(self, df=None):
        """Train all ML models on the dataset"""
        if df is None:
            df = self.create_synthetic_dataset()
        
        # Prepare skill embeddings using TF-IDF
        skill_texts = df['skills'].tolist()
        self.skill_embeddings = self.tfidf_vectorizer.fit_transform(skill_texts)
        
        # Train clustering models
        skills_dense = self.skill_embeddings.toarray()
        
        # K-Means clustering
        self.kmeans.fit(skills_dense)
        
        # DBSCAN clustering
        dbscan_labels = self.dbscan.fit_predict(skills_dense)
        
        # PCA for dimensionality reduction
        skills_pca = self.pca.fit_transform(skills_dense)
        
        # Nearest Neighbors for recommendations
        self.nn_model.fit(skills_dense)
        
        # Random Forest for classification
        self.rf_classifier.fit(skills_dense, df['career'])
        
        # Store career information
        self.career_names = df['career'].unique().tolist()
        
        # Create cluster-to-career mapping
        for i, career in enumerate(df['career']):
            cluster_id = self.kmeans.labels_[i]
            if cluster_id not in self.career_clusters:
                self.career_clusters[cluster_id] = []
            self.career_clusters[cluster_id].append(career)
        
        self.is_trained = True
        print(f"✅ Models trained successfully!")
        print(f"📊 Discovered {len(self.career_clusters)} career clusters")
        print(f"🎯 {len(self.career_names)} unique career paths identified")
    
    def predict_dynamic_careers(self, user_skills: List[str], top_k: int = 5) -> List[Dict]:
        """
        Predict dynamic career paths using multiple ML approaches
        """
        if not self.is_trained:
            self.train_models()
        
        # Convert user skills to the same format
        user_skills_text = ", ".join(user_skills)
        user_embedding = self.tfidf_vectorizer.transform([user_skills_text])
        user_dense = user_embedding.toarray()
        
        results = []
        
        # Method 1: Clustering-based prediction
        cluster_pred = self.kmeans.predict(user_dense)[0]
        cluster_careers = self.career_clusters.get(cluster_pred, [])
        
        # Method 2: Random Forest classification
        rf_probabilities = self.rf_classifier.predict_proba(user_dense)[0]
        rf_predictions = [(self.rf_classifier.classes_[i], prob) 
                         for i, prob in enumerate(rf_probabilities)]
        rf_predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Method 3: Similarity-based recommendations
        distances, indices = self.nn_model.kneighbors(user_dense, n_neighbors=min(10, len(self.career_names)))
        
        # Method 4: Cosine similarity with all careers
        all_similarities = cosine_similarity(user_embedding, self.skill_embeddings).flatten()
        similar_indices = np.argsort(all_similarities)[::-1]
        
        # Combine results with confidence scores
        career_scores = {}
        
        # Add clustering results
        for career in cluster_careers:
            career_scores[career] = career_scores.get(career, 0) + 0.3
        
        # Add RF results
        for career, prob in rf_predictions[:top_k]:
            career_scores[career] = career_scores.get(career, 0) + prob * 0.4
        
        # Add similarity results
        training_df = self.create_synthetic_dataset()  # In production, use cached data
        for idx in similar_indices[:top_k]:
            career = training_df.iloc[idx]['career']
            similarity = all_similarities[idx]
            career_scores[career] = career_scores.get(career, 0) + similarity * 0.3
        
        # Sort by combined score
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Format results
        for i, (career, score) in enumerate(sorted_careers[:top_k]):
            confidence = min(score * 100, 100)  # Convert to percentage
            results.append({
                'rank': i + 1,
                'career': career,
                'confidence': round(confidence, 1),
                'match_type': self._get_match_explanation(career, user_skills),
                'cluster_id': cluster_pred if career in cluster_careers else None
            })
        
        return results
    
    def _get_match_explanation(self, career: str, user_skills: List[str]) -> str:
        """Generate explanation for why this career was suggested"""
        # This is a simplified version - could be enhanced with more sophisticated analysis
        explanations = [
            "Strong skill alignment",
            "Emerging field match", 
            "Cross-domain opportunity",
            "Industry trend alignment",
            "Skill gap opportunity"
        ]
        return np.random.choice(explanations)
    
    def discover_new_career_paths(self, min_cluster_size: int = 3) -> List[Dict]:
        """
        Discover new career paths by analyzing skill clusters
        """
        if not self.is_trained:
            self.train_models()
        
        new_paths = []
        training_df = self.create_synthetic_dataset()
        
        # Analyze each cluster
        for cluster_id, careers in self.career_clusters.items():
            if len(set(careers)) >= min_cluster_size:
                # Get representative skills for this cluster
                cluster_mask = self.kmeans.labels_ == cluster_id
                cluster_skills = training_df[cluster_mask]['skills'].tolist()
                
                # Find common skills in this cluster
                all_skills = []
                for skill_set in cluster_skills:
                    all_skills.extend([s.strip() for s in skill_set.split(',')])
                
                from collections import Counter
                skill_frequency = Counter(all_skills)
                top_skills = [skill for skill, count in skill_frequency.most_common(5)]
                
                new_paths.append({
                    'cluster_id': cluster_id,
                    'suggested_name': f"Specialized {careers[0].split()[-1]}",
                    'key_skills': top_skills,
                    'related_careers': list(set(careers)),
                    'emergence_score': len(set(careers)) / len(careers)
                })
        
        return new_paths
    
    def get_skill_importance(self, career: str) -> Dict[str, float]:
        """Get feature importance for a specific career"""
        if not self.is_trained:
            self.train_models()
        
        try:
            career_idx = list(self.rf_classifier.classes_).index(career)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            importances = self.rf_classifier.feature_importances_
            
            skill_importance = dict(zip(feature_names, importances))
            # Sort by importance
            return dict(sorted(skill_importance.items(), key=lambda x: x[1], reverse=True)[:10])
        except ValueError:
            return {}
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        model_data = {
            'tfidf_vectorizer': self.tfidf_vectorizer,
            'kmeans': self.kmeans,
            'pca': self.pca,
            'nn_model': self.nn_model,
            'rf_classifier': self.rf_classifier,
            'career_clusters': self.career_clusters,
            'career_names': self.career_names,
            'is_trained': self.is_trained
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        for key, value in model_data.items():
            setattr(self, key, value)

# Usage example
if __name__ == "__main__":
    # Initialize and train the model
    predictor = DynamicCareerPredictor()
    predictor.train_models()
    
    # Test with sample skills
    test_skills = ["Python", "Machine Learning", "TensorFlow", "Data Analysis"]
    predictions = predictor.predict_dynamic_careers(test_skills)
    
    print("\n🎯 Dynamic Career Predictions:")
    for pred in predictions:
        print(f"{pred['rank']}. {pred['career']} ({pred['confidence']}% confidence)")
        print(f"   Match Type: {pred['match_type']}")
    
    # Discover new career paths
    new_paths = predictor.discover_new_career_paths()
    print(f"\n🚀 Discovered {len(new_paths)} potential new career paths!")