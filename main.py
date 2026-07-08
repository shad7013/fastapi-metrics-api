import time
import uuid
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. STRICT CORS POLICY CONFIGURATION
# Only this specific origin is allowed to talk to our API.
origins = [
    "https://dash-sa3rmq.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CUSTOM MIDDLEWARE FOR REQUIRED HEADERS
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.time() # Start the timer
    
    response = await call_next(request) # Process the request
    
    process_time = time.time() - start_time # Calculate how long it took
    
    # Add the mandatory headers to the response
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

# 3. THE STATS ENDPOINT
@app.get("/stats")
async def get_stats(values: str = Query(..., description="Comma-separated list of integers")):
    # Convert the comma-separated string into a list of actual integers
    try:
        int_list = [int(x) for x in values.split(",")]
    except ValueError:
        return {"error": "Invalid input. Please provide comma-separated integers."}
    
    # Compute the descriptive statistics
    count = len(int_list)
    total_sum = sum(int_list)
    minimum = min(int_list)
    maximum = max(int_list)
    mean = total_sum / count if count > 0 else 0
    
    # Return the exact JSON structure required by the grader
    return {
        "email": "your-email@example.com", # Replace this with your actual logged-in email
        "count": count,
        "sum": total_sum,
        "min": minimum,
        "max": maximum,
        "mean": round(mean, 2)
    }