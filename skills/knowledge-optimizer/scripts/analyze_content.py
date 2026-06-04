#!/usr/bin/env python3
"""Content Quality Analyzer - Analyzes text for RAG optimization opportunities"""
import re, json, sys
from collections import Counter

class ContentAnalyzer:
    FILLERS_PT = ['então', 'né', 'tipo', 'assim', 'ahn', 'bom', 'tá']
    
    def __init__(self, content):
        self.content = content
        self.sentences = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]
        self.words = content.lower().split()
    
    def analyze(self):
        # Redundancy
        sent_counts = Counter(s.lower() for s in self.sentences)
        duplicates = sum(c-1 for c in sent_counts.values() if c > 1)
        redundancy_pct = (duplicates/len(self.sentences)*100) if self.sentences else 0
        
        # Language quality
        filler_count = sum(1 for w in self.words if w in self.FILLERS_PT)
        filler_pct = (filler_count/len(self.words)*100) if self.words else 0
        avg_sent_len = sum(len(s.split()) for s in self.sentences)/len(self.sentences) if self.sentences else 0
        clarity = min(10, max(1, 10 - filler_pct/2))
        
        # Structure
        headings = len(re.findall(r'^#+\s+', self.content, re.MULTILINE))
        has_lists = bool(re.search(r'^\s*[-*]\s+', self.content, re.MULTILINE))
        structure_score = min(10, (3 if headings else 0) + (2 if has_lists else 0) + 3)
        
        return {
            "summary": {
                "word_count": len(self.words),
                "token_estimate": int(len(self.words) * 1.33),
                "overall_quality": round((clarity + structure_score)/2, 1)
            },
            "redundancy": {"percentage": round(redundancy_pct, 1), "duplicates": len([c for c in sent_counts.values() if c > 1])},
            "language": {"filler_pct": round(filler_pct, 1), "clarity_score": round(clarity, 1)},
            "structure": {"heading_count": headings, "structure_score": structure_score}
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: analyze_content.py <file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        report = ContentAnalyzer(f.read()).analyze()
    
    print(json.dumps(report, indent=2, ensure_ascii=False))
