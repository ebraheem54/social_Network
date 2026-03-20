# Django Social Network Application

## Overview
A full-stack social networking platform built with Django, featuring modern UI/UX, user authentication, and comprehensive profile management capabilities.

## Features
- 👤 User registration and authentication system
- 📝 User profiles with bio and profile pictures
- 📱 Post creation with captions and media upload
- ⚙️ Account settings to update profile information
- 📄 Pagination on profile pages (2 posts per page)
- 🔍 Search functionality to find and discover friends
- 👥 Follow/unfollow system for user connections

## Project Structure
```
socialNetworkApp/
├── core/                      # Main application
│   ├── models.py             # User and Post models
│   ├── views.py              # Authentication and CRUD operations
│   ├── forms.py              # Custom signup form
│   └── urls.py               # URL routing
├── socialNetworkApp/          # Project settings
│   ├── settings.py           # Django configuration
│   └── urls.py               # Main URL configuration
├── Templates/                 # HTML templates
├── Static/                    # Static files and media uploads
└── manage.py                  # Django management script
```

## Technology Stack
- **Framework:** Django 5.0.0
- **Forms:** django-crispy-forms 2.1 with Bootstrap 4
- **Image Handling:** Pillow 10.1.0
- **Environment:** python-dotenv 1.0.0
- **Database:** SQLite
- **Production Server:** Gunicorn 21.2.0
- **Python Version:** 3.11+

## Design & UI
The application features a modern, professional UI with:
- **Custom CSS Framework** - Professional gradient-based design system
- **Responsive Layouts** - Mobile-friendly cards and components
- **Modern Color Scheme** - Blue primary color (#2563eb) with accent colors
- **Smooth Animations** - Hover effects and transitions on all interactive elements
- **Professional Typography** - Clean, modern font stack with proper hierarchy
- **Card-Based Design** - Beautiful shadow effects and rounded corners
- **Gradient Backgrounds** - Modern gradient backgrounds throughout
- **Form Optimization** - Professional form inputs with focus states
- **Font Awesome Icons** - Enhanced UX with icon integration

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/ebraheem54/social_Network.git
cd social_Network/socialNetworkApp
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Project Architecture
This is a standard Django application following the **MVT (Model-View-Template)** pattern:
- **Models**: Define User and Post data structures
- **Views**: Handle request/response logic for authentication and CRUD operations
- **Templates**: Render dynamic HTML pages with professional UI
- **Static Files**: Custom CSS framework, JavaScript, and user-uploaded media

## Key Pages
- **Login Page**: Clean form card with modern design
- **Signup Page**: Professional registration form with gradients
- **Profile Page**: Card-based profile display with user stats
- **Account Settings**: Modern settings form with image preview
- **New Post**: Clean post creation interface with media upload
- **Navigation**: Modern navbar with search functionality

## Database Schema
- **User Model**: Extended Django user with profile picture and bio
- **Post Model**: User posts with captions, images, and timestamps

 
### Recent Updates
- **Friend Search & Social Features**
  - Added search functionality to find and discover friends
  - Implemented follow/unfollow system for user connections
  - Enhanced social interaction capabilities
- Template optimization and design refinement
- Removed inline styles, moved to CSS classes
- Improved HTML structure and semantic markup
- Enhanced pagination with better UI and accessibility
- Added accessibility attributes (aria-label, aria-hidden)
- Consistent responsive design across all pages
 

### Best Practices Implemented
- Clean separation of concerns (MVT pattern)
- Responsive design for all screen sizes
- Accessibility-first approach
- Professional form validation and error handling
- Secure authentication and authorization

## License
This project is open source and available for educational purposes.

## Author
**Ebraheem Wannous**
- GitHub: [@ebraheem54](https://github.com/ebraheem54)
- Portfolio: [ebraheem-wannous.vercel.app](https://ebraheem-wannous.vercel.app/)

## Contributing
Contributions, issues, and feature requests are welcome!

---

**Built with ❤️ using Django**
