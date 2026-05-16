#!/usr/bin/env python3
"""
Script to create a Jira issue using the Atlassian MCP server
"""
import json
import requests
import os

# The issue details
issue_data = {
    "project": "FRA",
    "issuetype": "Bug",
    "summary": "iOS missing per_page parameter in feature-flags API call",
    "priority": "Low",
    "components": ["iOS"],
    "versions": ["6.2.1"],  # Affects Versions
    "fixVersions": ["Vigo shutdown #1"],
    "labels": ["iOS"],
    "description": """Key details
• App: 6.2.1 (Build 1137)
• Device/OS: iPhone 13 Pro - iOS 26
• Environment: Preprod

Steps to reproduce
1. Fresh install of the app
2. Login and open the app
3. Observe network traffic
4. Check the feature flags call

Actual Result
iOS app makes feature-flags API call without the per_page=1000 parameter, which may result in paginated responses with default limit, potentially missing feature flags or requiring multiple API calls to retrieve all flags.

Expected Result
iOS app should include the per_page=1000 parameter in the feature-flags API call, matching Android's implementation, ensuring all feature flags are retrieved in a single request.

Notes
• Priority: Low
• Component: iOS
• Affects Versions: 6.2.1
• Fix Versions: Vigo shutdown #1
• Reproducibility: High"""
}

print(json.dumps(issue_data, indent=2))
