import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "client_store.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_code_lab_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create code_challenges table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS code_challenges (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        topic TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        description TEXT NOT NULL,
        starter_code TEXT NOT NULL,
        test_cases TEXT NOT NULL
    )
    ''')
    
    # Create code_submissions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS code_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenge_id TEXT NOT NULL,
        code TEXT NOT NULL,
        status TEXT NOT NULL,
        ai_review TEXT,
        score INTEGER,
        submitted_at TEXT NOT NULL,
        FOREIGN KEY (challenge_id) REFERENCES code_challenges(id) ON DELETE CASCADE
    )
    ''')
    
    # Migration: Add mode column if not exists
    cursor.execute("PRAGMA table_info(code_submissions)")
    columns = [col[1] for col in cursor.fetchall()]
    if columns and "mode" not in columns:
        cursor.execute("ALTER TABLE code_submissions ADD COLUMN mode TEXT DEFAULT 'practice';")
        
    conn.commit()
    
    # Seed default challenges if empty or if new sum-two-numbers challenge is missing
    cursor.execute("SELECT COUNT(*) FROM code_challenges WHERE id = 'sum-two-numbers'")
    if cursor.fetchone()[0] == 0:
        # Delete old seeded challenges to refresh them
        cursor.execute("DELETE FROM code_challenges")
        
        default_challenges = [
            (
                "sum-two-numbers",
                "Sum of Two Numbers",
                "Basic Operations",
                "Easy",
                "Write a function <code>add(a, b)</code> that returns the sum of two numbers <code>a</code> and <code>b</code>.<br/><br/>This is a starter challenge to test the coding workspace run/submit behavior.<br/><br/><b>Example 1:</b><br/>Input: a = 2, b = 3<br/>Output: 5",
                "def add(a, b):\n    # Write your code here\n    # Example solution:\n    # return a + b\n    pass\n",
                json.dumps([
                    {"input": [2, 3], "output": 5},
                    {"input": [-1, 5], "output": 4},
                    {"input": [0, 0], "output": 0}
                ])
            ),
            (
                "two-sum",
                "Two Sum",
                "Array & Hash Table",
                "Easy",
                "Given an array of integers <code>nums</code> and an integer <code>target</code>, return indices of the two numbers such that they add up to <code>target</code>.<br/><br/>You may assume that each input would have exactly one solution, and you may not use the same element twice.<br/><br/><b>Example 1:</b><br/>Input: nums = [2,7,11,15], target = 9<br/>Output: [0,1]<br/>Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].",
                "def two_sum(nums, target):\n    # Write your code here\n    #\n    # Hint (Uncomment to solve):\n    # seen = {}\n    # for idx, num in enumerate(nums):\n    #     diff = target - num\n    #     if diff in seen:\n    #         return [seen[diff], idx]\n    #     seen[num] = idx\n    pass\n",
                json.dumps([
                    {"input": [[2, 7, 11, 15], 9], "output": [0, 1]},
                    {"input": [[3, 2, 4], 6], "output": [1, 2]},
                    {"input": [[3, 3], 6], "output": [0, 1]}
                ])
            ),
            (
                "reverse-string",
                "Reverse a String",
                "String & Two Pointers",
                "Easy",
                "Write a function that reverses a string. The input string is given as an array of characters <code>s</code>.<br/><br/>You must do this by modifying the input array in-place with O(1) extra memory. The function should return the modified array.<br/><br/><b>Example 1:</b><br/>Input: s = ['h','e','l','l','o']<br/>Output: ['o','l','l','e','h']",
                "def reverse_string(s):\n    # Write your code here\n    # Modify s in-place (return s when completed)\n    #\n    # Hint (Uncomment to solve):\n    # s.reverse()\n    # return s\n    pass\n",
                json.dumps([
                    {"input": [["h","e","l","l","o"]], "output": ["o","l","l","e","h"]},
                    {"input": [["H","a","n","n","a","h"]], "output": ["h","a","n","n","a","H"]}
                ])
            ),
            (
                "palindrome-number",
                "Palindrome Number",
                "Math",
                "Easy",
                "Given an integer <code>x</code>, return <code>True</code> if <code>x</code> is a palindrome, and <code>False</code> otherwise.<br/><br/><b>Example 1:</b><br/>Input: x = 121<br/>Output: true<br/><br/><b>Example 2:</b><br/>Input: x = -121<br/>Output: false<br/>Explanation: From left to right, it reads -121. From right to left, it becomes 121-.",
                "def is_palindrome(x):\n    # Write your code here\n    #\n    # Hint (Uncomment to solve):\n    # return str(x) == str(x)[::-1]\n    pass\n",
                json.dumps([
                    {"input": [121], "output": True},
                    {"input": [-121], "output": False},
                    {"input": [10], "output": False}
                ])
            ),
            (
                "valid-parentheses",
                "Valid Parentheses",
                "Stack",
                "Easy",
                "Given a string <code>s</code> containing just the characters <code>'('</code>, <code>')'</code>, <code>'{'</code>, <code>'}'</code>, <code>'['</code> and <code>']'</code>, determine if the input string is valid.<br/><br/>An input string is valid if:<br/>1. Open brackets must be closed by the same type of brackets.<br/>2. Open brackets must be closed in the correct order.<br/><br/><b>Example 1:</b><br/>Input: s = '()[]{}'<br/>Output: true<br/><br/><b>Example 2:</b><br/>Input: s = '(]'<br/>Output: false",
                "def is_valid_parentheses(s):\n    # Write your code here\n    #\n    # Hint (Uncomment to solve):\n    # stack = []\n    # mapping = {\")\": \"(\", \"}\": \"{\", \"]\": \"[\"}\n    # for char in s:\n    #     if char in mapping:\n    #         top_element = stack.pop() if stack else '#'\n    #         if mapping[char] != top_element:\n    #             return False\n    #     else:\n    #         stack.append(char)\n    # return not stack\n    pass\n",
                json.dumps([
                    {"input": ["()"], "output": True},
                    {"input": ["()[]{}"], "output": True},
                    {"input": ["(]"], "output": False},
                    {"input": ["([)]"], "output": False}
                ])
            )
        ]
        
        for cid, title, topic, diff, desc, code, tests in default_challenges:
            cursor.execute(
                "INSERT INTO code_challenges (id, title, topic, difficulty, description, starter_code, test_cases) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (cid, title, topic, diff, desc, code, tests)
            )
        conn.commit()
        
    conn.close()

