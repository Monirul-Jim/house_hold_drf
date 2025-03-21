# Household Service Providing Platform

## Base URL

```
http://your-api-domain.com/api/
```

---

## 1️⃣ User Authentication

### 🔹 Register User

**Endpoint:** `/auth/users/`  
**Method:** `POST`  
**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

### 🔹 Login User

**Endpoint:** `/auth/jwt/create/`  
**Method:** `POST`  
**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "refresh": "your-refresh-token",
  "access": "your-access-token"
}
```

---

## 2️⃣ Admin Creation

### 🔹 Promote User to Admin

**Endpoint:** `/promote-admin/`  
**Method:** `POST`  
**Headers:** `Authorization: JWT <access_token>`  
**Request Body:**

```json
{
  "email": "newadmin@example.com"
}
```

**Response:**

```json
{
  "message": "User promoted to admin"
}
```

---

## 3️⃣ Client Profile

### 🔹 Get Profile

**Endpoint:** `/client-profile/`  
**Method:** `GET`  
**Headers:** `Authorization: JWT <access_token>`  
**Response:**

```json
{
  "user": 1,
  "bio": "I love household services!",
  "social_media_links": {}
}
```

### 🔹 Update Profile

**Endpoint:** `/client-profile/`  
**Method:** `PUT`  
**Headers:** `Authorization: JWT <access_token>`  
**Request Body:**

```json
{
  "bio": "Updated bio here.",
  "social_media_links": { "twitter": "https://twitter.com/example" }
}
```

**Response:**

```json
{
  "user": 1,
  "bio": "Updated bio here.",
  "social_media_links": { "twitter": "https://twitter.com/example" }
}
```

### 🔹 Upload Profile Picture

**Endpoint:** `/client-profile/<user_id>/image/`  
**Method:** `POST`  
**Headers:** `Authorization: JWT <access_token>`  
**Form Data:**

```json
{
  "profile_picture": "image.jpg"
}
```

**Response:**

```json
{
  "profile_picture": "https://cloudinary.com/path-to-image.jpg"
}
```

---

## 4️⃣ Add to Cart

### 🔹 Add Service to Cart

**Endpoint:** `/cart/add/<service_id>/`  
**Method:** `POST`  
**Headers:** `Authorization: JWT <access_token>`  
**Response:**

```json
{
  "message": "Service added to cart"
}
```

### 🔹 Remove Service from Cart

**Endpoint:** `/cart/remove/<service_id>/`  
**Method:** `DELETE`  
**Headers:** `Authorization: JWT <access_token>`  
**Response:**

```json
{
  "message": "Service removed from cart"
}
```

---

## 5️⃣ Orders

### 🔹 Place Order

**Endpoint:** `/orders/`  
**Method:** `POST`  
**Headers:** `Authorization: JWT <access_token>`  
**Response:**

```json
{
  "id": 1,
  "total_price": 150.0,
  "services": [
    { "name": "Home Cleaning", "price": 50.0 },
    { "name": "House Shifting", "price": 100.0 }
  ],
  "created_at": "2025-03-21T12:00:00Z"
}
```

### 🔹 View Orders

**Endpoint:** `/orders/`  
**Method:** `GET`  
**Headers:** `Authorization: JWT <access_token>`  
**Response:**

```json
[
  {
    "id": 1,
    "total_price": 150.0,
    "services": ["Home Cleaning", "House Shifting"],
    "created_at": "2025-03-21T12:00:00Z"
  }
]
```

---

## 6️⃣ Reviews & Ratings

### 🔹 Leave a Review

**Endpoint:** `/reviews/`  
**Method:** `POST`  
**Headers:** `Authorization: JWT <access_token>`  
**Request Body:**

```json
{
  "service": 1,
  "rating": 5,
  "comment": "Great service!"
}
```

**Response:**

```json
{
  "id": 1,
  "service": 1,
  "rating": 5,
  "comment": "Great service!",
  "created_at": "2025-03-21T12:00:00Z"
}
```

### 🔹 View Reviews

**Endpoint:** `/reviews/`  
**Method:** `GET`  
**Response:**

```json
[
  {
    "service": "Home Cleaning",
    "rating": 5,
    "comment": "Amazing!"
  }
]
```

---

## 7️⃣ Deployment

- **Hosting Platform:** `Vercel`
- **Database:** `PostgreSQL`
- **Media Storage:** `Cloudinary`

### 🔗 API Documentation

[Postman Collection](https://example.com/postman-collection)

---

### 🚀 Project By: **Team Household Services**
