#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sklearn import datasets

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

from mlxtend.classifier import EnsembleVoteClassifier, StackingClassifier

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mlxtend.plotting import plot_decision_regions

# Load demo data
iris = datasets.load_iris()
X, y = iris.data[:, [0, 2]], iris.target

# Models

# Logistic Regression
clf_lr = LogisticRegression(solver='lbfgs', multi_class='multinomial', random_state=1)
clf_meta_lr = LogisticRegression(solver='lbfgs', multi_class='multinomial', random_state=1)

# Decision Tree
clf_dt = DecisionTreeClassifier(max_depth=4, random_state=1)

# KNN
clf_knn = KNeighborsClassifier(n_neighbors=4)

# SVC
clf_svc = SVC(gamma='scale', kernel='rbf', probability=True, random_state=1)

# Naive Bayes
clf_nb = GaussianNB()

# MLP
clf_mlp = MLPClassifier(hidden_layer_sizes=(4, 4), activation='logistic', solver='lbfgs', random_state=1)

# Random Forest
clf_rf = RandomForestClassifier(n_estimators=4, max_depth=4, random_state=1)

# Vote
clf_vot = EnsembleVoteClassifier(
    clfs=[clf_lr, clf_dt, clf_knn, clf_svc, clf_nb, clf_mlp, clf_rf],
    voting='soft'
)

# Stacking
clf_stk = StackingClassifier(
    classifiers=[clf_lr, clf_dt, clf_knn, clf_svc, clf_nb, clf_mlp, clf_rf],
    meta_classifier=clf_meta_lr
)

# Fit and plot
clf_names = [
    'Logistic Regression\n(Multi Class: Multinomial)', 'Decision Tree\n(Depth: 4)', 'KNN\n(K: 4)',
    'SVC\n(Kernel: RBF)', 'Naive Bayes\n(Priors: None)', 'MLP\n(Hidden Layer Size: (4, 4))',
    'Random Forest\n(#Tree: 4, Max Depth: 4)', 'Voting\n(Method: Soft)', 'Stacking\n(Meta Classifier: LR)']
clfs = [clf_lr, clf_dt, clf_knn,
        clf_svc, clf_nb, clf_mlp,
        clf_rf, clf_vot, clf_stk]

fig = plt.figure(figsize=(8, 9))
gs = gridspec.GridSpec(3, 3)

for clf, name, grid in zip(clfs, clf_names, range(len(clfs))):
    clf.fit(X, y)
    ax = plt.subplot(gs[int(grid / 3), grid % 3])
    plot_decision_regions(X=X, y=y, clf=clf, legend=2)
    plt.axis('off')
    plt.tight_layout()
    plt.title(name)

plt.savefig('clfs-decision-regions.png')
