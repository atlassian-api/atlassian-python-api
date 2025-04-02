#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from atlassian import ConfluenceV2

"""
This example shows how to work with comments in Confluence using the API v2
"""

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get Confluence credentials from environment variables
CONFLUENCE_URL = os.environ.get('CONFLUENCE_URL', 'https://example.atlassian.net')
CONFLUENCE_USERNAME = os.environ.get('CONFLUENCE_USERNAME', 'email@example.com')
CONFLUENCE_PASSWORD = os.environ.get('CONFLUENCE_PASSWORD', 'api-token')

# Create the ConfluenceV2 client
confluence = ConfluenceV2(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_USERNAME,
    password=CONFLUENCE_PASSWORD
)

def print_comment(comment, indent=""):
    """Helper function to print a comment in a readable format"""
    comment_id = comment.get('id', 'unknown')
    body = comment.get('body', {}).get('storage', {}).get('value', 'No content')
    created_by = comment.get('createdBy', {}).get('displayName', 'unknown')
    created_at = comment.get('createdAt', 'unknown')
    
    print(f"{indent}Comment ID: {comment_id}")
    print(f"{indent}Created by: {created_by} at {created_at}")
    print(f"{indent}Content: {body[:100]}..." if len(body) > 100 else f"{indent}Content: {body}")
    
    if 'resolved' in comment:
        print(f"{indent}Resolved: {comment.get('resolved', False)}")
    
    print()

def get_page_comments_example(page_id):
    """Example showing how to get comments from a page"""
    print("\n=== Getting Page Comments ===")
    
    try:
        # Get footer comments for the page
        footer_comments = confluence.get_page_footer_comments(page_id)
        
        print(f"Found {len(footer_comments)} footer comments for page {page_id}:")
        for comment in footer_comments:
            print_comment(comment, indent="  ")
            
        # Get inline comments for the page
        inline_comments = confluence.get_page_inline_comments(page_id)
        
        print(f"Found {len(inline_comments)} inline comments for page {page_id}:")
        for comment in inline_comments:
            print_comment(comment, indent="  ")
            
        return footer_comments
        
    except Exception as e:
        print(f"Error getting page comments: {e}")
        return []

def get_comment_by_id_example(comment_id):
    """Example showing how to get a comment by ID"""
    print(f"\n=== Getting Comment by ID ({comment_id}) ===")
    
    try:
        comment = confluence.get_comment_by_id(comment_id)
        print("Retrieved comment:")
        print_comment(comment)
        return comment
        
    except Exception as e:
        print(f"Error getting comment: {e}")
        return None

def get_comment_children_example(comment_id):
    """Example showing how to get child comments"""
    print(f"\n=== Getting Child Comments for Comment ({comment_id}) ===")
    
    try:
        child_comments = confluence.get_comment_children(comment_id)
        
        print(f"Found {len(child_comments)} child comments:")
        for comment in child_comments:
            print_comment(comment, indent="  ")
            
        return child_comments
        
    except Exception as e:
        print(f"Error getting child comments: {e}")
        return []

def create_page_comment_example(page_id):
    """Example showing how to create comments on a page"""
    print("\n=== Creating Page Comments ===")
    
    created_comments = []
    
    try:
        # Create a footer comment
        footer_comment = confluence.create_page_footer_comment(
            page_id=page_id,
            body="This is a test footer comment created via API v2."
        )
        
        print("Created footer comment:")
        print_comment(footer_comment)
        created_comments.append(footer_comment.get('id'))
        
        # Create a reply to the footer comment
        reply_comment = confluence.create_comment_reply(
            parent_comment_id=footer_comment.get('id'),
            body="This is a reply to the test footer comment."
        )
        
        print("Created reply comment:")
        print_comment(reply_comment)
        created_comments.append(reply_comment.get('id'))
        
        # Create an inline comment (if text selection is known)
        try:
            inline_comment_props = {
                "textSelection": "API example text",
                "textSelectionMatchCount": 1,
                "textSelectionMatchIndex": 0
            }
            
            inline_comment = confluence.create_page_inline_comment(
                page_id=page_id,
                body="This is a test inline comment referring to specific text.",
                inline_comment_properties=inline_comment_props
            )
            
            print("Created inline comment:")
            print_comment(inline_comment)
            created_comments.append(inline_comment.get('id'))
            
        except Exception as e:
            print(f"Note: Could not create inline comment: {e}")
            
        return created_comments
            
    except Exception as e:
        print(f"Error creating comments: {e}")
        return created_comments

