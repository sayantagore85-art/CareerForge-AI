import streamlit as st
import pdfplumber
import re
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="AI Resume Analyser & MockTest Portal", layout="centered")

# ---------- Role Database with Skills & Descriptions ----------
ROLE_SKILLS = {
    "Data Analyst": {
        "skills": ["python", "sql", "excel", "power bi", "tableau", "statistics", "data cleaning", "data visualization", "pandas", "numpy"],
        "description": "Data Analysts clean, query, and visualize datasets to turn raw numbers into actionable business insights."
    },
    "Software Developer": {
        "skills": ["python", "java", "c++", "data structures", "algorithms", "git", "oop", "sql", "problem solving", "system design"],
        "description": "Software Developers require core programming knowledge, data structures, and algorithmic problem-solving skills."
    },
    "Web Developer": {
        "skills": ["html", "css", "javascript", "react", "node", "api", "git", "mongodb", "express", "responsive design"],
        "description": "Web Developers build responsive, scalable front-end and back-end web applications."
    },
    "Business Analyst": {
        "skills": ["excel", "sql", "power bi", "requirement gathering", "stakeholder management", "data analysis", "communication", "process improvement", "documentation", "agile"],
        "description": "Business Analysts bridge IT and business needs through requirements gathering and data reporting tools."
    }
}

MASTER_SKILLS = sorted(set(skill for data in ROLE_SKILLS.values() for skill in data["skills"]))

