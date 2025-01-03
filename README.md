# Recommendation Engine for a Shop

This README provides instructions for building a recommendation engine using Python, modern technologies, and best practices. The engine integrates with a React-based frontend in the **Martix** app ecosystem, which includes:
- **Order Processing:** Built on Go
- **Product Catalog:** Built on Nest.js
- **Admin Panel:** Built on .NET

## Purpose
The recommendation engine enhances the shopping experience by suggesting products to users based on their preferences, interactions, and other behavioral patterns. It helps:

- **Increase Sales:** Personalized recommendations drive conversions.
- **Improve User Engagement:** Relevant suggestions keep users engaged longer.
- **Boost Retention:** Satisfied customers are more likely to return.
- **Optimize Inventory Management:** Highlight products with high relevance or low visibility.

## Features
- Personalized product recommendations.
- Content-based and collaborative filtering hybrid approach.
- Real-time API to serve recommendations to the frontend.

## How It Works
### Recommendation Logic
The engine operates on:
1. **Collaborative Filtering:**
   - Based on user-item interactions (e.g., purchases, ratings).
   - Identifies patterns in user behavior and similarities between users or products.

2. **Content-Based Recommendations:**
   - Analyzes product attributes like categories, descriptions, or tags.
   - Matches user preferences with product features.

3. **Hybrid Approach:** Combines collaborative filtering and content-based methods for better accuracy.

### Data Flow
1. **User Interactions:** From the **Order Processing Module (Go)**
   - Purchase history, product views, and ratings.

2. **Product Metadata:** From the **Product Catalog Module (Nest.js)**
   - Product descriptions, categories, and tags.

3. **Administrative Input:** From the **Admin Panel (ASP.NET)**
   - Manage feature weights, fine-tune algorithms, and retrain models.

## Required Data
### From Modules
- **Order Processing:**
  - User activity logs: `user_id`, `product_id`, `timestamp`, `action_type` (view, purchase, etc.).

- **Product Catalog:**
  - Product details: `product_id`, `name`, `category`, `tags`, `price`, etc.

- **Admin Panel:**
  - Settings for model tuning: `parameter_name`, `value`.

### Preprocessed Data for Training
- User-item interaction matrix (e.g., ratings or purchase frequencies).
- Product feature vectors (e.g., categories, tags).

## Synchronization
### Data Sync Between Modules
- **Kafka:**
  - Real-time streaming of user interactions from Order Processing to the Recommendation Engine.
  - Synchronize product catalog updates from Nest.js.

- **Database:**
  - Shared PostgreSQL or MongoDB for consistent access to interaction and product data.

### Example Kafka Topics
- `user-interactions`: Logs user actions like purchases or views.
- `product-updates`: Updates product catalog details.
- `admin-commands`: Admin-triggered tasks like retraining models.

## Recommendation Generation
1. **Training:**
   - Train on historical data for collaborative filtering and feature extraction.
   - Fine-tune parameters with feedback from the admin module.

2. **Serving Recommendations:**
   - For a given `user_id`, the engine:
     - Retrieves similar users or products.
     - Scores and ranks products based on relevance.
     - Returns top `N` recommendations.

3. **Real-Time API:**
   - The FastAPI server processes requests and fetches recommendations dynamically.

---

## Technologies and Tools
### Backend (Recommendation Engine)
- **Programming Language:** Python
- **Frameworks/Libraries:**
  - **Data Handling:** `pandas`, `numpy`
  - **Machine Learning:** `scikit-learn`, `surprise`, `tensorflow`
  - **Model Deployment:** `FastAPI`
  - **Data Storage:** PostgreSQL (or MongoDB for NoSQL)
  - **Message Queue:** Apache Kafka (for communication with other modules)

### Frontend (React Integration)
- Use Axios or Fetch API for communication with the backend.
- Display recommendations in the Product Detail or Home Page components.

