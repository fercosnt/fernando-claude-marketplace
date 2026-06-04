#!/usr/bin/env python3
"""Chunk and Optimize - Multi-mode chunking for RAG"""
import json, sys

class ChunkOptimizer:
    def __init__(self, content, chunk_size=512, overlap=0.15):
        self.content = content
        self.chunk_size = chunk_size
        self.overlap_size = int(chunk_size * overlap)
    
    def chunk_semantic(self):
        paragraphs = [p.strip() for p in self.content.split('\n\n') if p.strip()]
        chunks = []
        current = []
        current_tokens = 0
        
        for para in paragraphs:
            para_tokens = len(para.split()) * 1.33
            if current_tokens + para_tokens > self.chunk_size and current:
                chunks.append({
                    "id": f"chunk_{len(chunks):03d}",
                    "content": '\n\n'.join(current),
                    "token_count": int(current_tokens)
                })
                current = [current[-1]] if current else []
                current_tokens = len(' '.join(current).split()) * 1.33
            current.append(para)
            current_tokens += para_tokens
        
        if current:
            chunks.append({
                "id": f"chunk_{len(chunks):03d}",
                "content": '\n\n'.join(current),
                "token_count": int(current_tokens)
            })
        return chunks
    
    def transform_rag_standard(self):
        chunks = self.chunk_semantic()
        for i, chunk in enumerate(chunks):
            chunk["metadata"] = {
                "chunk_index": i,
                "total_chunks": len(chunks),
                "content_type": "general"
            }
        return {"format": "rag_standard", "chunks": chunks}
    
    def transform_claude_project(self):
        output = '<document>\n\n'
        for para in [p for p in self.content.split('\n\n') if p.strip()]:
            output += para + '\n\n'
        output += '</document>'
        return output

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: chunk_and_optimize.py <file> <mode>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        content = f.read()
    
    opt = ChunkOptimizer(content)
    mode = sys.argv[2]
    
    if mode == 'rag':
        print(json.dumps(opt.transform_rag_standard(), indent=2, ensure_ascii=False))
    elif mode == 'claude':
        print(opt.transform_claude_project())
