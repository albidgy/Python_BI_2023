from sklearn.base import BaseEstimator
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
import numpy as np

from concurrent.futures import ProcessPoolExecutor


class RandomForestClassifierCustom(BaseEstimator):
    '''
    Random forest classifier based on DecisionTreeClassifier (scikit-learn).
    '''

    def __init__(
            self, n_estimators=10, max_depth=None, max_features=None, random_state=None
    ):
        '''
        :param int n_estimators: number of trees in random forest (by default 10)
        :param int or None max_depth: max depht for every tree (by default None)
        :param int or None max_features: max features (by default None)
        :param int or None random_state: random state (by default None)
        '''
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.random_state = random_state
        self.trees = []
        self.feat_ids_by_tree = []

    def _fitting_model(self, idx):
        '''
        Fitting tree. Helper method for fit().

        :param int idx: index of tree
        :return: fitted tree and featured indices
        '''
        np.random.seed(self.random_state + idx)
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
        '''
        Basic method for fitting trees. Can work in multiprocessor mode.

        :param np.ndarray X: array of features
        :param np.ndarray y: array of targets
        :param int n_jobs: number of processes (by default 1)
        :return: self object
        '''
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
        '''
        Calculate y_pred. Helper method for predict_proba().

        :param int tree_and_feat_ids: fitted tree and featured indices
        :return: prediction by tree
        '''
        tree, feat_ids = tree_and_feat_ids
        pred = tree.predict_proba(self.X[:, feat_ids])
        return pred

    def predict_proba(self, X, n_jobs=1):
        '''
        Predicting classes by X.

        :param np.ndarray X: array of features
        :param int n_jobs: number of processes (by default 1)
        :return: predicted y (target)
        '''
        self.X = X
        y_pred = np.zeros((self.X.shape[0], len(self.classes_)))
        with ProcessPoolExecutor(n_jobs) as pool:
            processes = list(pool.map(self._prediction_calc, zip(self.trees, self.feat_ids_by_tree)))
            for proc in processes:
                y_pred += proc
        return y_pred

    def predict(self, X, n_jobs=1):
        '''
        Maximizes received predictions

        :param np.ndarray X: array of features
        :param int n_jobs: number of processes (by default 1)
        :return: predicted labels
        '''
        probas = self.predict_proba(X, n_jobs)
        predictions = np.argmax(probas, axis=1)
        return predictions


X, y = make_classification(n_samples=100000)
