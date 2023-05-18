""" Cross validates parameters for different latent dimensionality.

 Latent Dimensions tested are 5, 10, 15, 20, 25, 30."""

from modelUtils.vae_utils import create_param_grid, VAECrossValidator
import os
from utils import data_validation
import pickle

import tensorflow as tf
import matplotlib.pyplot as plt
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

#%%
cur = os.getcwd()
filepath = os.path.join(cur, 'outputs/megasample_cleaned.csv')
train_data, val_data, test_data = data_validation(filepath)
input_dim = train_data.element_spec[0].shape[0]

#%%
# Cross Validation for 10 dimension latent space
latent_dims = [10]
beta = [1e-5, 1e-4, 1e-3]
hidden_dims = [[100, 100], [150, 150], [200, 200], [250, 250], [300, 300], [150, 100, 50], [200, 150, 100],
               [250, 200, 150], [300, 200, 100]]
epochs = 100

dropout = [0.1, 0.2, 0.3]

param_grid = create_param_grid(hidden_dims, latent_dims, dropout, ['relu'], ['glorot_uniform'], betas=beta)
cv = VAECrossValidator(param_grid, input_dim, 5, batch_size=128)

#%%
results = cv.cross_validate(train_data, epochs=epochs, verbose=0)

#%%
with open('outputs/CrossVal/cv_latent_10.pkl', 'wb') as file:
    pickle.dump(results, file)

#%%
# Cross Validation for 15 dimension latent space
latent_dims = [15]
beta = [1e-5, 1e-4, 1e-3]
hidden_dims = [[100, 100], [150, 150], [200, 200], [250, 250], [300, 300], [150, 100, 50], [200, 150, 100],
               [250, 200, 150], [300, 200, 100]]
epochs = 100

dropout = [0.1, 0.2, 0.3]

param_grid = create_param_grid(hidden_dims, latent_dims, dropout, ['relu'], ['glorot_uniform'], betas=beta)
cv = VAECrossValidator(param_grid, input_dim, 5, batch_size=128)

#%%
results = cv.cross_validate(train_data, epochs=epochs, verbose=0)

#%%
with open('outputs/CrossVal/cv_latent_15.pkl', 'wb') as file:
    pickle.dump(results, file)

#%%
# Cross Validation for 20 dimension latent space
latent_dims = [20]
beta = [1e-5, 1e-4, 1e-3]
hidden_dims = [[100, 100], [150, 150], [200, 200], [250, 250], [300, 300], [150, 100, 50], [200, 150, 100],
               [250, 200, 150], [300, 200, 100]]
epochs = 100

dropout = [0.1, 0.2, 0.3]

param_grid = create_param_grid(hidden_dims, latent_dims, dropout, ['relu'], ['glorot_uniform'], betas=beta)
cv = VAECrossValidator(param_grid, input_dim, 5, batch_size=128)

#%%
results = cv.cross_validate(train_data, epochs=epochs, verbose=0)

#%%
with open('outputs/CrossVal/cv_latent_20.pkl', 'wb') as file:
    pickle.dump(results, file)

#%%
# Cross Validation for 25 dimension latent space
latent_dims = [25]
beta = [1e-5, 1e-4, 1e-3]
hidden_dims = [[100, 100], [150, 150], [200, 200], [250, 250], [300, 300], [150, 100, 50], [200, 150, 100],
               [250, 200, 150], [300, 200, 100]]
epochs = 100

dropout = [0.1, 0.2, 0.3]

param_grid = create_param_grid(hidden_dims, latent_dims, dropout, ['relu'], ['glorot_uniform'], betas=beta)
cv = VAECrossValidator(param_grid, input_dim, 5, batch_size=128)

#%%
results = cv.cross_validate(train_data, epochs=epochs, verbose=0)

#%%
with open('outputs/CrossVal/cv_latent_25.pkl', 'wb') as file:
    pickle.dump(results, file)

#%%
# Cross Validation for 30 dimension latent space
latent_dims = [30]
beta = [1e-5, 1e-4, 1e-3]
hidden_dims = [[100, 100], [150, 150], [200, 200], [250, 250], [300, 300], [150, 100, 50], [200, 150, 100],
               [250, 200, 150], [300, 200, 100]]
epochs = 100

dropout = [0.1, 0.2, 0.3]

param_grid = create_param_grid(hidden_dims, latent_dims, dropout, ['relu'], ['glorot_uniform'], betas=beta)
cv = VAECrossValidator(param_grid, input_dim, 5, batch_size=128)

#%%
results = cv.cross_validate(train_data, epochs=epochs, verbose=0)

#%%
with open('outputs/CrossVal/cv_latent_30.pkl', 'wb') as file:
    pickle.dump(results, file)

#%%
# Plotting results

#%%
with open('outputs/CrossVal/cv_latent_5.pkl', 'rb') as file:
    cv_5 = pickle.load(file)

#%%
with open('outputs/CrossVal/cv_latent_10.pkl', 'rb') as file:
    cv_10 = pickle.load(file)

#%%
with open('outputs/CrossVal/cv_latent_15.pkl', 'rb') as file:
    cv_15 = pickle.load(file)

#%%

