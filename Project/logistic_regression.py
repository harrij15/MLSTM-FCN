# Adapted from https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8

import csv
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

# https://medium.datadriveninvestor.com/firths-logistic-regression-classification-with-datasets-that-are-small-imbalanced-or-separated-49d7782a13f1

#Define get_predictions function
def get_predictions(X,weights):
    z = np.dot(X,weights)
    y_pred =  1/(1 + np.exp(-z))
    return y_pred

def firth_logit(X,y,num_iter=5000,learning_rate=0.01):
    #Initialize weights
    weights = np.ones(X.shape[1])

    #Perform gradient descent
    for i in range(num_iter):

        y_pred = get_predictions(X,weights)

        #Calculate Fisher information matrix
        Xt = X.transpose()
        W = np.diag(y_pred*(1-y_pred))
        I = np.linalg.multi_dot([Xt,W,X])

        #Find diagonal of Hat Matrix
        sqrtW = W**0.5
        H = np.linalg.multi_dot([sqrtW,X,np.linalg.inv(I),Xt,sqrtW])
        hat_diag = np.diag(H)

        #Calculate U_star
        U_star = np.matmul((y -y_pred + hat_diag*(0.5 - y_pred)),X)

        #Update weights
        weights += np.matmul(np.linalg.inv(I),U_star)*learning_rate

    #Get final predictions
    y_pred =  get_predictions(X,weights)
    return y_pred

#!/usr/bin/env python
'''Python implementation of Firth regression by John Lees
See https://www.ncbi.nlm.nih.gov/pubmed/12758140'''

def firth_likelihood(beta, logit):
    return -(logit.loglike(beta) + 0.5*np.log(np.linalg.det(-logit.hessian(beta))))

# Do firth regression
# Note information = -hessian, for some reason available but not implemented in statsmodels
def fit_firth(y, X, start_vec=None, step_limit=1000, convergence_limit=0.0001):
    import statsmodels.api as sm
    logit_model = sm.Logit(y, X)

    if start_vec is None:
        start_vec = np.zeros(X.shape[1])

    beta_iterations = []
    beta_iterations.append(start_vec)
    for i in range(0, step_limit):
        pi = logit_model.predict(beta_iterations[i])
        W = np.diagflat(np.multiply(pi, 1-pi))
        var_covar_mat = np.linalg.pinv(-logit_model.hessian(beta_iterations[i]))

        # build hat matrix
        rootW = np.sqrt(W)
        H = np.dot(np.transpose(X), np.transpose(rootW))
        H = np.matmul(var_covar_mat, H)
        H = np.matmul(np.dot(rootW, X), H)

        # penalised score
        U = np.matmul(np.transpose(X), y - pi + np.multiply(np.diagonal(H), 0.5 - pi))
        new_beta = beta_iterations[i] + np.matmul(var_covar_mat, U)

        # step halving
        j = 0
        while firth_likelihood(new_beta, logit_model) > firth_likelihood(beta_iterations[i], logit_model):
            new_beta = beta_iterations[i] + 0.5*(new_beta - beta_iterations[i])
            j = j + 1
            if (j > step_limit):
                sys.stderr.write('Firth regression failed\n')
                return None

        beta_iterations.append(new_beta)
        if i > 0 and (np.linalg.norm(beta_iterations[i] - beta_iterations[i-1]) < convergence_limit):
            break

    return_fit = None
    if np.linalg.norm(beta_iterations[i] - beta_iterations[i-1]) >= convergence_limit:
        sys.stderr.write('Firth regression failed\n')
    else:
        # Calculate stats
        fitll = -firth_likelihood(beta_iterations[-1], logit_model)
        intercept = beta_iterations[-1][0]
        beta = beta_iterations[-1][1:].tolist()
        bse = np.sqrt(np.diagonal(np.linalg.pinv(-logit_model.hessian(beta_iterations[-1]))))

        return_fit = intercept, beta, bse, fitll

    return return_fit



if __name__ == "__main__":
    import random
    random.seed(10)

    use_logit = False
    smote = True

    # Set up data
    data = pd.read_csv('data.csv', header=0)
    data.astype({'Alert': 'float','Near Surface Air Temperature': 'float','Precipitation': 'float'})
    data = data.set_index('Date')
    data["Intercept"] = 1

    # Shuffle data
    data = data.sample(frac=1)

    # Define y and X
    #columns = ['Near Surface Air Temperature','Precipitation']
    #columns = ['Intercept','Near Surface Air Temperature','Precipitation']
    #columns = ['Intercept','Near Surface Air Temperature']
    columns = ['Intercept','Precipitation']

    assert((not use_logit and 'Intercept' in columns) or (use_logit))

    X = data[columns]
    y = data['Alert']

    X_columns = list(set(columns) - set(['Intercept']))

    # Oversampling
    if smote:
        from imblearn.over_sampling import SMOTE
        os = SMOTE(random_state=0)
        X,y=os.fit_resample(X, y)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    if use_logit:

        # Fit model
        logreg = LogisticRegression(class_weight='balanced')
        logreg.fit(X_train, y_train)

        # Evaluate model
        y_pred = logreg.predict(X_test)
        zeros = [x for x in y_pred if x == 0]
        print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

    else:

        # John Lees Firth implementation
        (intercept, beta, bse, fitll) = fit_firth(y_train,X_train)
        y_pred = []
        val_set = set()
        key = X_test.keys()[0]
        for i in range(len(X_test[key])):
            val = intercept
            for j in range(len(X_columns)):
                X_col = X_columns[j]
                x_val = list(X_test[X_col])[i]
                val = beta[j]*x_val
            val = 1/(1 + np.exp(-1*val))
            y_pred.append(int(val >= 0.5))

        # Compute F1 score
        from sklearn.metrics import f1_score
        print("F1 score:", f1_score(y_test,y_pred,average='binary'))

        # Wald test
        from scipy.stats import norm, chi2
        waldp = []
        beta = [intercept] + beta
        for beta_val, bse_val in zip(beta, bse):
            waldp.append(2 * (1 - norm.cdf(abs(beta_val/bse_val))))
        print(waldp)

        #print("# of ones in y_pred:",sum(y_pred))
        #print("# of ones in y_test:",sum(y_test))

        num_correct = 0
        one_correct = 0
        y_test = np.array(y_test)
        for i in range(len(y_pred)):
            if y_pred[i] == y_test[i]:
                if y_pred[i] + y_test[i] == 2:
                    one_correct += 1
                num_correct += 1

        #print("Test Accuracy:",num_correct/len(y_pred))
        #print("One Accuracy:",one_correct/sum(y_test))
        #zeros = [x for x in y_pred if x == 0]
        #print("Percentage of zeros in y_pred:",len(zeros)/len(y_pred))
        #zeros = [x for x in y_test if x == 0]
        #print("Percentage of zeros in y_test:",len(zeros)/len(y_test))

    # https://realpython.com/logistic-regression-python/
    # Confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    print('Confusion Matrix:\n', conf_matrix)

    # Produce heatmap of confusion matrix
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(conf_matrix)
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
    ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))

    # https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize('xx-large')
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize('xx-large')

    ax.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, conf_matrix[i, j], ha='center', va='center', color='red', fontsize='xx-large')
    plt.show()

    # Classification report
    report = classification_report(y_test, y_pred)
    print('Classification Report:\n', report)