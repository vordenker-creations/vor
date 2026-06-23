import sqlite3
import os

# Use the same DB path as client_store.db
DB_PATH = os.path.join(os.path.dirname(__file__), "client_store.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_skill_tree_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Create skill_branches table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skill_branches (
        name TEXT PRIMARY KEY,
        color_start TEXT NOT NULL,
        color_end TEXT NOT NULL
    )
    ''')

    # 2. Create skill_nodes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skill_nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch_name TEXT NOT NULL,
        name TEXT NOT NULL,
        mastery INTEGER DEFAULT 0,
        unlocked INTEGER DEFAULT 0,
        x REAL NOT NULL,
        y REAL NOT NULL,
        FOREIGN KEY (branch_name) REFERENCES skill_branches(name) ON DELETE CASCADE
    )
    ''')

    # 3. Create skill_edges table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skill_edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch_name TEXT NOT NULL,
        source_node_id INTEGER NOT NULL,
        target_node_id INTEGER NOT NULL,
        FOREIGN KEY (branch_name) REFERENCES skill_branches(name) ON DELETE CASCADE,
        FOREIGN KEY (source_node_id) REFERENCES skill_nodes(id) ON DELETE CASCADE,
        FOREIGN KEY (target_node_id) REFERENCES skill_nodes(id) ON DELETE CASCADE
    )
    ''')

    # 4. Create skill_missions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skill_missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        FOREIGN KEY (node_id) REFERENCES skill_nodes(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    
    # Seed default data if empty
    cursor.execute("SELECT COUNT(*) FROM skill_branches")
    if cursor.fetchone()[0] == 0:
        seed_default_data(conn)
        
    conn.close()
    recalculate_all_layouts()

def seed_default_data(conn):
    cursor = conn.cursor()
    
    default_branches = {
        "Software Dev": {
            "color_start": "#06B6D4",
            "color_end":   "#3B82F6",
            "nodes": [
                {"name": "Python",       "mastery": 90, "unlocked": 1, "x": -320, "y": -60},
                {"name": "C++",          "mastery": 75, "unlocked": 1, "x": -420, "y": -180},
                {"name": "Java",         "mastery": 60, "unlocked": 1, "x": -220, "y": -180},
                {"name": "Web Dev",      "mastery": 40, "unlocked": 1, "x": -320, "y": -300},
                {"name": "System Design","mastery": 0,  "unlocked": 0, "x": -420, "y": -420},
                {"name": "DevOps",       "mastery": 0,  "unlocked": 0, "x": -220, "y": -420},
            ],
            "edges": [(0,1),(0,2),(1,3),(2,3),(3,4),(3,5)]
        },
        "Artificial Intelligence": {
            "color_start": "#8B5CF6",
            "color_end":   "#EC4899",
            "nodes": [
                {"name": "Machine Learning","mastery": 80, "unlocked": 1, "x": 0, "y": -60},
                {"name": "Deep Learning",   "mastery": 55, "unlocked": 1, "x": -80, "y": -200},
                {"name": "Computer Vision", "mastery": 45, "unlocked": 1, "x": 80,  "y": -200},
                {"name": "NLP",             "mastery": 0,  "unlocked": 0, "x": -80, "y": -340},
                {"name": "Reinforcement L.","mastery": 0,  "unlocked": 0, "x": 80,  "y": -340},
                {"name": "AGI Research",    "mastery": 0,  "unlocked": 0, "x": 0,   "y": -460},
            ],
            "edges": [(0,1),(0,2),(1,3),(2,4),(3,5),(4,5)]
        },
        "Hardware & IoT": {
            "color_start": "#F59E0B",
            "color_end":   "#EF4444",
            "nodes": [
                {"name": "Arduino",          "mastery": 85, "unlocked": 1, "x": 320, "y": -60},
                {"name": "ESP32",            "mastery": 70, "unlocked": 1, "x": 220, "y": -180},
                {"name": "Robotics",         "mastery": 65, "unlocked": 1, "x": 420, "y": -180},
                {"name": "FPV Drones",       "mastery": 35, "unlocked": 1, "x": 320, "y": -300},
                {"name": "FPGA Design",      "mastery": 0,  "unlocked": 0, "x": 220, "y": -420},
                {"name": "Adv. Robotics",    "mastery": 0,  "unlocked": 0, "x": 420, "y": -420},
            ],
            "edges": [(0,1),(0,2),(1,3),(2,3),(3,4),(3,5)]
        }
    }

    for b_name, b_data in default_branches.items():
        cursor.execute(
            "INSERT INTO skill_branches (name, color_start, color_end) VALUES (?, ?, ?)",
            (b_name, b_data["color_start"], b_data["color_end"])
        )
        
        # Insert nodes and save their SQLite generated IDs
        node_ids = []
        for node in b_data["nodes"]:
            cursor.execute(
                "INSERT INTO skill_nodes (branch_name, name, mastery, unlocked, x, y) VALUES (?, ?, ?, ?, ?, ?)",
                (b_name, node["name"], node["mastery"], node["unlocked"], node["x"], node["y"])
            )
            node_ids.append(cursor.lastrowid)
            
        # Insert edges using mapped node IDs
        for u, v in b_data["edges"]:
            cursor.execute(
                "INSERT INTO skill_edges (branch_name, source_node_id, target_node_id) VALUES (?, ?, ?)",
                (b_name, node_ids[u], node_ids[v])
            )
            
    conn.commit()

# ==========================================
# CRUD Operations
# ==========================================

# 1. Branch Operations
def get_all_branches():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skill_branches")
    branches = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return branches

def add_branch(name, color_start, color_end):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO skill_branches (name, color_start, color_end) VALUES (?, ?, ?)",
            (name, color_start, color_end)
        )
        conn.commit()
        recalculate_all_layouts()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_branch(old_name, new_name, color_start, color_end):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE skill_branches SET name = ?, color_start = ?, color_end = ? WHERE name = ?",
            (new_name, color_start, color_end, old_name)
        )
        conn.commit()
        recalculate_all_layouts()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_branch(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skill_branches WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    recalculate_all_layouts()

# 2. Node Operations
def get_nodes_by_branch(branch_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skill_nodes WHERE branch_name = ?", (branch_name,))
    nodes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return nodes

def add_node(branch_name, name, mastery, unlocked, parent_node_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO skill_nodes (branch_name, name, mastery, unlocked, x, y) VALUES (?, ?, ?, ?, 0.0, 0.0)",
        (branch_name, name, mastery, unlocked)
    )
    new_id = cursor.lastrowid
    
    if parent_node_id:
        cursor.execute(
            "INSERT INTO skill_edges (branch_name, source_node_id, target_node_id) VALUES (?, ?, ?)",
            (branch_name, parent_node_id, new_id)
        )
        
    conn.commit()
    conn.close()
    recalculate_all_layouts()
    return new_id

def update_node(node_id, name, mastery, unlocked, parent_node_id=None, change_parent=False):
    conn = get_connection()
    cursor = conn.cursor()
    
    if change_parent:
        # Check for cycle before making updates
        if parent_node_id and is_path_exists(node_id, parent_node_id):
            conn.close()
            return False, "Adding this prerequisite would create a cyclic dependency loop."
            
        cursor.execute("SELECT branch_name FROM skill_nodes WHERE id = ?", (node_id,))
        branch_row = cursor.fetchone()
        if branch_row:
            branch_name = branch_row["branch_name"]
            
            # Delete old incoming edges
            cursor.execute("DELETE FROM skill_edges WHERE target_node_id = ?", (node_id,))
            # Insert new edge if parent specified
            if parent_node_id:
                cursor.execute(
                    "INSERT INTO skill_edges (branch_name, source_node_id, target_node_id) VALUES (?, ?, ?)",
                    (branch_name, parent_node_id, node_id)
                )

    cursor.execute(
        "UPDATE skill_nodes SET name = ?, mastery = ?, unlocked = ? WHERE id = ?",
        (name, mastery, unlocked, node_id)
    )
            
    conn.commit()
    conn.close()
    recalculate_all_layouts()
    return True, ""

def delete_node(node_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skill_nodes WHERE id = ?", (node_id,))
    conn.commit()
    conn.close()
    recalculate_all_layouts()

# 3. Edge Operations
def get_edges_by_branch(branch_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skill_edges WHERE branch_name = ?", (branch_name,))
    edges = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return edges

def add_edge(branch_name, source_node_id, target_node_id):
    if is_path_exists(target_node_id, source_node_id):
        return None  # Cycle detected
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if already exists
        cursor.execute(
            "SELECT id FROM skill_edges WHERE branch_name = ? AND source_node_id = ? AND target_node_id = ?",
            (branch_name, source_node_id, target_node_id)
        )
        if cursor.fetchone():
            return None
        cursor.execute(
            "INSERT INTO skill_edges (branch_name, source_node_id, target_node_id) VALUES (?, ?, ?)",
            (branch_name, source_node_id, target_node_id)
        )
        new_id = cursor.lastrowid
        conn.commit()
        recalculate_all_layouts()
        return new_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def delete_edge(edge_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skill_edges WHERE id = ?", (edge_id,))
    conn.commit()
    conn.close()
    recalculate_all_layouts()

def delete_edge_by_nodes(source_node_id, target_node_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM skill_edges WHERE (source_node_id = ? AND target_node_id = ?) OR (source_node_id = ? AND target_node_id = ?)",
        (source_node_id, target_node_id, target_node_id, source_node_id)
    )
    conn.commit()
    conn.close()
    recalculate_all_layouts()

# 4. Load full structured branches (replicating SKILL_BRANCHES style)
def load_skill_branches_structured():
    init_skill_tree_db()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all branches
    cursor.execute("SELECT * FROM skill_branches")
    branches_rows = cursor.fetchall()
    
    structured_data = {}
    
    for branch in branches_rows:
        b_name = branch["name"]
        color_start = branch["color_start"]
        color_end = branch["color_end"]
        
        # Get nodes
        cursor.execute("SELECT * FROM skill_nodes WHERE branch_name = ?", (b_name,))
        nodes_rows = [dict(row) for row in cursor.fetchall()]
        
        # Map node SQLite ID to its index in list for compatibility with old code or just use SQLite IDs!
        # Wait, the old code drew edges by indices `(u, v)`. Let's support BOTH index-based edges drawing OR drawing by direct node positions.
        # It's cleaner to map node IDs to indices to reuse edge drawings if needed, OR we can query edges and look up positions.
        # Let's map node IDs to their index in the list:
        id_to_index = {node["id"]: idx for idx, node in enumerate(nodes_rows)}
        
        # Format nodes as expected by SkillTreeCanvas, adding 'id' key for edit/delete actions!
        nodes_list = []
        for node in nodes_rows:
            nodes_list.append({
                "id": node["id"],
                "name": node["name"],
                "mastery": node["mastery"],
                "unlocked": bool(node["unlocked"]),
                "x": node["x"],
                "y": node["y"]
            })
            
        # Get edges
        cursor.execute("SELECT * FROM skill_edges WHERE branch_name = ?", (b_name,))
        edges_rows = cursor.fetchall()
        
        edges_list = []
        for edge in edges_rows:
            src_id = edge["source_node_id"]
            tgt_id = edge["target_node_id"]
            if src_id in id_to_index and tgt_id in id_to_index:
                edges_list.append((id_to_index[src_id], id_to_index[tgt_id]))
                
        structured_data[b_name] = {
            "color_start": color_start,
            "color_end": color_end,
            "nodes": nodes_list,
            "edges": edges_list,
            "raw_edges": [dict(row) for row in edges_rows] # for management
        }
        
    conn.close()
    return structured_data

def get_suggested_coordinates(branch_name):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Fetch nodes of this branch
    cursor.execute("SELECT x, y FROM skill_nodes WHERE branch_name = ?", (branch_name,))
    nodes = cursor.fetchall()
    
    # If no nodes exist in this branch yet, calculate branch center X relative to other branches
    if not nodes:
        cursor.execute("SELECT x FROM skill_nodes")
        all_nodes = cursor.fetchall()
        if not all_nodes:
            conn.close()
            return (0.0, -60.0)
        
        # Group all nodes by branch name to find their center Xs
        cursor.execute("SELECT branch_name, AVG(x) as center_x FROM skill_nodes GROUP BY branch_name")
        centers = [row["center_x"] for row in cursor.fetchall() if row["center_x"] is not None]
        if not centers:
            conn.close()
            return (0.0, -60.0)
        
        # Place new branch to the right of the rightmost branch
        new_branch_center_x = max(centers) + 320.0
        conn.close()
        return (new_branch_center_x, -60.0)
        
    # Calculate branch center X
    branch_center_x = sum(node["x"] for node in nodes) / len(nodes)
    
    # Group nodes by Y level: level_idx = round((y - (-60.0)) / -120.0)
    levels = {}
    for node in nodes:
        y = node["y"]
        level_idx = int(round((y - (-60.0)) / -120.0))
        if level_idx < 0:
            level_idx = 0
        levels.setdefault(level_idx, []).append(node["x"])
        
    # Find the first level index L that has room based on alternating capacity
    L = 0
    while True:
        level_nodes = levels.get(L, [])
        is_even_level = (L % 2 == 0)
        max_capacity = 1 if is_even_level else 2
        
        if len(level_nodes) < max_capacity:
            y_coord = -60.0 - L * 120.0
            if is_even_level:
                # Even levels have 1 node at the center
                conn.close()
                return (branch_center_x, y_coord)
            else:
                # Odd levels have 2 nodes at center - 100 and center + 100
                if len(level_nodes) == 0:
                    conn.close()
                    return (branch_center_x - 100.0, y_coord)
                else:
                    ex_x = level_nodes[0]
                    if ex_x < branch_center_x:
                        conn.close()
                        return (branch_center_x + 100.0, y_coord)
                    else:
                        conn.close()
                        return (branch_center_x - 100.0, y_coord)
        L += 1

def get_missions_by_node(node_id, skill_name=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM skill_missions WHERE node_id = ?", (node_id,))
    rows = [dict(row) for row in cursor.fetchall()]
    
    if not rows and skill_name:
        # Generate default missions based on skill name
        default_titles = [
            f"Learn fundamental concepts and syntax of {skill_name}",
            f"Build a small practical project using {skill_name}",
            f"Solve coding algorithms & practical challenges on {skill_name}",
            f"Complete a mock interview simulation for {skill_name}"
        ]
        
        lower_name = skill_name.lower()
        if "python" in lower_name:
            default_titles = [
                "Master Python basics (variables, control flow, functions)",
                "Understand Data Structures (lists, sets, dictionaries, tuples)",
                "Study Object-Oriented Programming (Classes, inheritance, methods)",
                "Implement Advanced Topics (decorators, generators, threading, file I/O)"
            ]
        elif "java" in lower_name:
            default_titles = [
                "Learn Java fundamentals (JVM, syntax, memory management)",
                "Master OOP principles in Java (Encapsulation, Polymorphism, Inheritance)",
                "Understand Java Collections & Streams (List, Map, Set, stream API)",
                "Build multithreaded apps and database connection (JDBC/Hibernate)"
            ]
        elif "c++" in lower_name:
            default_titles = [
                "Understand C++ basics (syntax, pointers, memory allocation)",
                "Master Object-Oriented C++ (classes, constructors, destructors)",
                "Study Standard Template Library (STL) (vectors, maps, algorithms)",
                "Implement Memory Management (Smart pointers, move semantics, OOP design)"
            ]
        elif "web" in lower_name or "html" in lower_name or "css" in lower_name or "javascript" in lower_name:
            default_titles = [
                "Master HTML5 structure & Semantic Tags",
                "Learn modern CSS layouts (Flexbox, Grid, Responsive Design)",
                "Understand JavaScript DOM manipulation and event handling",
                "Build a fully interactive single-page app and connect to APIs"
            ]
        elif "machine learning" in lower_name or "ml" in lower_name:
            default_titles = [
                "Understand math foundation (Linear Algebra, Calculus, Statistics)",
                "Master supervised & unsupervised algorithms (Regression, Clustering)",
                "Learn data preprocessing & model evaluation using Scikit-Learn",
                "Deploy a trained ML model as an API service"
            ]
            
        for title in default_titles:
            cursor.execute(
                "INSERT INTO skill_missions (node_id, title, completed) VALUES (?, ?, 0)",
                (node_id, title)
            )
        conn.commit()
        
        cursor.execute("SELECT * FROM skill_missions WHERE node_id = ?", (node_id,))
        rows = [dict(row) for row in cursor.fetchall()]
        
    conn.close()
    return rows

def update_mission_completed(mission_id, completed):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE skill_missions SET completed = ? WHERE id = ?",
        (completed, mission_id)
    )
    conn.commit()
    conn.close()

def get_parent_node_id(node_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT source_node_id FROM skill_edges WHERE target_node_id = ?", (node_id,))
    row = cursor.fetchone()
    conn.close()
    return row["source_node_id"] if row else None

def is_path_exists(source_id, target_id):
    if source_id == target_id:
        return True
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT source_node_id, target_node_id FROM skill_edges")
    edges = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Build adjacency list
    adj = {}
    for edge in edges:
        s, t = edge["source_node_id"], edge["target_node_id"]
        adj.setdefault(s, []).append(t)
        
    # BFS traversal
    queue = [source_id]
    visited = {source_id}
    while queue:
        curr = queue.pop(0)
        if curr == target_id:
            return True
        for neighbor in adj.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return False

def recalculate_all_layouts():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Get all branches sorted
    cursor.execute("SELECT name FROM skill_branches ORDER BY name")
    branches = [row["name"] for row in cursor.fetchall()]
    num_branches = len(branches)
    
    for idx, b_name in enumerate(branches):
        # Stack branches vertically: space them vertically by 350px
        if num_branches > 1:
            branch_center_y = (idx - (num_branches - 1) / 2) * 350.0
        else:
            branch_center_y = 0.0
            
        # Get all nodes in this branch
        cursor.execute("SELECT id, name FROM skill_nodes WHERE branch_name = ?", (b_name,))
        nodes = [dict(row) for row in cursor.fetchall()]
        if not nodes:
            continue
            
        node_ids = {node["id"] for node in nodes}
        
        # Get all edges in this branch
        cursor.execute("SELECT id, source_node_id, target_node_id FROM skill_edges WHERE branch_name = ?", (b_name,))
        edges = [dict(row) for row in cursor.fetchall()]
        
        # Find which nodes have incoming edges
        incoming_nodes = {edge["target_node_id"] for edge in edges if edge["target_node_id"] in node_ids}
        
        # Root nodes are those with no incoming edges
        roots = [node for node in nodes if node["id"] not in incoming_nodes]
        # In case of cycles or weird edge cases, if no roots found, pick the first node as root
        if not roots:
            roots = [nodes[0]]
            
        # Sort roots to maintain deterministic layout
        roots.sort(key=lambda n: n["name"])
        
        # Map parent node ID -> list of child node IDs
        parent_to_children = {}
        for edge in edges:
            src = edge["source_node_id"]
            tgt = edge["target_node_id"]
            if src in node_ids and tgt in node_ids:
                parent_to_children.setdefault(src, []).append(tgt)
                
        # Sort children deterministically by name
        node_names = {node["id"]: node["name"] for node in nodes}
        for parent_id in parent_to_children:
            parent_to_children[parent_id].sort(key=lambda cid: node_names.get(cid, ""))
            
        # Recursive function to assign coordinates
        positioned_nodes = {} # node_id -> (x, y)
        visited = set()
        
        # In left-to-right layout:
        # - Roots start on the left (x = -450)
        # - Children grow to the right (x increases by 160 per level)
        # - Vertically spaced (y changes)
        def position_subtree(node_id, x, y, depth):
            if node_id in visited:
                return
            visited.add(node_id)
            positioned_nodes[node_id] = (x, y)
            children = parent_to_children.get(node_id, [])
            if not children:
                return
                
            # Vertical spacing decreases with depth to prevent subtrees overlap
            spacing = max(80.0, 180.0 / (depth + 1))
            num_children = len(children)
            for i, child_id in enumerate(children):
                offset = (i - (num_children - 1) / 2) * spacing
                position_subtree(child_id, x + 160.0, y + offset, depth + 1)
                
        # Position roots vertically spaced on the left
        num_roots = len(roots)
        root_spacing = 200.0
        for i, root in enumerate(roots):
            root_offset = (i - (num_roots - 1) / 2) * root_spacing
            position_subtree(root["id"], -450.0, branch_center_y + root_offset, 0)
            
        # Write coordinates back to database
        for node_id, (x, y) in positioned_nodes.items():
            cursor.execute(
                "UPDATE skill_nodes SET x = ?, y = ? WHERE id = ?",
                (x, y, node_id)
            )
            
    conn.commit()
    conn.close()

