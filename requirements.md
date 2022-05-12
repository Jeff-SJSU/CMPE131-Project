## Functional Requirements

1. [x] Login  - Minh
2. [x] Logout - Anh
3. [x] Create Account - Minh
4. [x] Delete Account - Anh
5. [x] User Profile
   1. [x] User Pictures
6. [x] \*Add Item Pictures - Jeff
7. [ ] Add User Ratings/Reviews - Jeff
   1. [x] View User's Reviews
8. [x] Add to Cart - Minh
9. [x] Checkout - Jeff
10. [ ] \*Advanced Search w/ Filters - Jeff
11. [x] Add Items to Store (Seller Account)
12. [x] Save for Laters / Lists - Jeff
13. [ ] Discount Period - Anh
14. [ ] Related Items - Minh

(Richard will be assigned to collaborate on or take over certain requirements at our next meeting.)

## Non-functional Requirements

1. \*Dynamic Interface - Jeff
2. Dark Mode - Anh
3. Sale/Discount Display - Anh
4. \*Multilingual - Minh + Anh + Jeff
5. Image Zoom? - Minh

## Use Cases

### 1. Leave a review for a purchased item
- **Pre-condition:** User is logged in and has previously purchased an item.

- **Trigger:** User visits product page and clicks on a rating out of 5 stars.

- **Primary Sequence:** 
  1. Product average rating is updated based on user's rating.
  2. Page shows how many ratings of each # of stars were given.
  3. User's profile now contains ratings they've left

- **Primary Postconditions:** N/A

- **Alternate Sequence:** 
  1. User clicks button to delete their review
  2. Product stats is updated to remove their review.
  
  
### 2, Become a seller on the store.

- **Pre-condition:** User is logged in.
- **Trigger:** User clicks checkbox on their profile page to label themselves as a seller.
- **Primary Sequence:**
  1. User's profile is updated to show they are a seller
  2. User can now add items to the store via a button on the navbar.
  3. Seller's profile page will show seller rating that is an average of all their product ratings

### 3. Add item to store.
- **Pre-condition:** User is logged in and is a seller account.

- **Trigger:** User (Seller) clicks button on the navbar to add item to store

- **Primary Sequence:** (Add Item Form)
 
  1. Seller sets name, description
  2. Seller uploads image
  3. Seller sets price
  4. Seller can set categories for item
  5. Seller clicks submit
  6. Item is added to store
  
- **Primary Postconditions:**
  1. Item now appears in store and search results

- **Alternate Sequence:** 
  1. Seller can edit or remove their existing listings from the product page
  2. Seller is notified when a purchase is made
  3. System tracks how much money seller has made from their account page

### 4. Add to Cart + Checkout

- **Primary Precondition**: User is logged in and viewing a product.
- **Trigger:** User clicks button to add item to cart

- **Primary Sequence:**
  1. Item is added to cart
  3. User can click checkout (on the cart page) to enter the purchase flow
  4. Website takes fake credit card info, does not store
  5. Purchase is made

- **Primary Postconditions:** 
  1. Item is in user's cart.
  2. Cart icon has a little red number showing how many icons in cart
  3. Seller is notified and "paid" after a purchase is made.

- **Alternate Sequence:**
  1. User can remove items from cart or edit quantity
  2. User can cancel an order up to an hour after purchase

### 5. Discount Period
- **Pre-condition:** Seller has an item in their store.

- **Trigger:** Seller sets a discount and (optionally) specifies an expiration time.

- **Primary Sequence:**
  1. Item page now displays discount and time remaining
  2. Price of item is temporarily updated

- **Primary Postconditions:** Discount expires after certain period of time.

### 6. Add item to list (Save for Later).
- **Primary Precondition:** User is logged in and viewing a product page.
- **Trigger:** User clicks button to add item to list (wishlist, save for later)

- **Primary Sequence:**
  1. Item is added to user's list on their profile
  2. User can browse/buy items from their list or buy an entire list
  3. User is notified that item was added to list and can see that on the product page.
 
- **Postconditions**:
  1. List shows items that are discounted
  2. List shows if item on list has been removed from the store
  
- **Alternate Sequence:** 
  1. User can create or delete lists
  2. User can save entire cart as a list

### 6. Perform Advanced Search w/ Filters

- **Precondition:** None.
- **Trigger:**
  1. User (optionally) picks category in dropdown next to search bar
  2. User enters terms in the search bar.
  
- **Primary Sequence:**
  
  1. Search results are returned for items that match
  2. Matches can be in name or description
  3. Items must have category if one has been selected

- **Alternate Sequence:**
  
  1. User can filter by price range
  2. User can narrow down search results by more tags?
