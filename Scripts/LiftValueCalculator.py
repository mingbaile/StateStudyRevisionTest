import os
import pandas as pd

# Set classification directory paths
reason_dir = "RootCausesClassification"
exposure_dir = "ExploitationMethodsClassification"

# Get bug IDs under each category (all are numeric strings)
def load_category_files(root_dir):
    category_map = {}
    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        if os.path.isdir(category_path):
            bug_ids = set(os.listdir(category_path))  # bug file names are numeric strings, no extensions
            category_map[category] = bug_ids
    return category_map

# Load classification data
reason_map = load_category_files(reason_dir)
exposure_map = load_category_files(exposure_dir)

# Complete set of all bugs
all_bugs = set()
for bugs in reason_map.values():
    all_bugs.update(bugs)
total_bugs = len(all_bugs)

# Sort rows and columns by bug count
sorted_reasons = sorted(reason_map.items(), key=lambda x: len(x[1]), reverse=True)
sorted_exposures = sorted(exposure_map.items(), key=lambda x: len(x[1]), reverse=True)

# Build result matrix
lift_matrix = []

for reason_name, reason_bugs in sorted_reasons:
    row = []
    for exposure_name, exposure_bugs in sorted_exposures:
        intersection = reason_bugs & exposure_bugs
        p_a = len(reason_bugs) / total_bugs
        p_b = len(exposure_bugs) / total_bugs
        p_ab = len(intersection) / total_bugs
        lift = p_ab / (p_a * p_b) if p_a > 0 and p_b > 0 else 0
        row.append(round(lift, 4))  # Keep 4 decimal places
    lift_matrix.append(row)

# Build DataFrame
row_labels = [name for name, _ in sorted_reasons]
col_labels = [name for name, _ in sorted_exposures]
df = pd.DataFrame(lift_matrix, index=row_labels, columns=col_labels)

# Save as Excel
df.to_excel("lift_matrix.xlsx")

print("File generated: lift_matrix.xlsx")