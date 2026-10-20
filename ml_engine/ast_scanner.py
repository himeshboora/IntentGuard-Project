import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser
import os

# 1. Initialize the C++ Parser
CPP_LANGUAGE = Language(tscpp.language())
parser = Parser(CPP_LANGUAGE)

# 2. Read the poisoned C++ file
# This points Python from the ml_engine folder over to the test_code folder
target_file = os.path.join("..", "test_code", "poisoned.cpp")

try:
    with open(target_file, "rb") as f:
        source_code = f.read()
except FileNotFoundError:
    print(f"❌ ERROR: Cannot find {target_file}.")
    print("Please make sure you saved 'poisoned.cpp' in the 'test_code' folder!")
    exit()

tree = parser.parse(source_code)

# 3. Define the AST traversal function
def detect_os_primitives(node):
    # Look for function calls in the syntax tree
    if node.type == 'call_expression':
        node_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
        
        # Check if the function call is a known dangerous OS primitive
        dangerous_calls = ["system(", "execve(", "popen(", "socket("]
        for call in dangerous_calls:
            if call in node_text:
                print(f"🚨 ALERT: Dangerous OS Primitive Detected!")
                print(f"   Line {node.start_point[0] + 1}: {node_text}\n")

    # Recursively check all child branches in the tree
    for child in node.children:
        detect_os_primitives(child)

# 4. Run the scanner
print("Scanning C++ code using AST...\n")
detect_os_primitives(tree.root_node)
print("Scan Complete.")