# CRUD operations
def get_all_challenges():
    init_code_lab_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM code_challenges")
    challenges = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return challenges

def get_challenge_by_id(challenge_id):
    init_code_lab_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM code_challenges WHERE id = ?", (challenge_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_submission(challenge_id, code, status, ai_review=None, score=None, mode='practice'):
    conn = get_connection()
    cursor = conn.cursor()
    submitted_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO code_submissions (challenge_id, code, status, ai_review, score, submitted_at, mode) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (challenge_id, code, status, ai_review, score, submitted_at, mode)
    )
    conn.commit()
    conn.close()

def get_last_submission(challenge_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM code_submissions WHERE challenge_id = ? ORDER BY id DESC LIMIT 1",
        (challenge_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_challenge_submissions(challenge_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM code_submissions WHERE challenge_id = ? ORDER BY id DESC",
        (challenge_id,)
    )
    submissions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return submissions

def get_challenge_statistics():
    init_code_lab_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM code_challenges")
    total_challenges = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT challenge_id) FROM code_submissions WHERE status = 'Solved'")
    solved_challenges = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total": total_challenges,
        "solved": solved_challenges
    }

def get_exam_statistics():
    init_code_lab_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(DISTINCT challenge_id) FROM code_submissions WHERE status = 'Solved' AND mode = 'exam'")
    solved_count = cursor.fetchone()[0] or 0
    
    # Calculate sum of maximum score for each challenge solved in Exam Mode
    cursor.execute("""
        SELECT SUM(max_score) FROM (
            SELECT MAX(score) as max_score 
            FROM code_submissions 
            WHERE status = 'Solved' AND mode = 'exam' 
            GROUP BY challenge_id
        )
    """)
    total_score = cursor.fetchone()[0] or 0
    
    conn.close()
    return {
        "solved": solved_count,
        "score": total_score
    }

def add_custom_challenge(challenge_id, title, topic, difficulty, description, starter_code, test_cases):
    init_code_lab_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO code_challenges (id, title, topic, difficulty, description, starter_code, test_cases) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (challenge_id, title, topic, difficulty, description, starter_code, test_cases)
    )
    conn.commit()
    conn.close()
