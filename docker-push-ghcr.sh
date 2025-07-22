#!/bin/bash
# Script to build and push Docker images to GitHub Container Registry

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
GITHUB_USERNAME="zoza1982"
IMAGE_NAME="youtube-downloader"
REGISTRY="ghcr.io"

echo -e "${YELLOW}GitHub Container Registry Push Script${NC}"
echo "======================================="

# Check if token is provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}Error: GITHUB_TOKEN environment variable not set${NC}"
    echo "Please run: export GITHUB_TOKEN=your_personal_access_token"
    exit 1
fi

# Login to GitHub Container Registry
echo -e "\n${YELLOW}1. Logging in to GitHub Container Registry...${NC}"
echo $GITHUB_TOKEN | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully logged in to $REGISTRY${NC}"
else
    echo -e "${RED}✗ Failed to login${NC}"
    exit 1
fi

# Build images
echo -e "\n${YELLOW}2. Building Docker images...${NC}"

# Build standard image
echo -e "${YELLOW}Building standard image...${NC}"
docker build -t $IMAGE_NAME:latest .
echo -e "${GREEN}✓ Standard image built${NC}"

# Build Alpine image
echo -e "${YELLOW}Building Alpine image...${NC}"
docker build -f Dockerfile.alpine -t $IMAGE_NAME:alpine .
echo -e "${GREEN}✓ Alpine image built${NC}"

# Tag images for GitHub Container Registry
echo -e "\n${YELLOW}3. Tagging images for $REGISTRY...${NC}"
docker tag $IMAGE_NAME:latest $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:latest
docker tag $IMAGE_NAME:latest $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:$(cat VERSION)
docker tag $IMAGE_NAME:alpine $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:alpine
docker tag $IMAGE_NAME:alpine $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:$(cat VERSION)-alpine
echo -e "${GREEN}✓ Images tagged${NC}"

# Push images
echo -e "\n${YELLOW}4. Pushing images to $REGISTRY...${NC}"

echo -e "${YELLOW}Pushing latest...${NC}"
docker push $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:latest

echo -e "${YELLOW}Pushing version $(cat VERSION)...${NC}"
docker push $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:$(cat VERSION)

echo -e "${YELLOW}Pushing alpine...${NC}"
docker push $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:alpine

echo -e "${YELLOW}Pushing alpine version $(cat VERSION)...${NC}"
docker push $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:$(cat VERSION)-alpine

echo -e "\n${GREEN}✅ All images successfully pushed!${NC}"
echo -e "\nYour images are now available at:"
echo -e "  ${GREEN}$REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:latest${NC}"
echo -e "  ${GREEN}$REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:$(cat VERSION)${NC}"
echo -e "  ${GREEN}$REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:alpine${NC}"
echo -e "  ${GREEN}$REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:$(cat VERSION)-alpine${NC}"

echo -e "\nTo pull and use:"
echo -e "  docker pull $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:latest"
echo -e "  docker run -v \$(pwd)/downloads:/downloads $REGISTRY/$GITHUB_USERNAME/$IMAGE_NAME:latest URL"

# Logout
echo -e "\n${YELLOW}5. Logging out...${NC}"
docker logout $REGISTRY
echo -e "${GREEN}✓ Logged out${NC}"