import logging
import json
from typing import List, Dict, Optional
from datetime import datetime
import re
from config.config import config

logger = logging.getLogger(__name__)


class BehaviorAnalyzer:    
    CATEGORY_KEYWORDS = {
        "electronics": ["laptop", "phone", "tablet", "computer", "headphones", "speaker", "camera", "tv", "monitor"],
        "fashion": ["shirt", "dress", "jeans", "shoes", "jacket", "clothing", "apparel", "fashion"],
        "home": ["furniture", "decor", "kitchen", "bedding", "appliances", "home"],
        "sports": ["fitness", "gym", "yoga", "sports", "exercise", "workout"],
        "books": ["book", "novel", "magazine", "reading", "literature"],
        "beauty": ["cosmetics", "skincare", "makeup", "beauty", "fragrance"],
        "toys": ["toy", "game", "kids", "children", "baby"],
    }
    
    PURCHASE_INTENT_SIGNALS = [
        "buy", "purchase", "looking for", "need", "want", "interested in",
        "price", "cost", "how much", "available", "in stock", "delivery"
    ]
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_product_interests(self, message: str) -> List[str]:
        message_lower = message.lower()
        interests = []
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    if category not in interests:
                        interests.append(category)
                    break
        
        return interests
    
    def detect_purchase_intent(self, message: str) -> float:
        message_lower = message.lower()
        matches = 0
        
        for signal in self.PURCHASE_INTENT_SIGNALS:
            if signal in message_lower:
                matches += 1
        
        score = min(matches / config.INTENT_MATCH_DIVISOR, 1.0)
        return score
    
    def analyze_chat_history(self, chat_history: List[Dict]) -> Dict:
        all_interests = []
        total_intent = 0
        message_count = 0
        
        for msg in chat_history:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                
                interests = self.extract_product_interests(content)
                all_interests.extend(interests)
                
                intent = self.detect_purchase_intent(content)
                total_intent += intent
                message_count += 1
        
        category_counts = {}
        for interest in all_interests:
            category_counts[interest] = category_counts.get(interest, 0) + 1
        
        top_interests = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        
        avg_intent = total_intent / message_count if message_count > 0 else 0
        
        return {
            "top_interests": [cat for cat, _ in top_interests[:3]],
            "all_interests": category_counts,
            "purchase_intent": round(avg_intent, 2),
            "engagement_level": "high" if message_count > config.HIGH_ENGAGEMENT_MESSAGE_COUNT else "medium" if message_count > config.MEDIUM_ENGAGEMENT_MESSAGE_COUNT else "low"
        }


class RecommendationEngine:    
    def __init__(self, product_catalog_path: str = None):
        self.behavior_analyzer = BehaviorAnalyzer()
        catalog_path = product_catalog_path or config.PRODUCT_CATALOG_PATH
        self.product_catalog = self._load_product_catalog(catalog_path)
        self.logger = logging.getLogger(__name__)
    
    def _load_product_catalog(self, path: str) -> List[Dict]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("products", [])
        except FileNotFoundError:
            self.logger.warning(f"Product catalog not found at {path}")
            return []
        except Exception as e:
            self.logger.error(f"Error loading product catalog: {str(e)}")
            return []
    
    def analyze_user_behavior(self, chat_history: List[Dict]) -> Dict:
        return self.behavior_analyzer.analyze_chat_history(chat_history)
    
    def get_product_recommendations(
        self, 
        user_profile: Dict, 
        limit: int = None,
        llm_client = None
    ) -> List[Dict]:
        if not self.product_catalog:
            return []
        
        if limit is None:
            limit = config.MAX_RECOMMENDATIONS
        
        top_interests = user_profile.get("top_interests", [])
        
        if not top_interests:
            return self.product_catalog[:limit]
        
        recommended = []
        for product in self.product_catalog:
            product_category = product.get("category", "").lower()
            
            for interest in top_interests:
                if interest in product_category:
                    product_copy = product.copy()
                    product_copy["relevance_score"] = self._calculate_relevance(
                        product, user_profile
                    )
                    recommended.append(product_copy)
                    break
        
        recommended.sort(
            key=lambda x: (x.get("relevance_score", 0), x.get("rating", 0)), 
            reverse=True
        )
        
        return recommended[:limit]
    
    def _calculate_relevance(self, product: Dict, user_profile: Dict) -> float:
        score = 0.0
        
        category = product.get("category", "").lower()
        all_interests = user_profile.get("all_interests", {})
        
        for interest, count in all_interests.items():
            if interest in category:
                score += (count * config.CATEGORY_MATCH_WEIGHT)
        
        rating = product.get("rating", 0)
        score += (rating / 5.0) * config.RATING_WEIGHT
        
        if product.get("stock") == "in-stock":
            score += config.STOCK_AVAILABILITY_WEIGHT
        
        intent = user_profile.get("purchase_intent", 0)
        score *= (1 + intent)
        
        return recommended[:limit]
    
    def should_show_recommendations(
        self, 
        user_profile: Dict,
        messages_since_last: int
    ) -> bool:
        if user_profile.get("purchase_intent", 0) > config.HIGH_PURCHASE_INTENT_THRESHOLD and messages_since_last >= config.MIN_MESSAGES_FOR_RECOMMENDATION:
            return True
        
        if user_profile.get("engagement_level") == "high" and messages_since_last >= config.ENGAGED_USER_RECOMMENDATION_INTERVAL:
            return True
        
        return False
