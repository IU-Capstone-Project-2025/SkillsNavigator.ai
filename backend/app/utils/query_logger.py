import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class QueryLogger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        self.queries_log_file = self.logs_dir / "generated_queries.log"

    def log_queries(self, area: str, current_level: str, desired_skills: str, queries: List[str], source: str = "deepseek"):
        """Log generated queries to a file with timestamp and context"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = {
            "timestamp": timestamp,
            "source": source,
            "user_input": {
                "area": area,
                "current_level": current_level,
                "desired_skills": desired_skills
            },
            "generated_queries": queries
        }
        
        try:
            with open(self.queries_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False, indent=2) + "\n" + "-" * 80 + "\n")
            logger.info(f"Queries logged to {self.queries_log_file}")
        except Exception as e:
            logger.error(f"Failed to log queries to file: {e}")

    def log_search_results(self, query: str, results: List[dict], similarity_threshold: float):
        """Log search results with similarity scores"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = {
            "timestamp": timestamp,
            "query": query,
            "similarity_threshold": similarity_threshold,
            "total_results": len(results),
            "results": [],
            "best_course": None,
            "best_score": 0.0
        }
        
        for result in results:
            course_info = {
                "course_title": result.payload.get("title", "Unknown"),
                "course_id": result.payload.get("id", "Unknown"),
                "similarity_score": result.score,
                "passed_threshold": result.score >= similarity_threshold
            }
            log_entry["results"].append(course_info)
            
            # Track the best course that meets the threshold
            if result.score >= similarity_threshold and result.score > log_entry["best_score"]:
                log_entry["best_score"] = result.score
                log_entry["best_course"] = course_info
        
        try:
            with open(self.queries_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False, indent=2) + "\n" + "-" * 80 + "\n")
            logger.info(f"Search results logged to {self.queries_log_file}")
        except Exception as e:
            logger.error(f"Failed to log search results to file: {e}")


# Create a global instance
query_logger = QueryLogger() 