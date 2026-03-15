"""
Analytics dan monitoring untuk TripTrove RAG System
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import pandas as pd

class Analytics:
    def __init__(self, log_file: str = "analytics.json"):
        self.log_file = Path(log_file)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load analytics data"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'queries': [],
            'sessions': [],
            'errors': []
        }
    
    def _save_data(self):
        """Save analytics data"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def log_query(self, query: str, response: str, response_time: float, 
                  success: bool = True, metadata: Dict = None):
        """Log a query"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response_length': len(response),
            'response_time': response_time,
            'success': success,
            'metadata': metadata or {}
        }
        self.data['queries'].append(entry)
        self._save_data()
    
    def log_session(self, session_id: str, duration: float, 
                    num_queries: int, metadata: Dict = None):
        """Log a session"""
        entry = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'num_queries': num_queries,
            'metadata': metadata or {}
        }
        self.data['sessions'].append(entry)
        self._save_data()
    
    def log_error(self, error_type: str, error_message: str, 
                  context: Dict = None):
        """Log an error"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'error_message': error_message,
            'context': context or {}
        }
        self.data['errors'].append(entry)
        self._save_data()
    
    def get_stats(self, days: int = 7) -> Dict:
        """Get statistics for last N days"""
        cutoff = datetime.now() - timedelta(days=days)
        
        recent_queries = [
            q for q in self.data['queries']
            if datetime.fromisoformat(q['timestamp']) > cutoff
        ]
        
        recent_errors = [
            e for e in self.data['errors']
            if datetime.fromisoformat(e['timestamp']) > cutoff
        ]
        
        if not recent_queries:
            return {
                'total_queries': 0,
                'successful_queries': 0,
                'failed_queries': 0,
                'avg_response_time': 0,
                'success_rate': 0,
                'total_errors': 0
            }
        
        successful = [q for q in recent_queries if q['success']]
        failed = [q for q in recent_queries if not q['success']]
        
        avg_time = sum(q['response_time'] for q in recent_queries) / len(recent_queries)
        
        return {
            'total_queries': len(recent_queries),
            'successful_queries': len(successful),
            'failed_queries': len(failed),
            'avg_response_time': round(avg_time, 2),
            'success_rate': round(len(successful) / len(recent_queries) * 100, 1),
            'total_errors': len(recent_errors)
        }
    
    def get_popular_queries(self, limit: int = 10) -> List[Dict]:
        """Get most popular query patterns"""
        from collections import Counter
        
        # Extract keywords from queries
        keywords = []
        for q in self.data['queries']:
            words = q['query'].lower().split()
            keywords.extend(words)
        
        counter = Counter(keywords)
        # Filter out common words
        stop_words = {'apa', 'yang', 'ada', 'untuk', 'dengan', 'dari', 'ke', 'di'}
        filtered = [(k, v) for k, v in counter.most_common(limit * 2) 
                   if k not in stop_words]
        
        return [{'keyword': k, 'count': v} for k, v in filtered[:limit]]
    
    def get_performance_trend(self, days: int = 7) -> pd.DataFrame:
        """Get performance trend"""
        cutoff = datetime.now() - timedelta(days=days)
        
        recent_queries = [
            q for q in self.data['queries']
            if datetime.fromisoformat(q['timestamp']) > cutoff
        ]
        
        if not recent_queries:
            return pd.DataFrame()
        
        df = pd.DataFrame(recent_queries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        daily_stats = df.groupby('date').agg({
            'response_time': 'mean',
            'success': 'sum',
            'query': 'count'
        }).reset_index()
        
        daily_stats.columns = ['date', 'avg_response_time', 'successful', 'total']
        daily_stats['success_rate'] = (daily_stats['successful'] / daily_stats['total'] * 100).round(1)
        
        return daily_stats
    
    def export_report(self, filename: str = None, days: int = 7):
        """Export analytics report"""
        if filename is None:
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d')}.txt"
        
        stats = self.get_stats(days)
        popular = self.get_popular_queries()
        
        report = f"""
TripTrove RAG Analytics Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Period: Last {days} days

=== OVERVIEW ===
Total Queries: {stats['total_queries']}
Successful: {stats['successful_queries']}
Failed: {stats['failed_queries']}
Success Rate: {stats['success_rate']}%
Avg Response Time: {stats['avg_response_time']}s
Total Errors: {stats['total_errors']}

=== POPULAR KEYWORDS ===
"""
        for i, item in enumerate(popular, 1):
            report += f"{i}. {item['keyword']}: {item['count']} times\n"
        
        report += "\n=== RECENT ERRORS ===\n"
        recent_errors = self.data['errors'][-10:]
        for error in recent_errors:
            report += f"[{error['timestamp']}] {error['error_type']}: {error['error_message']}\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Report exported to {filename}")
        return filename

if __name__ == "__main__":
    # Test analytics
    analytics = Analytics()
    
    # Simulate some queries
    analytics.log_query("Paket tour ke Bali?", "Response...", 2.5, True)
    analytics.log_query("Harga tour?", "Response...", 1.8, True)
    
    # Get stats
    stats = analytics.get_stats()
    print("Statistics:", stats)
    
    # Export report
    analytics.export_report()
