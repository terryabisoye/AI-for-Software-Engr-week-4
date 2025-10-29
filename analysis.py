import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score, confusion_matrix
import pickle


df = pd.read_csv("breastcancer.csv.csv")


print("Dataset loaded sucessfully")
print("Shapes:", df.shape)
print("Columns:", df.columns.to_list()[:10], "...\n")


feature_for_priority = "radius_mean"
if feature_for_priority not in df.columns:
    raise ValueError(f"Column '{feature_for_priority}' not found in your CSV! Please update the name.")

df["priority"] = pd.qcut(df[feature_for_priority], q=3, labels=["low", "medium", "high"])
priority_map = {"low": 0, "medium": 1, "high": 2}
df["priority_label"] = df["priority"].map(priority_map)

print("✅ Priority column created successfully!\n")
print(df[[feature_for_priority, "priority", "priority_label"]].head())

drop_cols = ["priority", "priority_label"]
for col in ["id", "Unnamed: 32", "diagnosis"]:
    if col in df.columns:
        drop_cols.append(col)

X = df.drop(columns=drop_cols, errors="ignore")
y = df["priority_label"]

# -------------------------------------------------------------
# 5. Train-test split
# -------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------------------------------------
# 6. Scale features
# -------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------------------------------------------
# 7. Train RandomForest model
# -------------------------------------------------------------
clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train_scaled, y_train)

# -------------------------------------------------------------
# 8. Evaluate model
# -------------------------------------------------------------
y_pred = clf.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)
f1_macro = f1_score(y_test, y_pred, average="macro")
report = classification_report(y_test, y_pred, target_names=["low", "medium", "high"])
cm = confusion_matrix(y_test, y_pred)

print("\n--- MODEL PERFORMANCE ---")
print(f"Accuracy: {acc:.4f}")
print(f"F1 (macro): {f1_macro:.4f}")
print("\nClassification report:\n", report)
print("Confusion matrix:\n", cm)