## Architecture Overview
```
+-------------------+      +------------------+      +-------------------+      +------------------+
| Recommendation   |<---->| Product Catalog  |<---->| Order Processing  |<---->| Admin Panel      |
| Engine (Python)  |      | (Nest.js)        |      | (Go)              |      | (.NET)           |
+-------------------+      +------------------+      +-------------------+      +------------------+
         |                              Frontend (React-based mARTIX App)
         +----------------------------------------------------------------+
```

## Setting Up the Recommendation Engine

### 1. Install Dependencies

```bash
# Create a virtual environment
python -m venv recommendation-engine
source recommendation-engine/bin/activate  # On Windows: recommendation-engine\Scripts\activate

# Install required packages
pip install pandas numpy scikit-learn surprise fastapi uvicorn tensorflow psycopg2 kafka-python
```

### 2. Data Preparation
- **Input Data:** Collect user interactions (e.g., purchases, ratings) and product details (e.g., categories, descriptions).
- **Preprocessing:**
  - Convert raw data into a user-item interaction matrix.
  - Normalize ratings.

Example Code:

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load data
interactions = pd.read_csv('user_interactions.csv')
products = pd.read_csv('products.csv')

# Split into training and testing sets
train_data, test_data = train_test_split(interactions, test_size=0.2, random_state=42)
```

### 3. Training the Model
Use collaborative filtering and content-based features.

```python
from surprise import SVD, Dataset, Reader
from surprise.model_selection import cross_validate

# Prepare data for Surprise library
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(train_data[['user_id', 'product_id', 'rating']], reader)

# Train an SVD model
model = SVD()
cross_validate(model, data, cv=5, verbose=True)

# Train on the full dataset
trainset = data.build_full_trainset()
model.fit(trainset)

# Save the model
import pickle
with open('recommendation_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

### 4. API for Recommendations
Expose a FastAPI endpoint to serve recommendations.

```python
from fastapi import FastAPI
import pickle
import pandas as pd

app = FastAPI()

# Load model
with open('recommendation_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    # Generate recommendations
    predictions = [
        (iid, model.predict(user_id, iid).est)
        for iid in products['product_id'].unique()
    ]
    recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:10]
    return {"user_id": user_id, "recommendations": recommendations}

# Run the server
# uvicorn main:app --reload
```

### 5. Communication with Frontend
1. Use Axios in React to fetch recommendations:

```javascript
import axios from 'axios';

const fetchRecommendations = async (userId) => {
  try {
    const response = await axios.get(`/api/recommend/${userId}`);
    return response.data.recommendations;
  } catch (error) {
    console.error("Error fetching recommendations", error);
  }
};
```

2. Display recommendations in a component:

```javascript
import React, { useEffect, useState } from 'react';

const Recommendations = ({ userId }) => {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const getRecommendations = async () => {
      const data = await fetchRecommendations(userId);
      setRecommendations(data);
    };
    getRecommendations();
  }, [userId]);

  return (
    <div>
      <h3>Recommended Products</h3>
      <ul>
        {recommendations.map((rec) => (
          <li key={rec[0]}>{`Product ID: ${rec[0]}, Score: ${rec[1]}`}</li>
        ))}
      </ul>
    </div>
  );
};

export default Recommendations;
```


### 6. Integration with mARTIX Modules
- **Product Catalog (Nest.js):** Provide metadata for product features and categories.
- **Order Processing (Go):** Send user purchase data to the recommendation engine via Kafka.
- **Admin Panel (.NET):** Allow admins to fine-tune model parameters or retrain models.

### 7. Deployment
- **Backend:** Deploy the FastAPI server on Docker or Kubernetes.
- **Frontend:** Integrate the React component into the mARTIX app.
- **Inter-Module Communication:** Use Kafka topics for message passing between modules.

```yaml
# Example Docker Compose for the Recommendation Engine
version: '3.8'
services:
  recommendation:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db/recommendations
  db:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

## Summary
This recommendation engine uses modern technologies like FastAPI, collaborative filtering (Surprise library), and integrates seamlessly with mARTIX modules via REST and Kafka. It ensures real-time, personalized product recommendations, enhancing the shopping experience for users.
