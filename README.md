# Youtube_ETL
# How to Create a YouTube Data API Key

This guide explains how to generate an API key for the YouTube Data API v3 using Google Cloud Console.

---

## Prerequisites
- A Google account
- Access to Google Cloud Console: https://console.cloud.google.com

---

## Step 1: Create or Select a Google Cloud Project

1. Go to **Google Cloud Console**.
2. Click on the project dropdown (top left).
3. Click **New Project** (or select an existing one).
4. Enter a project name and click **Create**.

---

## Step 2: Enable YouTube Data API v3

1. In the Cloud Console, navigate to **APIs & Services → Library**.
2. Search for **YouTube Data API v3**.
3. Click it and press **Enable**.

---

## Step 3: Create API Credentials

1. Go to **APIs & Services → Credentials**.
2. Click **Create Credentials → API Key**.
3. Your API key will be generated.

---

## Step 4: Restrict the API Key (Recommended)

1. Click on the created API key.
2. Under **Application restrictions**, choose:
   - HTTP referrers (for web apps), or
   - IP addresses (for server apps).
3. Under **API restrictions**, select:
   - Restrict key
   - Choose **YouTube Data API v3**
4. Save changes.

---
