# CORS Configuration

## Overview
CORS (Cross-Origin Resource Sharing) has been configured to allow frontend applications running on common development ports to access the API.

## Allowed Origins
The following origins are whitelisted:
- `http://localhost:3000` - React (Create React App default)
- `http://localhost:5173` - Vite default port
- `http://localhost:5174` - Vite alternate port

## Configuration Details

### Settings
- **Allow Credentials**: `true` - Allows cookies and authorization headers
- **Allow Methods**: `*` - All HTTP methods (GET, POST, PUT, DELETE, PATCH, OPTIONS, etc.)
- **Allow Headers**: `*` - All headers including Authorization, Content-Type, etc.

### CORS Headers Returned
When a request is made from an allowed origin, the server returns:
```
access-control-allow-origin: http://localhost:3000
access-control-allow-credentials: true
access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
access-control-allow-headers: Authorization, Content-Type, etc.
access-control-max-age: 600
```

## Testing CORS

### Using cURL
```bash
# Test preflight request
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Authorization" \
     -X OPTIONS \
     http://localhost:8000/api/v1/github/search/users -v
```

### From Frontend (JavaScript)
```javascript
// Fetch with credentials
fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include', // Important for cookies
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
})
.then(response => response.json())
.then(data => console.log(data));

// Fetch with Authorization header
fetch('http://localhost:8000/api/v1/bookmarks/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  credentials: 'include'
})
.then(response => response.json())
.then(data => console.log(data));
```

### From Frontend (Axios)
```javascript
import axios from 'axios';

// Configure axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Use the API
api.post('/auth/login', { email, password })
  .then(response => {
    localStorage.setItem('token', response.data.access_token);
  });

api.get('/bookmarks/')
  .then(response => console.log(response.data));
```

## Adding More Origins

To add more allowed origins, edit `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:8080",  # Add new origin
        "https://yourdomain.com",  # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Production Considerations

For production deployment:

1. **Restrict Origins**: Only allow specific production domains
   ```python
   allow_origins=[
       "https://yourdomain.com",
       "https://www.yourdomain.com",
   ]
   ```

2. **Use Environment Variables**:
   ```python
   # In config.py
   CORS_ORIGINS: list = ["http://localhost:3000"]
   
   # In main.py
   allow_origins=settings.CORS_ORIGINS
   ```

3. **Consider Security**:
   - Don't use `allow_origins=["*"]` in production
   - Be specific with `allow_methods` if possible
   - Review `allow_headers` for security

## Troubleshooting

### CORS Error in Browser Console
```
Access to fetch at 'http://localhost:8000/api/v1/...' from origin 'http://localhost:3000' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

**Solutions:**
1. Ensure your frontend origin is in the `allow_origins` list
2. Restart the FastAPI server after changes
3. Check that you're using the correct port number
4. Clear browser cache

### Credentials Not Being Sent
Make sure to set:
- `credentials: 'include'` in fetch
- `withCredentials: true` in axios
- `allow_credentials=True` in CORS middleware

### Preflight Requests Failing
The server automatically handles OPTIONS requests. If failing:
1. Check that `allow_methods` includes the method you're using
2. Verify `allow_headers` includes your custom headers
3. Check server logs for errors

## Verification

CORS is working correctly if you see these headers in the response:
```
✓ access-control-allow-origin: http://localhost:3000
✓ access-control-allow-credentials: true
✓ access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
✓ access-control-allow-headers: Authorization
```

Server is running on: http://localhost:8000
