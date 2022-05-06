## Functional Requirements

1. Login  - Minh
2. Logout - Anh
3. Create Account - Minh
4. Delete Account - Anh
5. \*Add Item Pictures - Jeff
6. Add User Ratings/Reviews - Jeff
   1. View User's Reviews
7. Add to Cart - Minh
8. Checkout - Jeff
9.  \*Advanced Search w/ Filters - Jeff
10. Add Items to Store (Seller Account) - Minh
11. Save for Laters / Lists - Jeff
12. Discount Period - Anh
13. Related Items - Minh

(Richard will be assigned to collaborate on or take over certain requirements at our next meeting.)

## Non-functional Requirements

1. \*Dynamic Interface - Jeff
2. Dark Mode - Anh
3. Sale/Discount Display - Anh
4. \*Multilingual - Minh + Anh + Jeff
5. Image Zoom? - Minh

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
  
### 2. Seller Account, Item Pictures
- **Pre-condition:** User has checked the box on their profile to label themsevlves as a seller.

- **Trigger:** User clicks button to add item to store (probably in a similar place to where the YouTube Upload Button is)

- **Primary Sequence:** (Add Item Form)
 
  1. Seller sets name, description
  2. Seller uploads image
  3. Seller sets price
  4. Seller can set categories for item
  5. Seller clicks submit
  6. Item is added to store
  
- **Primary Postconditions:**
  1. Item now appears in store and search results

- **Secondary Postconditions:**
  1. Seller's profile page will show seller rating that is an average of all their product ratings

- **Alternate Sequence:** 
  1. Seller can edit or remove their existing listings
  2. Seller is notified whne a purchase is made
  3. System tracks how much money seller has made

### 3. Add to Cart + Checkout

- **Trigger:** User adds item to cart

- **Primary Sequence:**
  
  1. Item is added to cart
  3. User can click checkout (on the cart page) to enter the purchase flow
  4. Website takes fake credit card info
  5. Purchase is made

- **Primary Postconditions:** 
  1. Item is in user's cart.
  2. Cart icon has a little red number showing how many icons in cart
  3. Seller is notified and "paid" after a purchase is made.

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
