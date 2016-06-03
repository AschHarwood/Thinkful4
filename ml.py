from sklearn.cross_validation import KFold
from sklearn.metrics import mean_squared_error

def kf_data(df):
    kf = KFold(len(df), n_folds=10)
    for train, test in kf:
        print("%s %s" % (train, test))
    return kf

def run_model(train, test):
   poly_1 = smf.ols(formula='y ~ 1 + X', data=x_train, y_train).fit()
   pred = poly_1.predict(test_df)
   actual = np.array(test_df['y'].tolist())

   mse = mean_squared_error(actual,pred)
   return mse

def main():
   df = make_df()
   for tr, tst in kf_data(df):
   	  train_df = evaluate_df with index = tr
   	  test_df = evaluate_df with index = tst
      run_model(tr_dt, tst_df)

   # run_model(df[:2], df[8])
