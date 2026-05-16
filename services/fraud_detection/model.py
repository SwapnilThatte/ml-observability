import xgboost as xgb

class FraudeModel:
    def __init__(self, path: str):
        self.model = xgb.XGBClassifier()
        self.model.load_model(path)

    def predict_proba(self, X):
        return self.model.predict_proba(X)