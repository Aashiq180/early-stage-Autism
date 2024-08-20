import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, Normalizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

# Load dataset
df = pd.read_csv("C:\\Users\\91939\\Downloads\\csv_result-Autism-Adolescent-Data.csv")
df.drop(df.columns[0], axis=1, inplace=True)

# Separate features and labels
features = df.iloc[:, :-1]
labels = df.iloc[:, -1]

# Select categorical features
category_features = features.iloc[:, [11, 12, 13, 14, 15, 16, 17, 18, 19]]

# Drop categorical columns
features.drop(features.columns[-9:], axis=1, inplace=True)

# Fill missing values with mean
features = features.fillna(features.mean())

# One Hot Encoding without changing column names
enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
category_transformed = enc.fit_transform(category_features)
category_encoded_columns = enc.get_feature_names_out(category_features.columns)
transformed_df = pd.DataFrame(category_transformed, columns=category_encoded_columns)

# Concatenate encoded features with numerical features
result_df = pd.concat([features, transformed_df], axis=1)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(result_df, labels, test_size=0.16, random_state=42)

# Define Random Forest classifier
random_forest = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=42)

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler()),
            ('normalize', Normalizer())
        ]), ['A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score', 'A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score', 'age']),
        ('cat', Pipeline([
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), category_encoded_columns)
    ],
    remainder='passthrough'
)

# Create pipeline with preprocessing and Random Forest classifier for training and testing
pipeline_rf_normalize = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', random_forest)
])

# Perform 10-fold cross-validation
cv_scores = cross_val_score(pipeline_rf_normalize, X_train, y_train, cv=10)

# Print cross-validation scores
print("Cross-validation scores:", cv_scores)
print("Mean CV accuracy:", np.mean(cv_scores))

# Train the model on the entire training set
pipeline_rf_normalize.fit(X_train, y_train)

# Test the model on the separate testing set
y_pred_test = pipeline_rf_normalize.predict(X_test)
test_accuracy_test_rf_normalize = accuracy_score(y_test, y_pred_test)
print("Testing Set Accuracy with cross-validation (Random Forest with Normalizer):", test_accuracy_test_rf_normalize)

from sklearn.metrics import precision_score, f1_score, roc_curve, auc, recall_score, cohen_kappa_score, log_loss, matthews_corrcoef

print("printing precision")
print(precision_score(y_test, y_pred_test, average='macro'))
print("f1-score")

# # F1 Score
print(f1_score(y_test, y_pred_test,average='macro'))

import matplotlib.pyplot as plt

# ... (your existing code)

# Test the model on the separate testing set
y_prob_test = pipeline_rf_normalize.predict_proba(X_test)[:, 1]
y_pred_test = pipeline_rf_normalize.predict(X_test)
test_accuracy_test = accuracy_score(y_test, y_pred_test)
print("Testing Set Accuracy without cross-validation:", test_accuracy_test)

from sklearn.metrics import roc_auc_score



# Test the model on the separate testing set
y_prob_test = pipeline_rf_normalize.predict_proba(X_test)[:, 1]
y_pred_test = pipeline_rf_normalize.predict(X_test)
test_accuracy_test = accuracy_score(y_test, y_pred_test)
print("Testing Set Accuracy without cross-validation:", test_accuracy_test)

# Calculate ROC AUC
roc_auc = roc_auc_score(y_test, y_prob_test)
print("ROC AUC:", roc_auc)

print('recall')
# # Recall
print(recall_score(y_test, y_pred_test,average='macro'))

print('kappa score')
# # Kappa Score
print(cohen_kappa_score(y_test, y_pred_test))

print('log loss')
# # Log Loss
print(log_loss(y_test, pipeline_rf_normalize.predict_proba(X_test)))

print('MCC')
# # Matthews Correlation Coefficient
print(matthews_corrcoef(y_test, y_pred_test))