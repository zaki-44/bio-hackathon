# Bio Marketplace - React Frontend

A modern React.js frontend for the Bio Marketplace platform, built with TypeScript, Vite, and Tailwind CSS.

## Features

- 🔐 **Authentication**: Login, Register, Session Management
- 👨‍🌾 **Farmer Applications**: Apply to become a verified farmer
- 📦 **Product Management**: Create and search for products (farmer-only)
- 👨‍💼 **Admin Dashboard**: Manage farmer applications (approve/deny)
- 🎨 **Modern UI**: Beautiful, responsive design with Tailwind CSS
- 🔄 **Real-time Updates**: Session-based authentication with automatic state management

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Backend server running on `http://localhost:5000`

### Installation

1. Navigate to the frontend directory:
```bash
cd vite
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or the port Vite assigns).

## Project Structure

```
vite/
├── src/
│   ├── components/       # Reusable components
│   │   └── Layout/      # Layout components (Navbar, Layout)
│   ├── contexts/        # React contexts
│   │   └── AuthContext.tsx  # Authentication state management
│   ├── pages/           # Page components
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── FarmerApply.tsx
│   │   ├── Products.tsx
│   │   ├── ProductCreate.tsx
│   │   └── Admin.tsx
│   ├── services/        # API service layer
│   │   └── api.ts       # All API calls
│   ├── App.tsx          # Main app component with routing
│   └── main.tsx         # Entry point
├── package.json
└── vite.config.ts
```

## API Integration

The frontend communicates with the Flask backend at `http://localhost:5000`. All API calls are centralized in `src/services/api.ts` and use session-based authentication (cookies).

### Available APIs

- **Authentication**: `/api/login`, `/api/register`, `/api/logout`, `/api/profile`, `/api/session`
- **Farmer Applications**: `/api/farmers/apply`, `/api/admin/farmers/applications/*`
- **Products**: `/api/products`, `/api/products/search`
- **Sellers**: `/api/admin/sellers`

## User Roles

- **User**: Can browse and search products
- **Farmer**: Can create products, manage listings
- **Transporter**: (Future feature)
- **Admin**: Can manage farmer applications

## Routes

- `/` - Home page
- `/login` - Login page
- `/register` - Registration page
- `/farmer/apply` - Farmer application form
- `/products` - Product search and listing
- `/products/create` - Create new product (farmer only)
- `/admin` - Admin dashboard (for managing applications)

## Development

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Technologies Used

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Notes

- The frontend uses session-based authentication (cookies) instead of JWT tokens
- All API calls include `credentials: 'include'` to send cookies
- The backend must have CORS configured with `supports_credentials=True`
- Make sure the backend is running before starting the frontend
