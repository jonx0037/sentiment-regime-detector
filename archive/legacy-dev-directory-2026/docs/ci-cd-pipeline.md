# CI/CD pipeline - Sentiment Regime Detector - YML

```yaml
name: CI/CD Pipeline - Sentiment Regime Detector

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Backend Testing & Build
  backend-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt
        pip install pytest pytest-cov pylint black
    
    - name: Lint with pylint
      run: |
        pylint backend/ --fail-under=8.0 || true
    
    - name: Format check with black
      run: |
        black --check backend/
    
    - name: Run tests with pytest
      run: |
        pytest backend/tests/ --cov=backend --cov-report=xml --cov-report=html
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      if: matrix.python-version == '3.11'
      with:
        file: ./coverage.xml
        flags: backend
        name: backend-coverage

  # Frontend Testing & Build
  frontend-test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      working-directory: ./frontend
      run: npm ci
    
    - name: Lint check
      working-directory: ./frontend
      run: npm run lint
    
    - name: Run tests
      working-directory: ./frontend
      run: npm test -- --coverage --watchAll=false
    
    - name: Build frontend
      working-directory: ./frontend
      run: npm run build
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./frontend/coverage/coverage-final.json
        flags: frontend
        name: frontend-coverage

  # Build and Push Docker Images
  build-and-push:
    needs: [backend-test, frontend-test]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write
    
    strategy:
      matrix:
        component: [backend, frontend]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-${{ matrix.component }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: ./${{ matrix.component }}
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-${{ matrix.component }}:buildcache
        cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-${{ matrix.component }}:buildcache,mode=max

  # Deploy to Kubernetes
  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'
    
    - name: Configure kubectl
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
    
    - name: Update image tags
      run: |
        cd k8s
        export IMAGE_TAG=main-${GITHUB_SHA::7}
        sed -i "s|IMAGE_TAG|${IMAGE_TAG}|g" backend-deployment.yaml
        sed -i "s|IMAGE_TAG|${IMAGE_TAG}|g" frontend-deployment.yaml
    
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/namespace.yaml
        kubectl apply -f k8s/configmap.yaml
        kubectl apply -f k8s/secrets.yaml
        kubectl apply -f k8s/backend-deployment.yaml
        kubectl apply -f k8s/backend-service.yaml
        kubectl apply -f k8s/frontend-deployment.yaml
        kubectl apply -f k8s/frontend-service.yaml
        kubectl apply -f k8s/ingress.yaml
    
    - name: Verify deployment
      run: |
        kubectl rollout status deployment/sentiment-backend -n sentiment-detector
        kubectl rollout status deployment/sentiment-frontend -n sentiment-detector
    
    - name: Run smoke tests
      run: |
        kubectl run smoke-test --image=curlimages/curl:latest --rm -i --restart=Never \
          -n sentiment-detector -- \
          curl -f http://sentiment-backend:8000/health || exit 1

  # Notification
  notify:
    needs: [deploy]
    runs-on: ubuntu-latest
    if: always()
    
    steps:
    - name: Send notification
      run: |
        if [ "${{ needs.deploy.result }}" == "success" ]; then
          echo "✅ Deployment successful!"
        else
          echo "❌ Deployment failed!"
        fi
```
