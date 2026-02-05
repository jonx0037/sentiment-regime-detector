# Kubernetes Deployment Manifests

```yaml

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-cache-pvc
  namespace: sentiment-regime-detector
  labels:
    app: backend
    component: storage
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: sentiment-regime-detector
  labels:
    app: sentiment-regime-detector
data:
  # Model configurations
  FINBERT_MODEL: "ProsusAI/finbert"
  ROBERTA_MODEL: "cardiffnlp/twitter-roberta-base-sentiment"
  
  # Asset classes
  ASSET_CLASSES: "equities,crypto,forex,commodities"
  
  # Data sources
  DATA_SOURCES: "reddit,twitter,financial-news"
  
  # Date range
  DATA_START_DATE: "2016-01-01"
  
  # Regime detection settings
  REGIME_TYPES: "Risk-On,Transition,Risk-Off"
  SENTIMENT_THRESHOLD_HIGH: "0.6"
  SENTIMENT_THRESHOLD_LOW: "-0.6"
  
  # Update intervals
  SENTIMENT_UPDATE_INTERVAL: "300"  # 5 minutes
  REGIME_UPDATE_INTERVAL: "900"     # 15 minutes
  ```
  