from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import pickle

from Model_Felix_SPOHR import X_train, y_train

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('mlp', MLPRegressor(hidden_layer_sizes=100, random_state=100))
])

pipeline.fit(X_train, y_train)

pickle.dump(pipeline, open('boite_a_IA.pkl', 'wb'))
