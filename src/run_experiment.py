from pathlib import Path
import json, numpy as np, matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score,f1_score,ConfusionMatrixDisplay
X,y=load_digits(return_X_y=True); novelty=(y==0).astype(int); idx=np.arange(len(y)); tr,te=train_test_split(idx,test_size=.35,random_state=42,stratify=novelty); normal_tr=tr[novelty[tr]==0]
m=IsolationForest(contamination=.10,random_state=42,n_estimators=350).fit(X[normal_tr]); score=-m.score_samples(X[te]); pred=(m.predict(X[te])==-1).astype(int); out={'roc_auc':float(roc_auc_score(novelty[te],score)),'f1':float(f1_score(novelty[te],pred)),'novel_digit':0,'n_test':int(len(te))}
Path('results').mkdir(exist_ok=True); Path('results/metrics.json').write_text(json.dumps(out,indent=2))
plt.figure(figsize=(7,5)); plt.hist(score[novelty[te]==0],bins=30,alpha=.7,label='normal'); plt.hist(score[novelty[te]==1],bins=20,alpha=.7,label='novel digit 0'); plt.xlabel('Anomaly score'); plt.ylabel('Count'); plt.title('Novelty-score distributions'); plt.legend(); plt.tight_layout(); plt.savefig('assets/03_data_or_model.png',dpi=150); plt.close()
fig,ax=plt.subplots(figsize=(6,5)); ConfusionMatrixDisplay.from_predictions(novelty[te],pred,ax=ax); ax.set_title('Thresholded novelty detection'); fig.tight_layout(); fig.savefig('assets/04_evaluation_or_results.png',dpi=150); plt.close(fig); print(json.dumps(out,indent=2))