def update_comment_example(comment_id):
    """Example showing how to update a comment"""
    print(f"\n=== Updating Comment ({comment_id}) ===")
    
    try:
        # First, get the current comment
        comment = confluence.get_comment_by_id(comment_id)
        print("Original comment:")
        print_comment(comment)
        
        # Update the comment with a new body
        updated_comment = confluence.update_comment(
            comment_id=comment_id,
            body="This comment has been updated via API v2.",
            version=comment.get('version', {}).get('number', 1)
        )
        
        print("Updated comment:")
        print_comment(updated_comment)
        
        # Mark the comment as resolved
        resolved_comment = confluence.update_comment(
            comment_id=comment_id,
            body=updated_comment.get('body', {}).get('storage', {}).get('value', ""),
            version=updated_comment.get('version', {}).get('number', 1),
            resolved=True
        )
        
        print("Comment marked as resolved:")
        print_comment(resolved_comment)
            
    except Exception as e:
        print(f"Error updating comment: {e}")

def delete_comment_example(comment_id):
    """Example showing how to delete a comment"""
    print(f"\n=== Deleting Comment ({comment_id}) ===")
    
    try:
        # Delete the comment
        confluence.delete_comment(comment_id)
        
        print(f"Successfully deleted comment {comment_id}")
            
    except Exception as e:
        print(f"Error deleting comment: {e}")

def get_blogpost_comments_example(blogpost_id):
    """Example showing how to get comments from a blog post"""
    print(f"\n=== Getting Blog Post Comments ({blogpost_id}) ===")
    
    try:
        # Get footer comments for the blog post
        footer_comments = confluence.get_blogpost_footer_comments(blogpost_id)
        
        print(f"Found {len(footer_comments)} footer comments for blog post {blogpost_id}:")
        for comment in footer_comments:
            print_comment(comment, indent="  ")
            
        # Get inline comments for the blog post
        inline_comments = confluence.get_blogpost_inline_comments(blogpost_id)
        
        print(f"Found {len(inline_comments)} inline comments for blog post {blogpost_id}:")
        for comment in inline_comments:
            print_comment(comment, indent="  ")
            
    except Exception as e:
        print(f"Error getting blog post comments: {e}")

def get_attachment_comments_example(attachment_id):
    """Example showing how to get comments from an attachment"""
    print(f"\n=== Getting Attachment Comments ({attachment_id}) ===")
    
    try:
        comments = confluence.get_attachment_comments(attachment_id)
        
        print(f"Found {len(comments)} comments for attachment {attachment_id}:")
        for comment in comments:
            print_comment(comment, indent="  ")
            
    except Exception as e:
        print(f"Error getting attachment comments: {e}")

def get_custom_content_comments_example(custom_content_id):
    """Example showing how to get comments from custom content"""
    print(f"\n=== Getting Custom Content Comments ({custom_content_id}) ===")
    
    try:
        comments = confluence.get_custom_content_comments(custom_content_id)
        
        print(f"Found {len(comments)} comments for custom content {custom_content_id}:")
        for comment in comments:
            print_comment(comment, indent="  ")
            
    except Exception as e:
        print(f"Error getting custom content comments: {e}")

if __name__ == "__main__":
    # You need valid IDs for these examples
    page_id = "123456"           # Replace with a real page ID
    blogpost_id = "654321"       # Replace with a real blog post ID
    attachment_id = "789012"     # Replace with a real attachment ID
    custom_content_id = "345678" # Replace with a real custom content ID
    
    # Get existing comments for the page
    existing_comments = get_page_comments_example(page_id)
    
    # If there are existing comments, show how to get details and replies
    comment_to_check = None
    if existing_comments:
        comment_to_check = existing_comments[0].get('id')
        get_comment_by_id_example(comment_to_check)
        get_comment_children_example(comment_to_check)
    
    # Create new comments
    created_comment_ids = create_page_comment_example(page_id)
    
    # Update one of the created comments
    if created_comment_ids:
        update_comment_example(created_comment_ids[0])
    
    # Clean up by deleting the comments we created
    for comment_id in created_comment_ids:
        delete_comment_example(comment_id)
    
    # Examples for other content types
    # Note: These require valid IDs for those content types
    # get_blogpost_comments_example(blogpost_id)
    # get_attachment_comments_example(attachment_id)
    # get_custom_content_comments_example(custom_content_id) 