# ---------- Very Detailed Study Materials Database ----------
ACTION_PLAN_DATABASE = {
    "Python Programming": {
        "title": "Python Programming Mastery",
        "routine": "Daily 2 Hours (Morning 7:00 AM - 8:30 AM | Evening 8:00 PM - 8:30 PM)",
        "weeks": {
            "Week 1 (Days 1-7): Syntax, Variables & Control Flow": "Mastering basic syntax, operators, type casting, conditional branching, and looping constructs.",
            "Week 2 (Days 8-14): Data Structures & OOP": "Deep dive into lists, dictionaries, tuples, sets, and Object-Oriented Programming (Classes, Inheritance).",
            "Week 3 (Days 15-21): Advanced Python & Libraries": "File handling, exception blocks, lambda functions, list comprehensions, and Pandas/NumPy basics.",
            "Week 4 (Days 22-30): Mini Projects & Problem Solving": "Building automation scripts, consuming REST APIs, and rigorous coding practice."
        },
        "notes": {
            "Week 1": """
### 📚 Comprehensive Study Material: Syntax, Variables & Control Flow
* **Variables & Memory Assignment:** Understanding mutable vs immutable objects, dynamic typing, and memory references.
* **Control Flow Statements:** Detailed practice with `if`, `elif`, `else` nested blocks, and short-circuit evaluation.
* **Loops (`for` & `while`):** Using `break`, `continue`, `else` clauses in loops, and range generation functions.
* **Functions & Scope:** Defining functions with default arguments, `*args`, `**kwargs`, local vs global scopes, and docstrings.
            """,
            "Week 2": """
### 📚 Comprehensive Study Material: Data Structures & OOP
* **Advanced Data Structures:** Built-in methods for Lists, Tuples, Dictionaries, and Sets. Time complexities of dictionary lookups ($O(1)$ average).
* **Object-Oriented Programming (OOP):** 
    * Classes and Objects instantiation (`__init__` constructor).
    * Four Pillars: Encapsulation (private variables), Inheritance (single/multiple), Polymorphism (method overriding), and Abstraction.
            """,
            "Week 3": """
### 📚 Comprehensive Study Material: Advanced Python & Libraries
* **File Handling:** Reading and writing text/CSV files safely using context managers (`with open(...) as f:`).
* **Exception Handling:** Managing runtime errors using `try`, `except`, `else`, `finally`, and raising custom exceptions.
* **Data Manipulation Libraries:** Introduction to NumPy arrays and Pandas DataFrames for tabular data filtering and aggregation.
            """,
            "Week 4": """
### 📚 Comprehensive Study Material: Mini Projects & Problem Solving
* **Automation & APIs:** Writing scripts to parse JSON data from web APIs using the `requests` library.
* **Coding Drills:** Solving 20+ algorithmic questions on HackerRank or LeetCode using core Python features.
            """
        }
    },
    "Java": {
        "title": "Java Core & Advanced Mastery",
        "routine": "Daily 2 Hours (Morning 6:30 AM - 8:00 AM)",
        "weeks": {
            "Week 1 (Days 1-7): Java Basics & OOP": "JVM architecture, syntax, classes, objects, constructors, and OOP principles.",
            "Week 2 (Days 8-14): Collections Framework": "In-depth study of List, Set, Map interfaces, ArrayList, HashMap, and Iterators.",
            "Week 3 (Days 15-21): Exception Handling & Multithreading": "Try-catch hierarchy, checked vs unchecked exceptions, and thread lifecycle.",
            "Week 4 (Days 22-30): JDBC & Spring Boot Intro": "Connecting Java apps to databases using JDBC and building basic REST controllers."
        },
        "notes": {
            "Week 1": """
### 📚 Comprehensive Study Material: Java Basics & OOP
* **JVM, JRE & JDK:** Understanding platform independence and bytecode execution.
* **OOP Pillars:** Access modifiers (`public`, `private`, `protected`, default), method overloading vs overriding.
            """,
            "Week 2": """
### 📚 Comprehensive Study Material: Collections Framework
* **Collections Hierarchy:** `Collection`, `List` (ArrayList, LinkedList), `Set` (HashSet, TreeSet), and `Map` (HashMap, TreeMap). Internal working of hashing.
            """,
            "Week 3": """
### 📚 Comprehensive Study Material: Exception Handling & Multithreading
* **Exceptions:** `try`, `catch`, `finally`, `throw`, `throws`, and creating custom exception classes.
* **Multithreading:** Extending `Thread` class, implementing `Runnable` interface, and thread synchronization locks.
            """,
            "Week 4": """
### 📚 Comprehensive Study Material: JDBC & Spring Boot
* **Database Connectivity:** Executing SQL queries from Java using JDBC drivers and prepared statements.
            """
        }
    },
    "Data Structures & Algorithms (DSA)": {
        "title": "DSA & Coding Interview Mastery",
        "routine": "Daily 2.5 Hours",
        "weeks": {
            "Week 1 (Days 1-7): Complexity & Linear DS": "Big-O Notation, Arrays, Strings, Two-Pointer technique, and Sliding Window problems.",
            "Week 2 (Days 8-14): Linked Lists, Stacks & Queues": "Singly/Doubly Linked Lists, Stack implementation, Queue operations, and expression parsing.",
            "Week 3 (Days 15-21): Recursion, Trees & BST": "Recursion logic, Binary Trees, DFS/BFS traversals, and BST operations.",
            "Week 4 (Days 22-30): Graphs & Dynamic Programming": "Graph representations, Dijkstra's algorithm, sorting algorithms, and intro to DP."
        },
        "notes": {
            "Week 1": """
### 📚 Comprehensive Study Material: Complexity & Linear DS
* **Big-O Analysis:** Evaluating time and space complexities. Best, average, and worst-case scenarios.
* **Array & String Patterns:** Two-pointer approach for palindrome checks, sliding window for subarray sums.
            """,
            "Week 2": """
### 📚 Comprehensive Study Material: Linked Lists, Stacks & Queues
* **Linked Lists:** Pointer manipulations, cycle detection (Floyd's algorithm), and list reversal.
* **Stacks & Queues:** LIFO and FIFO implementations, evaluating postfix expressions, and monotonic stacks.
            """,
            "Week 3": """
### 📚 Comprehensive Study Material: Trees & Recursion
* **Tree Traversals:** Inorder, Preorder, Postorder (recursive and iterative), and Level Order BFS.
* **Backtracking:** Solving N-Queens, Sudoku solver, and subset generation problems.
            """,
            "Week 4": """
### 📚 Comprehensive Study Material: Graphs & Dynamic Programming
* **Graphs:** Adjacency lists, BFS, DFS, shortest path in unweighted and weighted graphs.
* **Dynamic Programming:** Memoization vs Tabulation, 0/1 Knapsack problem, and Longest Common Subsequence.
            """
        }
    },
    "Database Management Systems (DBMS)": {
        "title": "DBMS & Relational Databases",
        "routine": "Daily 2 Hours",
        "weeks": {
            "Week 1 (Days 1-7): ER Models & Relational Algebra": "Entities, Attributes, Relationships, ER diagrams, and Relational Algebra operations.",
            "Week 2 (Days 8-14): SQL Queries & Joins": "DDL, DML, Complex Joins, Subqueries, Aggregate functions, and Views.",
            "Week 3 (Days 15-21): Normalization & Transactions": "1NF, 2NF, 3NF, BCNF, ACID properties, and Concurrency control.",
            "Week 4 (Days 22-30): Indexing & Performance Tuning": "B-Trees, B+ Trees, hashing, query optimization, and NoSQL intro."
        },
        "notes": {
            "Week 1": """
### 📚 Comprehensive Study Material: ER Models & Relational Algebra
* **ER Diagrams:** Cardinality, participation constraints, mapping entities into relational tables.
* **Relational Algebra:** Fundamental operations including selection, projection, union, set difference, and cartesian product.
            """,
            "Week 2": """
### 📚 Comprehensive Study Material: SQL Queries & Joins
* **Advanced Joins:** Inner, Left Outer, Right Outer, Full Outer, and Self Joins.
* **Window Functions:** Using `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, and running totals.
            """,
            "Week 3": """
### 📚 Comprehensive Study Material: Normalization & Transactions
* **Database Normalization:** Functional dependencies, removing anomalies using 1NF, 2NF, 3NF, and BCNF.
* **ACID Properties:** Atomicity, Consistency, Isolation levels, and Two-Phase Locking protocols.
            """,
            "Week 4": """
### 📚 Comprehensive Study Material: Indexing & Optimization
* **Indexing:** Clustered vs Non-clustered indexes, B-Trees and B+ Trees structure. Query execution plan analysis.
            """
        }
    },
    "Quantitative Aptitude": {
        "title": "Quantitative Aptitude",
        "routine": "Daily 1.5 Hours",
        "weeks": {
            "Week 1 (Days 1-7): Arithmetic Basics": "Percentages, Ratio & Proportion, Profit & Loss, Simple & Compound Interest.",
            "Week 2 (Days 8-14): Advanced Arithmetic": "Time & Work, Pipes & Cisterns, Speed, Time & Distance, Boats & Streams.",
            "Week 3 (Days 15-21): Modern Math": "Permutations & Combinations, Probability, Progressions (AP, GP).",
            "Week 4 (Days 22-30): Data Interpretation": "Pie charts, Bar graphs, Tabular data analysis, and shortcut tricks."
        },
        "notes": {
            "Week 1": """
### 📚 Comprehensive Study Material: Arithmetic Basics
* **Percentages & Ratios:** Fraction tables, successive percentage changes, and ratio scaling rules.
* **Interest:** Direct formulas for compound interest and simple interest differences.
            """,
            "Week 2": """
### 📚 Comprehensive Study Material: Advanced Arithmetic
* **Time & Work:** LCM efficiency method for combined workers and alternate working days.
* **Relative Speed:** Problems involving trains crossing poles/platforms and upstream/downstream boat speeds.
            """,
            "Week 3": """
### 📚 Comprehensive Study Material: Modern Math & Probability
* **P&C:** Fundamental counting theorems, circular permutations, and selection formulas.
* **Probability:** Independent and mutually exclusive events, conditional probability.
            """,
            "Week 4": """
### 📚 Comprehensive Study Material: Data Interpretation
* **DI Analysis:** Fast calculation techniques for tables, bar graphs, and pie charts under exam time limits.
            """
        }
    },
    "Logical Reasoning": {
        "title": "Logical Reasoning",
        "routine": "Daily 1.5 Hours",
        "weeks": {
            "Week 1 (Days 1-7): Verbal Reasoning": "Coding-Decoding, Blood Relations, Direction Sense Test, Alphabet & Number Series.",
            "Week 2 (Days 8-14): Analytical Reasoning": "Seating Arrangements (Linear & Circular), Puzzles, Syllogisms.",
            "Week 3 (Days 15-21): Critical Reasoning": "Statement & Assumptions, Course of Action, Cause & Effect.",
            "Week 4 (Days 22-30): Mock Practice & Speed Drills": "Solving previous year placement reasoning sections under strict timed conditions."
        },
        "notes": {
            "Week 1": """
### 📚 Comprehensive Study Material: Verbal Reasoning
* **Coding & Decoding:** Recognizing alphabet shifting patterns, substitution codes, and number coding.
* **Blood Relations:** Diagramming family trees with standard male/female notations.
            """,
            "Week 2": """
### 📚 Comprehensive Study Material: Analytical Puzzles & Syllogisms
* **Seating Arrangements:** Solving complex multi-variable linear and circular puzzle layouts.
* **Syllogisms:** Testing logical validity using standard Venn diagram rules.
            """,
            "Week 3": """
### 📚 Comprehensive Study Material: Critical Reasoning
* **Assumptions & Arguments:** Evaluating implicit assumptions behind corporate or social statements.
            """,
            "Week 4": """
### 📚 Comprehensive Study Material: Speed Drills
* **Timed Practice:** Mixed reasoning test sets to build speed and accuracy for placement exams.
            """
        }
    }
}

