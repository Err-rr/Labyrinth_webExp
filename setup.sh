#!/bin/bash

# Labyrinth CTF - Setup Script
# This script automates the deployment process

set -e

echo "=========================================="
echo "  Labyrinth: Endless Mirage - Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}[*] Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}[✓] Python 3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}[✗] Python 3 not found. Please install Python 3.7+${NC}"
    exit 1
fi

# Create virtual environment
echo -e "\n${YELLOW}[*] Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}[✓] Virtual environment created${NC}"
else
    echo -e "${GREEN}[✓] Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}[*] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}[✓] Virtual environment activated${NC}"

# Install dependencies
echo -e "\n${YELLOW}[*] Installing dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}[✓] Dependencies installed${NC}"

# Create necessary directories
echo -e "\n${YELLOW}[*] Creating directories...${NC}"
mkdir -p templates uploads
echo -e "${GREEN}[✓] Directories created${NC}"

# Check if database exists
if [ -f "labyrinth.db" ]; then
    echo -e "\n${YELLOW}[*] Existing database found${NC}"
    read -p "Do you want to reset the database? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm labyrinth.db
        echo -e "${GREEN}[✓] Database reset${NC}"
    fi
fi

# Test configuration
echo -e "\n${YELLOW}[*] Testing configuration...${NC}"
if [ -f "config.py" ] && [ -f "config.py.bak" ]; then
    echo -e "${GREEN}[✓] Configuration files found${NC}"
else
    echo -e "${RED}[✗] Configuration files missing${NC}"
    exit 1
fi

# Display setup summary
echo -e "\n=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "To start the CTF challenge:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the application: python app.py"
echo "  3. Access at: http://localhost:5000"
echo ""
echo "To test the exploit:"
echo "  python exploit.py --quick"
echo ""
echo "Flag: EHAX{l4bYr1n7_byp4ss_1s_th3_k3y}"
echo ""
echo "=========================================="
echo ""

# Ask if user wants to start the server
read -p "Do you want to start the server now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}[*] Starting Flask server...${NC}"
    echo -e "${YELLOW}[i] Press Ctrl+C to stop the server${NC}"
    echo ""
    python app.py
fi