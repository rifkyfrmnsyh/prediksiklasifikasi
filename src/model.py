from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.metrics import (
    classification_report, confusion_matrix, f1_score,
    roc_auc_score, roc_curve
)
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def get_models():
    return {
        "Gaussian Naive Bayes": GaussianNB(),
    }


def tune_model(name, X_train, y_train):

    if name == "Gaussian Naive Bayes":
        param_grid = {
            'var_smoothing': [1e-9, 1e-8, 1e-7]
        }
        model = GaussianNB()

    else:
        raise ValueError(f"Model tuning belum tersedia untuk: {name}")

    grid_search = GridSearchCV(model, param_grid, cv=10, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    return grid_search.best_estimator_, grid_search.best_params_


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = model.score(X_test, y_test)
    f1 = f1_score(y_test, y_pred)

    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]


    report = classification_report(y_test, y_pred, output_dict=True)


    st.subheader("📄 Classification Report")

    st.write(f"**Accuracy:** {accuracy:.3f}")
    st.write(f"**F1-score:** {f1:.3f}")


    return accuracy, report
