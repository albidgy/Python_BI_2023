from sklearn.base import BaseEstimator
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
import numpy as np

from concurrent.futures import ProcessPoolExecutor


class RandomForestClassifierCustom(BaseEstimator):
    def __init__(
            self, n_estimators=10, max_depth=None, max_features=None, random_state=None
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.random_state = random_state
        self.trees = []
        self.feat_ids_by_tree = []

    def _fitting_model(self, i):
        np.random.seed(self.random_state + i)
        features_ids = np.random.choice(self.X.shape[1], size=self.max_features, replace=False)
        pseudosampling_ids = np.random.choice(self.X.shape[0], size=self.X.shape[0], replace=True)
        pseudo_X = self.X[pseudosampling_ids][:, features_ids]
        pseudo_y = self.y[pseudosampling_ids]

        tree_class = DecisionTreeClassifier(max_depth=self.max_depth,
                                            max_features=self.max_features,
                                            random_state=self.random_state,
                                            )
        fitted_tree = tree_class.fit(pseudo_X, pseudo_y)
        return fitted_tree, features_ids

    def fit(self, X, y, n_jobs=1):
        self.X = X
        self.y = y
        self.classes_ = sorted(np.unique(self.y))
        with ProcessPoolExecutor(n_jobs) as pool:
            processes = list(pool.map(self._fitting_model, list(range(self.n_estimators))))
            for proc in processes:
                tree, feat_ids = proc
                self.trees.append(tree)
                self.feat_ids_by_tree.append(feat_ids)
            return self

    def _prediction_calc(self, tree_and_feat_ids):
        tree, feat_ids = tree_and_feat_ids
        pred = tree.predict_proba(self.X[:, feat_ids])
        return pred

    def predict_proba(self, X, n_jobs=1):
        self.X = X
        y_pred = np.zeros((self.X.shape[0], len(self.classes_)))
        with ProcessPoolExecutor(n_jobs) as pool:
            processes = list(pool.map(self._prediction_calc, zip(self.trees, self.feat_ids_by_tree)))
            for proc in processes:
                y_pred += proc
        return y_pred

    def predict(self, X, n_jobs=1):
        probas = self.predict_proba(X, n_jobs)
        predictions = np.argmax(probas, axis=1)
        return predictions


X, y = make_classification(n_samples=100000)

# if __name__ == '__main__':
#     random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)
#     _ = random_forest.fit(X, y, n_jobs=1)
#     preds_1 = random_forest.predict(X)
#     random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)
#     _ = random_forest.fit(X, y, n_jobs=2)
#     preds_2 = random_forest.predict(X, n_jobs=2)
#     print((preds_1 == preds_2).all())
