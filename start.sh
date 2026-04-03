#!/bin/bash
# ══════════════════════════════════════════════
#  CareerForge — Career Intelligence Platform
#  Quick Start Script
# ══════════════════════════════════════════════

set -e
CYAN='\033[0;36m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'; NC='\033[0m'

echo -e "${CYAN}╔═══════════════════════════════════╗${NC}"
echo -e "${CYAN}║  CareerForge — Career Intelligence ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════╝${NC}"
echo ""

# Step 1: Install deps
echo -e "${YELLOW}[1/3] Installing dependencies...${NC}"
pip install -r requirements.txt -q

# Step 2: Generate data
echo -e "${YELLOW}[2/3] Generating question bank & learning content...${NC}"
python3 generate_data.py

# Step 3: Start server
echo -e "${YELLOW}[3/3] Starting CareerForge server...${NC}"
echo ""
echo -e "${GREEN}  → Open http://localhost:8000 in your browser${NC}"
echo -e "${GREEN}  → Press Ctrl+C to stop${NC}"
echo ""

uvicorn main:app --reload --port 8000 --host 127.0.0.1
