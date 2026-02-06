"""Content aggregation utilities"""

class ContentAggregator:
    """Aggregates and processes scraped content"""
    
    def __init__(self):
        pass
    
    def aggregate(self, pages):
        """Aggregate content from multiple pages"""
        return "\n\n".join([p.content for p in pages if p.extraction_success])


