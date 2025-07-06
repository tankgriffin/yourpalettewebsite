# Your Palette - Korean Makeup Tools E-commerce Store

A dynamic Flask web application for selling premium Korean makeup tools and accessories.

## Overview

Your Palette is a full-featured e-commerce website built with Flask that allows customers to browse, search, and purchase Korean makeup tools. The application includes a complete shopping experience from product browsing to order completion.

## Features

### Customer-Facing Features
- **Product Browsing**: View all available products with detailed information
- **Search Functionality**: Text-based search across product names and descriptions
- **Product Categories**: Browse by categories (Palettes, Spatulas, Lip Tools, Accessories)
- **Product Details**: Detailed product pages with specifications and related products
- **Shopping Basket**: Add/remove items with quantity management
- **Checkout Process**: Complete order form with customer information
- **Order Confirmation**: Order summary and confirmation page

### Technical Features
- **Responsive Design**: Bootstrap 4.6 with custom CSS
- **Database Integration**: SQLite database with SQLAlchemy ORM
- **Form Handling**: Flask-WTF for secure form processing
- **Session Management**: Shopping basket persistence across pages
- **Flash Messages**: User feedback for all actions
- **Template Inheritance**: Modular template structure

## Technology Stack

- **Backend**: Python Flask 2.3.3
- **Database**: SQLite with Flask-SQLAlchemy 3.0.5
- **Forms**: Flask-WTF 1.1.1 with WTForms 3.0.1
- **Frontend**: HTML5, CSS3, Bootstrap 4.6, JavaScript
- **Icons**: Font Awesome 6.0
- **Validation**: Email-validator 2.0.0

## Database Schema

### Products Table
- `id` (Primary Key)
- `name` (String, 100 chars)
- `description` (Text)
- `price` (Decimal, 10,2)
- `image_url` (String, 200 chars)
- `stock_quantity` (Integer)
- `category` (String, 50 chars)
- `brand` (String, 50 chars)

### Orders Table
- `id` (Primary Key)
- `customer_name` (String, 100 chars)
- `customer_email` (String, 120 chars)
- `customer_phone` (String, 20 chars)
- `customer_address` (Text)
- `order_date` (DateTime)
- `total_amount` (Decimal, 10,2)

### Order_Details Table
- `id` (Primary Key)
- `order_id` (Foreign Key → Orders.id)
- `product_id` (Foreign Key → Products.id)
- `quantity` (Integer)
- `price` (Decimal, 10,2)

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone/Download the project files**
   ```bash
   # Navigate to the project directory
   cd "YourPalette Assignment base"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to `http://127.0.0.1:5000`

## Application Structure

```
YourPalette Assignment base/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── ACCEPTANCE_CRITERIA.md # Detailed acceptance criteria
├── yourpalette.db        # SQLite database (created automatically)
├── static/               # Static files
│   ├── css/
│   │   └── styles.css    # Custom CSS styles
│   └── img/              # Product images
│       ├── makeup-palette.jpg
│       ├── korean-spatula.jpg
│       ├── mini-palette.jpg
│       ├── lip-kit.jpg
│       ├── led-mirror.jpg
│       └── hero-bg.jpg
└── templates/            # Flask templates
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── product_detail.html # Product details page
    ├── basket.html       # Shopping basket
    ├── checkout.html     # Checkout form
    └── order_confirmation.html # Order confirmation
```

## Usage Guide

### For Customers

1. **Browse Products**: Visit the homepage to see all available products
2. **Search**: Use the search bar to find specific products
3. **View Details**: Click "View Details" on any product for more information
4. **Add to Basket**: Select quantity and click "Add to Basket"
5. **Manage Basket**: View basket by clicking the basket icon in navigation
6. **Checkout**: Click "Proceed to Checkout" and fill in your details
7. **Confirmation**: Receive order confirmation with order number

### Sample Data

The application comes pre-loaded with 5 sample products:
- Professional Makeup Mixing Palette ($18.99)
- Korean Spatula ($24.99)
- Mini Palette ($12.50)
- Lip Kit ($15.75)
- LED Compact Mirror ($32.00)

## Features Implemented

### ✅ Required Features (Assignment Brief)
- [x] Customer landing page with search functionality
- [x] Item detail page with product information
- [x] Shopping basket with view/delete capabilities
- [x] Checkout page with customer details form
- [x] Three database tables (Products, Orders, Order_Details)
- [x] Flask Templates with Bootstrap CSS
- [x] Flask WTForms for form handling
- [x] Flask SQLAlchemy for database operations

### ✅ Additional Features
- [x] Responsive design for mobile devices
- [x] Product categories and filtering
- [x] Quantity management in basket
- [x] Flash messages for user feedback
- [x] Order confirmation page
- [x] Product image gallery
- [x] Related products suggestions
- [x] Session-based basket persistence

## Development Notes

### Design Decisions
- **Single-file Architecture**: All models, forms, and routes in `app.py` for simplicity
- **Session-based Basket**: Shopping basket stored in Flask sessions for user convenience
- **Bootstrap Integration**: Leveraged existing CSS from Assignment 1
- **Form Validation**: Comprehensive client and server-side validation

### Security Considerations
- CSRF protection enabled via Flask-WTF
- SQL injection prevention through SQLAlchemy ORM
- Input validation and sanitization
- Secure session management

## Testing

### Manual Testing Checklist
- [x] Homepage loads with products displayed
- [x] Search functionality works correctly
- [x] Product detail pages accessible
- [x] Add to basket functionality
- [x] Basket view and item removal
- [x] Checkout form validation
- [x] Order completion and confirmation
- [x] Database persistence of orders
- [x] Responsive design on mobile devices

### Sample Test Scenarios
1. **Product Search**: Search for "palette" should return 2 results
2. **Add to Basket**: Adding items should update basket counter
3. **Checkout**: Form should validate all required fields
4. **Order Creation**: Successful checkout should create database records

## Troubleshooting

### Common Issues

1. **Database Not Found Error**
   ```
   Solution: Run the app once to auto-create the database
   ```

2. **Template Not Found Error**
   ```
   Solution: Ensure templates/ directory exists with all HTML files
   ```

3. **Static Files Not Loading**
   ```
   Solution: Check static/ directory structure and file paths
   ```

4. **Form Validation Errors**
   ```
   Solution: Ensure Flask-WTF and email-validator are installed
   ```

## Submission Information

### Assignment 2 Deliverables
- **Part A**: Complete Flask application (this project)
- **Part B**: 5-minute video demonstration

### Key Implementation Points
- ✅ HTML and Bootstrap CSS implementation
- ✅ Flask Templates with dynamic content
- ✅ Flask WTForms for all user input
- ✅ Flask SQLAlchemy with three required tables
- ✅ Well-commented code with documentation
- ✅ No unexpected dependencies

## Future Enhancements

Potential improvements for future versions:
- User authentication and accounts
- Admin dashboard for product management
- Payment gateway integration
- Order tracking system
- Email notifications
- Product reviews and ratings
- Inventory management
- Multi-image product galleries

## Author

Created for IFQ557 Rapid Web Development - Assignment 2
Queensland University of Technology (QUT)

## License

This project is created for educational purposes as part of university coursework.