const mongoose = require('mongoose')
const Discussion = require('./models/Discussion')
require('dotenv').config()

const sampleDiscussions = [
  {
    title: 'How to handle authentication in React with JWT tokens?',
    description: 'I\'m building a React application and need to implement JWT authentication. I\'ve tried storing the token in localStorage, but I\'m concerned about security. What are the best practices for handling JWT tokens in a React app? Should I use httpOnly cookies instead? How do I handle token refresh?',
    author: 'Sarah Chen',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Web Development',
    views: 1247,
    likes: 42,
    comments: [
      {
        text: 'Using httpOnly cookies is definitely more secure than localStorage for storing JWT tokens. localStorage is vulnerable to XSS attacks. I recommend storing the access token in memory and the refresh token in an httpOnly cookie.',
        author: 'David Martinez',
        authorId: new mongoose.Types.ObjectId(),
        likes: 15
      },
      {
        text: 'Here\'s a simple approach: Use Context API or Redux to store the token in memory. Implement an axios interceptor to automatically add the token to requests. For refresh tokens, use a secure httpOnly cookie and implement a refresh endpoint.',
        author: 'Emma Thompson',
        authorId: new mongoose.Types.ObjectId(),
        likes: 28
      }
    ]
  },
  {
    title: 'What\'s the difference between supervised and unsupervised learning?',
    description: 'I\'m new to machine learning and keep hearing about supervised vs unsupervised learning. Can someone explain the key differences with practical examples? Which one should I start learning first?',
    author: 'Alex Rodriguez',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Data Science',
    views: 892,
    likes: 35,
    comments: [
      {
        text: 'Supervised learning uses labeled data (input-output pairs) to train models. Examples: classification, regression. Unsupervised learning finds patterns in unlabeled data. Examples: clustering, dimensionality reduction. Start with supervised learning - it\'s more intuitive!',
        author: 'Dr. Lisa Wang',
        authorId: new mongoose.Types.ObjectId(),
        likes: 22
      }
    ]
  },
  {
    title: 'Should I learn React or Vue.js in 2024?',
    description: 'I\'m a beginner web developer trying to decide between React and Vue.js. I see React has more job opportunities, but Vue seems easier to learn. What would you recommend for someone starting out? Are there any major differences I should consider?',
    author: 'Michael Johnson',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Web Development',
    views: 2134,
    likes: 67,
    comments: [
      {
        text: 'React has a larger ecosystem and more job opportunities. However, Vue\'s learning curve is gentler. If you\'re looking for jobs, go with React. If you want to build personal projects quickly, Vue is great.',
        author: 'Carlos Mendez',
        authorId: new mongoose.Types.ObjectId(),
        likes: 31
      },
      {
        text: 'I\'d say learn React. The concepts you learn (components, state management, hooks) are more transferable. Plus, React Native lets you build mobile apps with the same knowledge.',
        author: 'Jennifer Kim',
        authorId: new mongoose.Types.ObjectId(),
        likes: 18
      },
      {
        text: 'Don\'t overthink it! Both are excellent choices. Pick one and focus on mastering JavaScript fundamentals. Once you know one framework well, learning others becomes much easier.',
        author: 'Tom Anderson',
        authorId: new mongoose.Types.ObjectId(),
        likes: 25
      }
    ]
  },
  {
    title: 'How to prepare for FAANG interviews as a self-taught developer?',
    description: 'I\'ve been learning to code for about 2 years now, mostly through online courses and personal projects. I want to apply to FAANG companies but I\'m not sure how to prepare. What resources should I use? How important are data structures and algorithms? Should I focus on building more projects or solving LeetCode problems?',
    author: 'Priya Sharma',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Career Advice',
    views: 3421,
    likes: 156,
    comments: [
      {
        text: 'LeetCode is essential! I got into Google after solving ~300 medium/hard problems. Focus on patterns: two pointers, sliding window, DFS/BFS, dynamic programming. Also practice system design for senior roles.',
        author: 'Kevin Zhang',
        authorId: new mongoose.Types.ObjectId(),
        likes: 89
      },
      {
        text: 'Don\'t neglect behavioral interviews! Use the STAR method. Also, having 2-3 strong projects on GitHub shows you can build real things, which matters a lot.',
        author: 'Sofia Martinez',
        authorId: new mongoose.Types.ObjectId(),
        likes: 45
      }
    ]
  },
  {
    title: 'Python async/await vs threading - when to use which?',
    description: 'I\'m working on a Python application that needs to handle multiple concurrent operations. I\'m confused about when to use asyncio with async/await versus traditional threading. Can someone explain the differences and provide guidance on when each approach is more appropriate?',
    author: 'Robert Lee',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Development',
    views: 1567,
    likes: 48,
    comments: [
      {
        text: 'Use async/await for I/O-bound operations (API calls, database queries, file operations). Use threading for CPU-bound tasks. Asyncio is more efficient for high-concurrency I/O scenarios because it uses a single thread with cooperative multitasking.',
        author: 'James Wilson',
        authorId: new mongoose.Types.ObjectId(),
        likes: 32
      }
    ]
  },
  {
    title: 'Best practices for Git branching strategy in a team?',
    description: 'Our team of 5 developers keeps running into merge conflicts and confusion with our Git workflow. What branching strategy would you recommend? We\'re currently using a modified Git Flow but it feels too complex for our small team.',
    author: 'Nina Patel',
    authorId: new mongoose.Types.ObjectId(),
    category: 'DevOps',
    views: 978,
    likes: 31,
    comments: [
      {
        text: 'For small teams, I recommend GitHub Flow. It\'s simpler: main branch is always deployable, create feature branches, open PRs, merge after review. Add branch protection rules to prevent direct pushes to main.',
        author: 'Ahmed Hassan',
        authorId: new mongoose.Types.ObjectId(),
        likes: 18
      },
      {
        text: 'We use trunk-based development with feature flags. Developers commit to main frequently (daily), use feature flags to hide incomplete features. Works great for CI/CD!',
        author: 'Laura Schmidt',
        authorId: new mongoose.Types.ObjectId(),
        likes: 12
      }
    ]
  },
  {
    title: 'iOS vs Android development - which should I learn first?',
    description: 'I want to get into mobile app development but I\'m not sure whether to start with iOS (Swift) or Android (Kotlin). I know both platforms well as a user, but from a developer perspective, which one is better to learn first? Does it matter?',
    author: 'Daniel Park',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Mobile Development',
    views: 1823,
    likes: 52,
    comments: [
      {
        text: 'Learn both by using Flutter or React Native! You\'ll be able to build for both platforms simultaneously. Flutter is especially good for beginners.',
        author: 'Maria Santos',
        authorId: new mongoose.Types.ObjectId(),
        likes: 34
      }
    ]
  },
  {
    title: 'How do I optimize SQL queries for better performance?',
    description: 'My application is getting slower as the database grows. Some queries are taking several seconds to execute. What are the most important things I should check? I\'ve heard about indexes but I\'m not sure how to use them effectively.',
    author: 'Chris Anderson',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Data Science',
    views: 1456,
    likes: 44,
    comments: []
  },
  {
    title: 'Microservices vs Monolith - when to make the switch?',
    description: 'Our startup has been growing and our monolithic application is becoming harder to maintain. Everyone keeps talking about microservices, but I\'m not sure if we\'re ready for that complexity. At what point does it make sense to move from a monolith to microservices?',
    author: 'Rachel Green',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Development',
    views: 2891,
    likes: 98,
    comments: [
      {
        text: 'Don\'t rush into microservices! They add significant operational complexity. Only consider them when: 1) Your team is large enough to own separate services, 2) You have clear bounded contexts, 3) You have solid DevOps infrastructure. Many successful companies run monoliths at scale.',
        author: 'Marcus Johnson',
        authorId: new mongoose.Types.ObjectId(),
        likes: 67
      },
      {
        text: 'Consider a modular monolith first. It gives you many benefits of microservices (clear boundaries, independent teams) without the distributed system complexity. You can always extract services later if needed.',
        author: 'Anna Kowalski',
        authorId: new mongoose.Types.ObjectId(),
        likes: 41
      }
    ]
  },
  {
    title: 'What are some must-know design patterns for senior developers?',
    description: 'I\'m preparing for senior developer interviews and want to make sure I understand the most important design patterns. Which patterns do you use most frequently in your daily work? Any patterns that are overrated?',
    author: 'Brandon Taylor',
    authorId: new mongoose.Types.ObjectId(),
    category: 'Development',
    views: 2156,
    likes: 73,
    comments: [
      {
        text: 'Most used: Singleton, Factory, Observer, Strategy, Decorator. Less common but important: Adapter, Proxy, Command. Don\'t memorize all 23 GoF patterns - focus on understanding when and why to use patterns.',
        author: 'Diana Chen',
        authorId: new mongoose.Types.ObjectId(),
        likes: 45
      }
    ]
  }
]

async function seedDiscussions() {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/pathwise')
    console.log('Connected to MongoDB')

    // Clear existing discussions
    await Discussion.deleteMany({})
    console.log('Cleared existing discussions')

    // Insert sample discussions
    await Discussion.insertMany(sampleDiscussions)
    console.log('Seeded discussions successfully')

    process.exit(0)
  } catch (error) {
    console.error('Error seeding discussions:', error)
    process.exit(1)
  }
}

seedDiscussions()
