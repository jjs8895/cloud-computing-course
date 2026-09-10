# HW1 Cloud Deployment Guide

## Platform
Google Cloud Platform (GCP)

## Account Setup
- Account created: 09/10/26
- Project ID: cmpe789-hw1

## Instance Details
- Instance name: cmpe789-hw1-flask
- Zone: us-central1-a
- Machine type: e2-micro
- OS: Ubuntu 22.04 LTS

## Application Details
- Framework: Flask 3.0.0
- Language: Python 3
- Port: 5000

## Deployment Steps Performed
1. Created GCP account and project
2. Installed and configured gcloud CLI
3. Provisioned Compute Engine instance
4. Opened port 5000 via firewall rules
5. Copied local application assets to VM target
6. Deployed application background process via nohup

## Testing Results
- Health endpoint: ✅ Working
- POST message: ✅ Working
- GET messages: ✅ Working

## Cost Analysis
- VM instance: ~$6-8/month (e2-micro)
- Storage: ~$0.50/month (10GB boot disk)
- **Total estimated cost: ~$7-9/month**

## Troubleshooting
Always check you gcloud project list and insure that you configure your gcloud project to have the exact same ID as the projectID in the gcloud project list. If you run into permissions issue your project configuration is incorrect.