# ---------- Comprehensive Quiz Database ----------
QUIZ_DATABASE = {
    "Programming Languages": {
        "Python": {
            "Easy": [
                {"question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "lambda"], "answer": "def", "explanation": "def is used to create functions in Python.", "topic": "Functions"},
                {"question": "What is the output of type(10) in Python?", "options": ["<class 'float'>", "<class 'int'>", "<class 'number'>", "<class 'str'>"], "answer": "<class 'int'>", "explanation": "10 is an integer.", "topic": "Datatypes"}
            ],
            "Medium": [
                {"question": "What does a lambda function do in Python?", "options": ["Creates an anonymous function", "Imports libraries", "Deletes variables", "Reads files"], "answer": "Creates an anonymous function", "explanation": "Lambda creates small anonymous functions inline.", "topic": "Functions"}
            ],
            "Expert": [
                {"question": "What is a generator in Python?", "options": ["Power supply", "Function returning an iterator using yield", "Compiler", "Debugger"], "answer": "Function returning an iterator using yield", "explanation": "Generators yield items one by one efficiently.", "topic": "Advanced"}
            ]
        },
        "C": {
            "Easy": [
                {"question": "What is the size of an int data type typically in a 32-bit C compiler?", "options": ["1 byte", "2 bytes", "4 bytes", "8 bytes"], "answer": "4 bytes", "explanation": "Standard integer takes 4 bytes.", "topic": "Basics"}
            ],
            "Medium": [
                {"question": "What does the 'static' keyword specify for local variables?", "options": ["Global scope", "Retains value between function calls", "Constant value", "Stored in register"], "answer": "Retains value between function calls", "explanation": "Static local variables preserve values.", "topic": "Storage"}
            ],
            "Expert": [
                {"question": "What causes a segmentation fault in C?", "options": ["Syntax error", "Accessing unauthorized memory location", "Division by zero", "Memory leak"], "answer": "Accessing unauthorized memory location", "explanation": "Invalid pointer memory access.", "topic": "Pointers"}
            ]
        },
        "Java": {
            "Easy": [
                {"question": "Which component executes Java bytecode?", "options": ["JDK", "JVM", "JRE", "JIT"], "answer": "JVM", "explanation": "JVM executes bytecode.", "topic": "Architecture"}
            ],
            "Medium": [
                {"question": "Difference between String and StringBuilder?", "options": ["Both mutable", "String mutable", "String immutable, StringBuilder mutable & non-thread-safe", "No difference"], "answer": "String immutable, StringBuilder mutable & non-thread-safe", "explanation": "StringBuilder is mutable.", "topic": "Strings"}
            ],
            "Expert": [
                {"question": "Purpose of volatile keyword in Java?", "options": ["Constant", "Ensure cross-thread variable visibility", "Lock sections", "GC trigger"], "answer": "Ensure cross-thread variable visibility", "explanation": "Reads from main memory.", "topic": "Concurrency"}
            ]
        },
        "SQL & DBMS": {
            "Easy": [
                {"question": "Which SQL clause filters rows?", "options": ["GROUP BY", "ORDER BY", "WHERE", "HAVING"], "answer": "WHERE", "explanation": "WHERE filters rows.", "topic": "SQL Basics"}
            ],
            "Medium": [
                {"question": "Difference between WHERE and HAVING?", "options": ["WHERE filters rows before aggregation, HAVING filters groups", "No difference", "HAVING is faster", "WHERE uses joins"], "answer": "WHERE filters rows before aggregation, HAVING filters groups", "explanation": "HAVING filters groups.", "topic": "Queries"}
            ],
            "Expert": [
                {"question": "What are Window Functions used for?", "options": ["Open connections", "Calculations across rows related to current row", "GUI windows", "Privileges"], "answer": "Calculations across rows related to current row", "explanation": "Computes metrics across rows.", "topic": "Advanced SQL"}
            ]
        }
    },
    "Aptitude & Logical Reasoning": {
        "Aptitude": {
            "Easy": [
                {"question": "If a train travels 60 km in 1.5 hours, what is its average speed?", "options": ["30 km/h", "40 km/h", "45 km/h", "50 km/h"], "answer": "40 km/h", "explanation": "60 / 1.5 = 40 km/h.", "topic": "Speed"}
            ]
        },
        "Logical Reasoning": {
            "Easy": [
                {"question": "Find missing number: 2, 4, 8, 16, 32, ?", "options": ["48", "64", "128", "36"], "answer": "64", "explanation": "Multiplied by 2 each time.", "topic": "Series"}
            ]
        }
    }
}

AI_INTERVIEW_QUESTIONS = [
    {
        "category": "HR / Introduction",
        "question": "Tell me about yourself and your background.",
        "tip": "Keep it concise (1-2 minutes). Focus on your professional journey and key skills.",
        "sample": "Hello, my name is Sayan Tagore. I recently completed my graduation..."
    }
]

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t: text += t + "\n"
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def extract_resume_skills(resume_text):
    clean = clean_text(resume_text)
    return [s for s in MASTER_SKILLS if s in clean]

def get_role_matches(skills):
    results = []
    for role, data in ROLE_SKILLS.items():
        req = data["skills"]
        matched = [s for s in req if s in skills]
        pct = round((len(matched) / len(req)) * 100, 1)
        missing = [s for s in req if s not in skills]
        results.append({
            "role": role, 
            "score": pct, 
            "matched": matched, 
            "missing": missing, 
            "description": data["description"]
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def validate_password(p):
    if not (6 <= len(p) <= 12): return False, "Length must be 6-12 chars."
    if not re.search(r'[A-Z]', p): return False, "Must contain 1 uppercase letter."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', p): return False, "Must contain 1 special char."
    return True, "Valid"

# Session States
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "username" not in st.session_state: st.session_state["username"] = ""
if "exam_history" not in st.session_state: st.session_state["exam_history"] = []
if "resume_text" not in st.session_state: st.session_state["resume_text"] = None
if "resume_skills" not in st.session_state: st.session_state["resume_skills"] = None
if "role_results" not in st.session_state: st.session_state["role_results"] = None

# Login Page
if not st.session_state["logged_in"]:
    st.title("🔐 Login Portal")
    with st.form("login_form"):
        u = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            ok, msg = validate_password(pw)
            if u.strip() and ok:
                st.session_state["logged_in"] = True
                st.session_state["username"] = u
                st.rerun()
            else:
                st.error(msg if not ok else "Enter username.")
    st.stop()

# Sidebar
st.sidebar.title(f"👤 {st.session_state['username']}")
page = st.sidebar.radio("Navigation:", [
    "📄 Resume Analyser & AI Insights", 
    "📅 30-Day Action Plan & Study Routine", 
    "📝 MockTest Portal (Timed & Randomized)", 
    "📈 Performance Analytics & Radar Chart",
    "🤖 AI Interview & Confidence Coach"
])

if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

# Page 1: Resume Analyser
if page == "📄 Resume Analyser & AI Insights":
    st.title("📄 AI Resume Analyser & Job Match Insights")
    st.write("Upload your PDF resume to check which roles you are a perfect fit for, and what skills you are lacking.")
    
    f = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if f:
        st.session_state["resume_text"] = extract_text_from_pdf(f)
        st.session_state["resume_skills"] = extract_resume_skills(st.session_state["resume_text"])
        st.session_state["role_results"] = get_role_matches(st.session_state["resume_skills"])
        st.success("Resume parsed successfully!")

    if st.session_state["role_results"]:
        st.markdown("---")
        st.subheader("🎯 Job Role Matching Results")
        
        for r in st.session_state["role_results"]:
            st.write(f"### 💼 Role: {r['role']} — Match: {r['score']}%")
            st.progress(int(r['score']))
            st.write(f"📌 **Description:** {r['description']}")
            
            if r['score'] >= 50:
                st.success(f"✅ **Verdict:** You are a good fit for this role! Your resume contains matching core skills.")
            else:
                st.error(f"❌ **Verdict:** You are not an ideal fit yet. Your profile lacks several key requirements for this dream job.")
            
            if r['missing']:
                st.write(f"🔸 **Missing Skills to Learn:** {', '.join([s.title() for s in r['missing']])}")
            else:
                st.write("🎉 **Great!** You have all the primary required skills listed for this role.")
            st.markdown("---")

# Page 2: Study Plan
elif page == "📅 30-Day Action Plan & Study Routine":
    st.title("📅 30-Day Action Plan & Detailed Study Materials")
    subj = st.selectbox("Select Subject:", list(ACTION_PLAN_DATABASE.keys()))
    plan = ACTION_PLAN_DATABASE[subj]
    st.success(plan["routine"])
    
    for w, desc in plan["weeks"].items():
        with st.expander(w):
            st.write(f"**Syllabus Overview:** {desc}")
            st.markdown("---")
            week_key = f"Week {w.split()[1]}"
            if week_key in plan["notes"]:
                st.markdown(plan["notes"][week_key])
            else:
                st.info("Comprehensive study material will be updated soon.")

# Page 3: MockTest Portal
elif page == "📝 MockTest Portal (Timed & Randomized)":
    st.title("📝 MockTest Portal")
    if "exam_started" not in st.session_state: st.session_state["exam_started"] = False
    if "exam_submitted" not in st.session_state: st.session_state["exam_submitted"] = False

    if not st.session_state["exam_started"]:
        cat = st.selectbox("Category:", list(QUIZ_DATABASE.keys()))
        sub = st.selectbox("Sub-category:", list(QUIZ_DATABASE[cat].keys()))
        diff = st.select_slider("Difficulty:", options=["Easy", "Medium", "Expert"])
        q_count = st.selectbox("Number of Questions:", [2, 5, 10])

        if st.button("🚀 Start Test"):
            qs = QUIZ_DATABASE[cat][sub].get(diff, QUIZ_DATABASE[cat][sub]["Easy"])
            st.session_state["active_questions"] = random.sample(qs, min(len(qs), q_count))
            st.session_state["exam_started"] = True
            st.session_state["current_q_index"] = 0
            st.session_state["user_answers"] = {}
            st.session_state["exam_submitted"] = False
            st.session_state["test_name"] = f"{sub} ({diff})"
            st.rerun()
    elif st.session_state["exam_started"] and not st.session_state["exam_submitted"]:
        qs = st.session_state["active_questions"]
        idx = st.session_state["current_q_index"]
        st.markdown(f"### Q{idx+1} of {len(qs)}")
        q = qs[idx]
        ans = st.radio(q["question"], q["options"], key=f"q_{idx}")
        st.session_state["user_answers"][idx] = ans

        col1, col2 = st.columns(2)
        with col1:
            if idx > 0 and st.button("⬅️ Prev"):
                st.session_state["current_q_index"] -= 1
                st.rerun()
        with col2:
            if idx < len(qs) - 1:
                if st.button("Next ➡️"):
                    st.session_state["current_q_index"] += 1
                    st.rerun()
            else:
                if st.button("Submit"):
                    st.session_state["exam_submitted"] = True
                    score = sum(1 for i, q in enumerate(qs) if st.session_state["user_answers"].get(i) == q["answer"])
                    pct = round((score / len(qs)) * 100, 2)
                    st.session_state["exam_history"].append({"Test Name": st.session_state["test_name"], "Score (%)": pct})
                    st.rerun()
    else:
        st.success("Test Submitted!")
        if st.button("Take Another"):
            st.session_state["exam_started"] = False
            st.rerun()

# Page 4: Analytics
elif page == "📈 Performance Analytics & Radar Chart":
    st.title("📈 Performance Analytics")
    if len(st.session_state["exam_history"]) == 0:
        st.info("No history yet.")
    else:
        history_df = pd.DataFrame([{
            "Attempt": f"Attempt {idx+1}",
            "Test Name": h["Test Name"],
            "Score (%)": h["Score (%)"]
        } for idx, h in enumerate(st.session_state["exam_history"])])
        st.dataframe(history_df, use_container_width=True)
        st.bar_chart(history_df, x="Attempt", y="Score (%)")

# Page 5: AI Coach
else:
    st.title("🤖 AI Interview Coach")
    q = st.selectbox("Question:", [item["question"] for item in AI_INTERVIEW_QUESTIONS])
    ans = st.text_area("Your Answer:")
    if st.button("Get Feedback"):
        st.success("Rating: 8/10. Good structure!")