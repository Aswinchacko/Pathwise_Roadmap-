# Community Feature - Stack Overflow Style

## Overview
The community feature has been completely redesigned to look and feel like Stack Overflow, with modern styling, voting functionality, and real-time updates.

## Features ✨

### Stack Overflow Style Design
- **Clean, minimal interface** with Stack Overflow's signature colors
- **Orange accent** (#f48024) for votes and active elements
- **List-based layout** instead of grid for better readability
- **Stats sidebar** showing votes, answers, and views for each question
- **User avatars** with initials
- **Relative timestamps** (e.g., "asked 2 hours ago")
- **Tag system** for categorization

### Functionality
- ✅ Ask questions with title, description, and category
- ✅ Answer questions (comments)
- ✅ Upvote questions
- ✅ Filter by category
- ✅ View counts tracking
- ✅ Real-time updates
- ✅ Responsive design

## Quick Start

### 1. Seed Sample Data
```bash
cd auth_back
node seedDiscussions.js
```

This will populate your database with 10 realistic questions covering various topics like:
- React authentication
- Machine learning basics
- Career advice
- Web development
- And more!

### 2. Start the Backend
```bash
cd auth_back
npm start
```
Backend runs on `http://localhost:5000`

### 3. Start the Frontend
```bash
cd dashboard
npm run dev
```
Frontend runs on `http://localhost:5173`

### 4. Navigate to Community
- Open your browser to `http://localhost:5173`
- Log in with your account
- Click on "Community" in the sidebar

## Usage

### Viewing Questions
- Questions are displayed in a list format
- Each question shows:
  - **Votes count** (orange if > 0)
  - **Answers count** (green border if > 0)
  - **Views count**
  - Question title and preview
  - Category tag
  - Author info with avatar
  - Time posted

### Filtering
- Use the left sidebar to filter by category
- Categories include:
  - Web Development
  - Data Science
  - Career Advice
  - Development
  - Mobile Development
  - DevOps

### Asking a Question
1. Click "Ask Question" button in header
2. Fill in:
   - Title (e.g., "How do I implement authentication?")
   - Category
   - Detailed description
3. Click "Post Your Question"

### Viewing/Answering Questions
1. Click on any question card
2. Modal opens with:
   - Full question details
   - Voting buttons (up/down arrows)
   - All existing answers
   - Text area to post your answer
3. Vote by clicking the up arrow
4. Add your answer and click "Post Your Answer"

## API Endpoints

All endpoints are prefixed with `/api/discussions`

### GET /api/discussions
Get all discussions (optional category filter)
```javascript
// Get all
fetch('http://localhost:5000/api/discussions')

// Filter by category
fetch('http://localhost:5000/api/discussions?category=Web%20Development')
```

### GET /api/discussions/:id
Get single discussion (increments view count)
```javascript
fetch('http://localhost:5000/api/discussions/[id]')
```

### POST /api/discussions
Create new discussion (requires auth)
```javascript
fetch('http://localhost:5000/api/discussions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    title: 'Question title',
    description: 'Detailed description',
    category: 'Web Development'
  })
})
```

### POST /api/discussions/:id/comments
Add answer to discussion (requires auth)
```javascript
fetch('http://localhost:5000/api/discussions/[id]/comments', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    text: 'Your answer here'
  })
})
```

### PUT /api/discussions/:id/like
Upvote a discussion (requires auth)
```javascript
fetch('http://localhost:5000/api/discussions/[id]/like', {
  method: 'PUT',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
})
```

## Design Details

### Color Scheme
- **Primary Blue**: #0077cc (links, buttons)
- **Orange**: #f48024 (votes, highlights)
- **Green**: #5eba7d (answered questions)
- **Gray**: #6a737c (secondary text)
- **Background**: #f8f9f9
- **Border**: #d6d9dc

### Typography
- Clean, sans-serif fonts
- Hierarchy with font sizes and weights
- Good readability with proper line height

### Layout
- **Header**: Fixed header with search and "Ask Question" button
- **Sidebar**: Sticky category filter (200px wide)
- **Main Content**: Question list with stats
- **Modals**: Centered overlays for creating/viewing questions

## File Structure

```
dashboard/src/
├── pages/
│   ├── Community.jsx          # Main page component
│   └── Community.css          # Stack Overflow styles
├── components/community/
│   ├── DiscussionCard.jsx     # Question card with stats
│   ├── DiscussionList.jsx     # List of questions
│   ├── DiscussionDetailModal.jsx  # View/answer modal
│   ├── CreateDiscussionModal.jsx  # Ask question modal
│   └── Sidebar.jsx            # Category filter
└── services/
    └── discussionService.js   # API calls

auth_back/
├── models/
│   └── Discussion.js          # MongoDB schema
├── routes/
│   └── discussions.js         # API routes
└── seedDiscussions.js         # Sample data
```

## Database Schema

### Discussion
```javascript
{
  title: String (required),
  description: String (required),
  author: String (required),
  authorId: ObjectId (ref: User),
  category: String (enum),
  views: Number (default: 0),
  likes: Number (default: 0),
  comments: [CommentSchema],
  createdAt: Date,
  updatedAt: Date
}
```

### Comment (embedded)
```javascript
{
  text: String (required),
  author: String (required),
  authorId: ObjectId (ref: User),
  likes: Number (default: 0),
  createdAt: Date,
  updatedAt: Date
}
```

## Troubleshooting

### No discussions showing
1. Make sure you've seeded the database: `node seedDiscussions.js`
2. Check backend is running on port 5000
3. Check browser console for errors
4. Verify MongoDB is running

### Can't create discussions
- Make sure you're logged in
- Check that JWT token is present in localStorage
- Verify backend auth middleware is working

### Styles not loading
- Clear browser cache
- Check that Community.css is imported in Community.jsx
- Verify CSS variables are defined

## Future Enhancements

Potential features to add:
- 🔍 Search functionality
- 🏷️ More granular tags
- ⬆️⬇️ Downvoting
- ✅ Accept answer (mark as solution)
- 👤 User reputation system
- 📊 Trending questions
- 🔔 Notifications
- 💬 Comment on answers
- 🔖 Bookmark questions
- 📱 Better mobile responsiveness

## Credits

Design inspired by Stack Overflow's clean and functional interface.

