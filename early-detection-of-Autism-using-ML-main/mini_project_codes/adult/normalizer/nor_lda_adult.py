import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, Normalizer
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  # Import LDA classifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, cohen_kappa_score, log_loss, matthews_corrcoef
from sklearn.impute import SimpleImputer

# Load dataset
df = pd.read_csv("C:\\Users\\91939\\Downloads\\csv_result-Autism-Adult-Data.csv")
df.drop(df.columns[0], axis=1, inplace=True)

# Separate features and labels
features = df.iloc[:, :-1]
labels = df.iloc[:, -1]

# Select categorical features
category_features = features.iloc[:, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]

# Drop categorical columns
features.drop(features.columns[-10:], axis=1, inplace=True)

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
X_train, X_test, y_train, y_test = train_test_split(result_df, labels, test_size=0.8, random_state=44)

# Define LDA classifier
lda = LinearDiscriminantAnalysis()

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', Normalizer())
        ]), ['A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score', 'A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score']),
        ('cat', Pipeline([
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), category_encoded_columns)
    ],
    remainder='passthrough'
)

# Create pipeline with preprocessing and LDA classifier for training and testing
pipeline_cv_lda = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', lda)
])

# Define 10-fold cross-validation
cv = KFold(n_splits=10, shuffle=True, random_state=42)

# Perform cross-validation on training set
cv_scores_lda = cross_val_score(pipeline_cv_lda, X_train, y_train, cv=cv, scoring='accuracy')

# Print cross-validation scores
print("Cross-validation scores (LDA):", cv_scores_lda)
print("Mean CV accuracy (LDA):", np.mean(cv_scores_lda))

# Train the model on the entire training set using pipeline_cv_lda
pipeline_cv_lda.fit(X_train, y_train)

# Test the model on the separate testing set
y_pred_test_lda = pipeline_cv_lda.predict(X_test)
test_accuracy_test_lda = accuracy_score(y_test, y_pred_test_lda)
print("Testing Set Accuracy with cross-validation (LDA):", test_accuracy_test_lda)
for i in range(5):
    print()
# Calculate and print additional evaluation metrics
print("Precision:", precision_score(y_test, y_pred_test_lda, average='macro'))
print("F1 Score:", f1_score(y_test, y_pred_test_lda, average='macro'))
print("Recall:", recall_score(y_test, y_pred_test_lda, average='macro'))
print("Kappa Score:", cohen_kappa_score(y_test, y_pred_test_lda))
# LDA does not have a predict_proba method, so log_loss cannot be computed
print("Matthews Correlation Coefficient:", matthews_corrcoef(y_test, y_pred_test_lda))
