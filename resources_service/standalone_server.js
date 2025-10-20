const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = process.env.PORT || 8001;

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}));

// CORS configuration
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.',
    retryAfter: 900
  },
  standardHeaders: true,
  legacyHeaders: false,
});

app.use(limiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compression middleware
app.use(compression());

// Logging middleware
app.use(morgan('combined'));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    services: {
      mongodb: { status: 'mocked', note: 'Running in standalone mode' },
      redis: { status: 'unavailable', note: 'Redis is optional for this service' }
    }
  });
});

// Mock scraping endpoints
app.post('/api/scraping/resources', (req, res) => {
  const { query, domain, maxResults = 10 } = req.body;
  
  if (!query) {
    return res.status(400).json({
      success: false,
      error: 'Query is required'
    });
  }

  // Generate mock resources
  const mockResources = [];
  const numResources = Math.min(maxResults, 5);
  
  for (let i = 0; i < numResources; i++) {
    mockResources.push({
      id: `mock-${Date.now()}-${i}`,
      title: `${query} - Resource ${i + 1}`,
      description: `Mock resource about ${query} for learning purposes`,
      url: `https://example.com/resource-${i + 1}`,
      type: ['Tutorial', 'Course', 'Documentation', 'Video', 'Article'][i % 5],
      difficulty: ['Beginner', 'Intermediate', 'Advanced'][i % 3],
      duration: ['10 min', '30 min', '1 hour', '2 hours'][i % 4],
      domain: domain || 'General',
      skill: query,
      source: 'MockSource',
      color: '#3B82F6',
      tags: [query.toLowerCase()],
      rating: 4 + Math.random(),
      isActive: true,
      lastScraped: new Date(),
      metadata: {
        mockResource: true,
        scrapedAt: new Date()
      }
    });
  }

  res.json({
    success: true,
    message: `Successfully scraped ${mockResources.length} mock resources`,
    data: {
      query,
      domain,
      resourcesFound: mockResources.length,
      resources: mockResources
    }
  });
});

app.post('/api/scraping/url', (req, res) => {
  const { url, domain, skill } = req.body;
  
  if (!url) {
    return res.status(400).json({
      success: false,
      error: 'URL is required'
    });
  }

  const mockResource = {
    id: `mock-url-${Date.now()}`,
    title: `Resource from ${new URL(url).hostname}`,
    description: `Content scraped from ${url}`,
    url,
    type: 'Article',
    difficulty: 'Intermediate',
    duration: '10 min',
    domain: domain || 'General',
    skill: skill || 'General',
    source: new URL(url).hostname,
    color: '#3B82F6',
    tags: ['scraped'],
    rating: 4,
    isActive: true,
    lastScraped: new Date(),
    metadata: {
      mockResource: true,
      directScrape: true,
      scrapedAt: new Date()
    }
  };

  res.json({
    success: true,
    message: 'Successfully scraped URL',
    data: {
      url,
      resourcesFound: 1,
      resources: [mockResource]
    }
  });
});

app.get('/api/scraping/sources', (req, res) => {
  const sources = [
    {
      name: 'GitHub',
      description: 'Open source repositories and projects',
      types: ['Project', 'Tutorial'],
      active: true
    },
    {
      name: 'freeCodeCamp',
      description: 'Free coding tutorials and articles',
      types: ['Tutorial', 'Article'],
      active: true
    },
    {
      name: 'MDN Web Docs',
      description: 'Web development documentation',
      types: ['Documentation'],
      active: true
    },
    {
      name: 'YouTube',
      description: 'Video tutorials and lectures',
      types: ['Video'],
      active: true
    }
  ];

  res.json({
    success: true,
    data: { sources }
  });
});

app.get('/api/scraping/stats', (req, res) => {
  res.json({
    success: true,
    data: {
      totalResources: 42,
      recentlyScraped: 5,
      byType: {
        'Tutorial': 15,
        'Course': 10,
        'Documentation': 8,
        'Video': 6,
        'Article': 3
      },
      byDifficulty: {
        'Beginner': 20,
        'Intermediate': 15,
        'Advanced': 7
      }
    }
  });
});

// Mock resources endpoints
app.get('/api/resources', (req, res) => {
  const mockResources = [
    {
      id: 'mock-1',
      title: 'React Hooks Tutorial',
      description: 'Learn React Hooks with practical examples',
      url: 'https://react.dev/learn/state-a-components-memory',
      type: 'Tutorial',
      difficulty: 'Beginner',
      duration: '30 min',
      domain: 'Frontend Development',
      skill: 'React',
      source: 'React Docs',
      color: '#3B82F6'
    },
    {
      id: 'mock-2',
      title: 'JavaScript Async/Await Guide',
      description: 'Master asynchronous JavaScript programming',
      url: 'https://javascript.info/async-await',
      type: 'Guide',
      difficulty: 'Intermediate',
      duration: '45 min',
      domain: 'Frontend Development',
      skill: 'JavaScript',
      source: 'JavaScript.info',
      color: '#F59E0B'
    }
  ];

  res.json({
    success: true,
    resources: mockResources,
    pagination: {
      total: mockResources.length,
      limit: 50,
      offset: 0,
      hasMore: false
    }
  });
});

app.get('/api/resources/search', (req, res) => {
  const { q } = req.query;
  
  const mockResults = [
    {
      id: 'search-1',
      title: `${q} - Search Result 1`,
      description: `Tutorial about ${q}`,
      url: `https://example.com/search/${q.replace(/\s+/g, '-')}`,
      type: 'Tutorial',
      difficulty: 'Beginner',
      duration: '20 min',
      domain: 'General',
      skill: q,
      source: 'SearchSource',
      color: '#10B981'
    }
  ];

  res.json({
    success: true,
    resources: mockResults,
    query: q,
    resultsCount: mockResults.length
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'PathWise Resources Service API (Standalone Mode)',
    version: '1.0.0',
    status: 'operational',
    mode: 'standalone',
    endpoints: {
      health: '/health',
      resources: '/api/resources',
      scraping: '/api/scraping'
    }
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    message: `The requested endpoint ${req.originalUrl} does not exist`,
    availableEndpoints: [
      'GET /',
      'GET /health',
      'GET /api/resources',
      'POST /api/scraping/resources',
      'POST /api/scraping/url',
      'GET /api/scraping/sources'
    ]
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  res.status(err.status || 500).json({
    success: false,
    error: err.message || 'Internal Server Error'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Resources Service (Standalone) running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  console.log(`📚 API docs: http://localhost:${PORT}/api/resources`);
  console.log(`⚡ Scraping: http://localhost:${PORT}/api/scraping`);
  console.log(`\n✨ Ready to handle scraping requests!`);
});

module.exports = app;


