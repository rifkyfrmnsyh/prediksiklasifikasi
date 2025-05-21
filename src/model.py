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
        auc = roc_auc_score(y_test, y_proba)
    else:
        auc = None

    report = classification_report(y_test, y_pred, output_dict=True)

    st.subheader("📊 Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    st.pyplot(fig)

    st.subheader("📄 Classification Report")
    st.json(report)

    st.write(f"**Accuracy:** {accuracy:.3f}")
    st.write(f"**F1-score:** {f1:.3f}")

    if auc is not None:
        st.write(f"**ROC AUC:** {auc:.3f}")
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        fig2, ax2 = plt.subplots()
        ax2.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
        ax2.plot([0, 1], [0, 1], linestyle="--", color="gray")
        ax2.set_xlabel("False Positive Rate")
        ax2.set_ylabel("True Positive Rate")
        ax2.set_title("ROC Curve")
        ax2.legend()
        st.pyplot(fig2)

    return accuracy, report
