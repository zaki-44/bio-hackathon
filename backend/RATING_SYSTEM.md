# Farmer Rating System

This document describes the farmer rating system that allows users to rate farmers from 1-5 stars.

## Database Model

### FarmerRating Model

- **farmer_id**: Foreign key to the farmer (User with user_type='farmer')
- **user_id**: Foreign key to the user who gave the rating
- **rating**: Integer from 1-5 (stars)
- **comment**: Optional text comment
- **created_at**: Timestamp when rating was created
- **updated_at**: Timestamp when rating was last updated
- **Unique constraint**: One user can only rate a farmer once (can update their rating)

## API Endpoints

### 1. Rate a Farmer

**POST** `/api/farmers/<farmer_id>/rate`

Submit or update a rating for a farmer.

**Authentication**: Required (session or JWT token)

**Request Body**:

```json
{
  "rating": 5,
  "comment": "Great quality products!"
}
```

**Response** (201 Created or 200 Updated):

```json
{
  "success": true,
  "message": "Rating submitted successfully",
  "rating": {
    "id": 1,
    "farmer_id": 2,
    "farmer_username": "farmer1",
    "user_id": 3,
    "user_username": "user1",
    "rating": 5,
    "comment": "Great quality products!",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

**Validation**:

- Rating must be between 1 and 5
- User cannot rate themselves
- Only farmers can be rated
- If user already rated, the rating is updated

### 2. Get Farmer Rating Information

**GET** `/api/farmers/<farmer_id>/rating`

Get comprehensive rating information for a farmer.

**Authentication**: Optional (if authenticated, includes user's own rating)

**Response**:

```json
{
  "success": true,
  "farmer_id": 2,
  "farmer_username": "farmer1",
  "average_rating": 4.5,
  "total_ratings": 10,
  "rating_distribution": {
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4
  },
  "user_rating": {
    "id": 1,
    "rating": 5,
    "comment": "Great quality!",
    "created_at": "2024-01-15T10:30:00"
  },
  "ratings": [
    {
      "id": 1,
      "user_username": "user1",
      "rating": 5,
      "comment": "Excellent!",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### 3. Get Farmer Ratings List (Paginated)

**GET** `/api/farmers/<farmer_id>/ratings?page=1&per_page=10`

Get paginated list of all ratings for a farmer.

**Query Parameters**:

- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 50)

**Response**:

```json
{
  "success": true,
  "farmer_id": 2,
  "farmer_username": "farmer1",
  "ratings": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3
  }
}
```

## User Model Updates

The `User` model now includes rating information for farmers:

- **`get_average_rating()`**: Calculates average rating for farmers
- **`get_rating_count()`**: Gets total number of ratings
- **`to_dict()`**: Now includes `average_rating` and `rating_count` for farmers

Example user dict for a farmer:

```json
{
  "id": 2,
  "username": "farmer1",
  "user_type": "farmer",
  "average_rating": 4.5,
  "rating_count": 10
}
```

## Usage Examples

### Submit a Rating

```python
import requests

response = requests.post(
    'http://localhost:5000/api/farmers/2/rate',
    json={
        'rating': 5,
        'comment': 'Amazing organic products!'
    },
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)
```

### Get Rating Information

```python
response = requests.get('http://localhost:5000/api/farmers/2/rating')
data = response.json()
print(f"Average rating: {data['average_rating']}")
print(f"Total ratings: {data['total_ratings']}")
```

## Frontend Integration

The rating system can be integrated into the frontend by:

1. Displaying average rating and count on farmer profiles
2. Showing a star rating component (1-5 stars) for users to submit ratings
3. Displaying rating distribution charts
4. Showing list of all ratings with comments

## Notes

- Users can update their rating by submitting a new rating (same endpoint)
- One user can only have one rating per farmer (enforced by unique constraint)
- Farmers cannot rate themselves
- Only authenticated users can submit ratings
- Rating information is publicly viewable
