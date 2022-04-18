## Functional Requirements

1. Login
2. Logout
3. Create Account
4. Delete Account
5. \*Item Pictures
6. User Ratings + Profiles
7. Add to Cart
8. Checkout
9. \*Advanced Search w/ Filters
10. Seller Account
11. Save for Laters / Lists
12. Discount Period
13. Related Items

## Non-functional Requirements

1. \*Dynamic Interface
2. Dark Mode
3. Sale/Discount Display
4. \*Multilingual
5. Image Zoom?

## Use Cases

### 1. User Ratings + Profiles
- **Pre-condition:** User has purchased an item.

- **Trigger:** User leaves a rating out of 5 stars.

- **Primary Sequence:** 
  1. Product average rating is updated based on user's rating.
  2. Page shows how many ratings of each # of stars were given.
  3. User's profile contains ratings they've left

- **Primary Postconditions:** N/A

- **Alternate Sequence:** 
  1. User delete's their review
  2. Product stats is updated to remove their review.

- **Alternate Sequence <optional>:** 
  1. User can upload profile image and change their name
  
### 2. Seller Account
- **Pre-condition:** User enables checkbox on their profile to label themsevlves as a seller.

- **Trigger:** User opens form to upload a new item

- **Primary Sequence:**
  
  1. User sets name, description
  2. User uploads image
  3. User sets price
  4. Seller can set categories for item
  5. Item is added to store
  
- **Primary Postconditions:** 
  1. User's profile now contains a seller rating that's an average of all their product ratings

- **Alternate Sequence:** 
  1. Seller can edit or remove existing listings
  2. Seller is notified whne a purchase is made
  3. System tracks how much money seller has made

### 3. Add to Cart + Checkout

- **Trigger:** User adds item to cart

- **Primary Sequence:**
  
  1. Item is added to cart
  2. User can click checkout to enter the purchase flow
  3. Website takes fake credit card info
  4. Purchase is made

- **Primary Postconditions:** 
  1. Item is in user's cart.
  2. Seller is notified and "paid" after a purchase is made.

- **Alternate Sequence:**
  1. User can remove items from cart or edit quantity
  2. User can cancel an order up to an hour after purchase

### 4. Discount Period
- **Pre-condition:** Seller has an item in their store.

- **Trigger:** Seller sets a discount and (optionally) specifies an expiration time.

- **Primary Sequence:**
  
  1. Item page now displays discount and time remaining
  2. Price of item is temporarily updated

- **Primary Postconditions:** Discount expires after certain period of time.

### 5. Save for Later + Lists
  
- **Trigger:** User adds item to list (wishlist, save for later)

- **Primary Sequence:**
  
  1. Item is added to user's list on their profile
  2. User can browse/buy items from their list or buy an entire list
 
- **Postconditions**:
  1. List shows items that are discounted
  2. List shows if item on list has been removed from the store
  
- **Alternate Sequence:** 
  1. User can create or delete lists
  2. User can save entire cart as a list

### 6. Advanced Search w/ Filters

- **Trigger:**
  1. User picks category in search bar
  2. User enters terms in the search bar.
  
- **Primary Sequence:**
  
  1. Search results are returned for items that match
  2. Matches can be in name or description
  3. Items must have category if one has been selected

- **Alternate Sequence:**
  
  1. User can filter by price range
  2. User can narrow down search results by more tags?
