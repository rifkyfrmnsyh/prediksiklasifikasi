from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score, roc_auc_score, roc_curve
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def get_models():
    return {
        "Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier()
    }

def tune_model(name, X_train, y_train):
    if name == "Decision Tree":
        param_grid = {
            'max_depth': [3, 5, 10, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        model = DecisionTreeClassifier(random_state=42)

    elif name == "K-Nearest Neighbors":
        param_grid = {
            'n_neighbors': [3, 5, 7, 9],
            'weights': ['uniform', 'distance']
        }
        model = KNeighborsClassifier()

    elif name == "Naive Bayes":
        param_grid = {
            'var_smoothing': [1e-09, 1e-08, 1e-07]
        }
        model = GaussianNB()

    else:
        raise ValueError(f"Model tuning belum tersedia untuk: {name}")

    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    return best_model, best_params


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = model.score(X_test, y_test)
    f1 = f1_score(y_test, y_pred)

    # ROC AUC hanya untuk klasifikasi biner dan perlu prediksi probabilitas
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
    if auc:
        st.write(f"**ROC AUC:** {auc:.3f}")
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        fig2, ax2 = plt.subplots()
        ax2.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
        ax2.plot([0,1], [0,1], linestyle="--", color="gray")
        ax2.set_xlabel("False Positive Rate")
        ax2.set_ylabel("True Positive Rate")
        ax2.set_title("ROC Curve")
        ax2.legend()
        st.pyplot(fig2)

    return accuracy, report
