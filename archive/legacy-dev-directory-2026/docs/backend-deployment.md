# backend-deployment - yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentiment-backend
  namespace: sentiment-app
  labels:
    app: sentiment-backend
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentiment-backend
  template:
    metadata:
      labels:
        app: sentiment-backend
        version: v1
    spec:
      containers:
      - name: backend
        image: ghcr.io/your-username/sentiment-backend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        
        env:
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: sentiment-app-config
              key: BACKEND_PORT
        - name: MODEL_NAME
          valueFrom:
            configMapKeyRef:
              name: sentiment-app-config
              key: MODEL_NAME
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: sentiment-app-config
              key: LOG_LEVEL
        
        # Secrets
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: sentiment-app-secrets
              key: DATABASE_URL
        - name: REDDIT_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: sentiment-app-secrets
              key: REDDIT_CLIENT_ID
        - name: REDDIT_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: sentiment-app-secrets
              key: REDDIT_CLIENT_SECRET
        - name: TWITTER_BEARER_TOKEN
          valueFrom:
            secretKeyRef:
              name: sentiment-app-secrets
              key: TWITTER_BEARER_TOKEN
        - name: NEWS_API_KEY
          valueFrom:
            secretKeyRef:
              name: sentiment-app-secrets
              key: NEWS_API_KEY
        
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        volumeMounts:
        - name: model-cache
          mountPath: /app/models
        - name: data-storage
          mountPath: /app/data
      
      volumes:
      - name: model-cache
        emptyDir:
          sizeLimit: 10Gi
      - name: data-storage
        persistentVolumeClaim:
          claimName: sentiment-data-pvc
      
      # Affinity rules for better distribution
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - sentiment-backend
              topologyKey: kubernetes.io/hostname

---
apiVersion: v1
kind: Service
metadata:
  name: sentiment-backend-service
  namespace: sentiment-app
  labels:
    app: sentiment-backend
spec:
  type: ClusterIP
  selector:
    app: sentiment-backend
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
    name: http
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```
