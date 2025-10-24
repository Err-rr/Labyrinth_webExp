================================================================================
                    LABYRINTH: ENDLESS LOOP
                    Web Exploitation CTF Challenge
================================================================================

DIFFICULTY: Medium to Hard
CATEGORY: Web Exploitation
ESTIMATED TIME: 30 minutes

================================================================================
DESCRIPTION
================================================================================

Navigate an impossible maze game that's unsolvable by design. Players must 
discover and chain multiple web vulnerabilities to bypass the maze and capture
the flag. The challenge features a modern, professional interface with a 
playable HTML5 canvas maze that serves as misdirection.

================================================================================
INSTALLATION
================================================================================

1. PREREQUISITES
   - Python
   - pip (Python package manager)
   - Git (optional)

2. SETUP STEPS

   # Clone or download the challenge files
   cd labyrinth-ctf

   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run the application
   python app.py

3. ACCESS
   - Open browser to: http://localhost:5000
   - Challenge will be available on port 5000
   - Database auto-initializes on first run

================================================================================
EXPLOITATION PATH OVERVIEW
================================================================================

This challenge requires chaining multiple vulnerabilities. Players must:

TOTAL STEPS: 7

Step 1: RECONNAISSANCE
   - Explore the application
   - Check common files (robots.txt, comments, JavaScript)
   - Identify hidden endpoints

Step 2: INFORMATION GATHERING
   - Enumerate users and roles
   - Discover database structure
   - Find exposed backup files

Step 3: VULNERABILITY DISCOVERY
   - Test for SQL injection
   - Check for insecure direct object references
   - Identify authentication weaknesses

Step 4: SECRET KEY EXTRACTION
   - Locate configuration leaks
   - Extract JWT signing key
   - Analyze token structure

Step 5: TOKEN FORGERY
   - Understand JWT claims required
   - Generate forged authentication token
   - Validate token structure

Step 6: PRIVILEGE ESCALATION
   - Access admin-only endpoints
   - Bypass authorization checks
   - Navigate admin panel

Step 7: FLAG CAPTURE
   - Use forged credentials
   - Access protected resources
   - Retrieve final flag

================================================================================
VULNERABILITIES INCLUDED
================================================================================

1. SQL Injection (Error-based & UNION-based)
2. Information Disclosure (Backup file exposure)
3. Insecure Direct Object Reference (IDOR)
4. Broken Authentication (JWT forgery)
5. Missing Authorization Controls
6. Path Traversal (LFI)
7. Insecure File Upload
8. WebSocket Token Echo

================================================================================
LEARNING OBJECTIVES
================================================================================

- Reconnaissance and enumeration techniques
- SQL injection exploitation
- JWT security and token forgery
- Authorization bypass methods
- Vulnerability chaining
- Web application security testing

================================================================================
TESTING
================================================================================

# Automated exploit script included for testing:
python exploit.py --quick

# Run specific exploitation steps:
python exploit.py --step 1
python exploit.py --step 2
# ... up to step 7

# Interactive mode (with pauses):
python exploit.py

================================================================================
ENDPOINTS
================================================================================

Public Endpoints:
- / (Home page with maze game)
- /play (Canvas maze interface)
- /search (User search)
- /upload (File upload)
- /profile/<id> (User profiles)
- /hint (Progressive hint system)

Hidden Endpoints:
- /robots.txt (Reveals disallowed paths)
- /backup (Configuration backup)
- /secret/portal (Hidden guide)
- /debug (Debug information)
- /admin (Admin panel - requires JWT)
- /flag (Final flag endpoint)

API Endpoints:
- /api/move (Maze move validation)
- /api/vault (Admin vault access)
- /ws (WebSocket echo)

================================================================================
HINTS SYSTEM
================================================================================

Progressive hints available at:
- /hint?level=1 (Basic reconnaissance)
- /hint?level=2 (Intermediate discovery)
- /hint?level=3 (Advanced exploitation)

Secret portal with full guide:
- /secret/portal (Must discover URL)

================================================================================
SECURITY NOTES
================================================================================

⚠️ WARNING: This application contains INTENTIONAL security vulnerabilities
for educational purposes only.

DO NOT:
- Deploy on public networks
- Use in production environments
- Expose to untrusted users

DO:
- Use only in controlled CTF environments
- Run in isolated networks
- Reset database between events

================================================================================
TROUBLESHOOTING
================================================================================

Issue: Port 5000 already in use
Solution: Change port in app.py or kill existing process

Issue: Database errors
Solution: Delete labyrinth.db and restart app.py

Issue: Module not found
Solution: Ensure virtual environment is activated

Issue: Permission denied
Solution: chmod +x setup.sh exploit.py

================================================================================
FILES STRUCTURE
================================================================================

labyrinth-ctf/
├── app.py                  # Main Flask application
├── config.py               # Configuration file
├── config.py.bak          # Backup config (intentional leak)
├── requirements.txt        # Python dependencies
├── exploit.py             # Automated exploitation script
├── setup.sh               # Setup script
├── README.md              # Full documentation
├── WALKTHROUGH.md         # Solution guide
└── templates/             # HTML templates
    ├── index.html
    ├── play.html
    ├── search.html
    ├── upload.html
    ├── profile.html
    ├── admin_login.html
    ├── admin_panel.html
    └── portal.html

================================================================================
SUPPORT
================================================================================

For technical issues or questions:
- Check WALKTHROUGH.md for detailed solution
- Review README.md for complete documentation
- Use /hint endpoints in the application
- Check Flask debug output for errors

================================================================================
CREDITS
================================================================================

Challenge Type: Web Exploitation
Difficulty: Hard
Category: CTF Challenge
Technologies: Flask, Python, SQLite, HTML5 Canvas, Bootstrap, JWT

================================================================================
LICENSE
================================================================================

Educational use only. Do not deploy in production environments.

================================================================================
