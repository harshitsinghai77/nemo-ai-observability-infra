# NemoAI Transaction Search Stack

AWS CDK infrastructure for X-Ray transaction search with automated deployment.

## Structure

```
├── .github/workflows/deploy.yml    # GitHub Actions CI/CD
├── infrastructure/                 # CDK stack
├── cdk_app.py                     # CDK entry point
└── requirements.txt               # Dependencies
```

## What it does

- Enables X-Ray transaction search (100% indexing)
- Sets up CloudWatch Logs permissions for X-Ray
- Auto-deploys on push to main branch

## Setup

```bash
pip install -r requirements.txt
npm install -g aws-cdk
cdk deploy
```

## GitHub Actions

Requires secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_ACCOUNT`

Deploys to us-east-1 on main branch pushes.