#!/bin/bash
# =============================================================================
# DataScout — S3 Bucket Creation Script
# =============================================================================
# Creates and configures the S3 storage bucket with encryption, versioning,
# public access blocking, and lifecycle policies.
# =============================================================================
set -euo pipefail

BUCKET_NAME="${1:-datascout-storage}"
REGION="${2:-us-east-1}"

echo "═══════════════════════════════════════════════════════"
echo " DataScout — S3 Bucket Setup"
echo " Bucket: ${BUCKET_NAME}"
echo " Region: ${REGION}"
echo "═══════════════════════════════════════════════════════"

# Create bucket
echo "→ Creating S3 bucket..."
aws s3 mb "s3://${BUCKET_NAME}" --region "${REGION}" 2>/dev/null || echo "  Bucket already exists."

# Enable versioning
echo "→ Enabling versioning..."
aws s3api put-bucket-versioning \
    --bucket "${BUCKET_NAME}" \
    --versioning-configuration Status=Enabled

# Enable encryption
echo "→ Enabling server-side encryption..."
aws s3api put-bucket-encryption \
    --bucket "${BUCKET_NAME}" \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            },
            "BucketKeyEnabled": true
        }]
    }'

# Block public access
echo "→ Blocking public access..."
aws s3api put-public-access-block \
    --bucket "${BUCKET_NAME}" \
    --public-access-block-configuration \
        BlockPublicAcls=true,IgnorePublicAcls=true,\
BlockPublicPolicy=true,RestrictPublicBuckets=true

# Set lifecycle rules
echo "→ Setting lifecycle rules..."
aws s3api put-bucket-lifecycle-configuration \
    --bucket "${BUCKET_NAME}" \
    --lifecycle-configuration '{
        "Rules": [
            {
                "ID": "DeleteSessionData",
                "Filter": {"Prefix": "datasets/"},
                "Status": "Enabled",
                "Expiration": {"Days": 7}
            },
            {
                "ID": "DeleteArtifacts",
                "Filter": {"Prefix": "artifacts/"},
                "Status": "Enabled",
                "Expiration": {"Days": 7}
            },
            {
                "ID": "ArchiveLogs",
                "Filter": {"Prefix": "logs/"},
                "Status": "Enabled",
                "Transitions": [{"Days": 7, "StorageClass": "GLACIER"}],
                "Expiration": {"Days": 90}
            }
        ]
    }'

echo ""
echo "✅ S3 bucket '${BUCKET_NAME}' setup complete!"
