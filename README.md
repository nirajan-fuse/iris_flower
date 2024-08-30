## Setup Instructions

### 1. Generate a Secret Key

To generate a secure secret key for your Flask application, you can use Python’s secrets module:

```python
import secrets

secret_key = secrets.token_hex(16)  # Generates a secure random secret key
print(secret_key)
```

### 2. Save secret key in .env file:
```.env
SECRET_KEY=<your_secret_key>
```

### 3. Run 'model_training.py' to train the model.
```terminal
python model_training.py
```

### 4. Use Docker Compose to build the Docker image and start the container:
```terminal
docker-compose up -d
```

#### 5. After the container is running, you can access the Flask application at:
```terminal
http://localhost:8000
```
