import os
import re
from datetime import datetime

class PublisherAgent:
    """
    Action Layer Agent grounded in 'Agents in Trustworthy' (Section 2.1.5).
    Formats and writes articles to the _posts folder.
    """

    def __init__(self, posts_dir="../../_posts"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.posts_dir = os.path.abspath(os.path.join(script_dir, posts_dir))

    def publish(self, title, content, date_str=None, categories="news"):
        """
        Creates a Jekyll markdown post.
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Create slug from title
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        filename = f"{date_str}-{slug}.md"
        filepath = os.path.join(self.posts_dir, filename)
        
        # Ensure posts directory exists
        os.makedirs(self.posts_dir, exist_ok=True)
        
        frontmatter = f"""---
layout: post
title: "{title}"
date: {date_str}
categories: {categories}
---

"""
        full_content = frontmatter + content
        
        with open(filepath, 'w') as f:
            f.write(full_content)
        
        return filepath

if __name__ == "__main__":
    publisher = PublisherAgent()
    print(publisher.publish("Test Title", "Test content with source [link](http://example.com)"))
