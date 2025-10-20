const axios = require('axios');
const cheerio = require('cheerio');
const Resource = require('../models/Resource');
const logger = require('../utils/logger');

class SimplifiedWebScrapingService {
  constructor() {
    this.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36';
    this.delay = 1000; // 1 second between requests
  }

  async makeRequest(url, options = {}) {
    const config = {
      method: 'GET',
      url,
      headers: {
        'User-Agent': this.userAgent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
      },
      timeout: 10000,
      ...options
    };

    try {
      const response = await axios(config);
      return response.data;
    } catch (error) {
      logger.error(`Request failed for ${url}:`, error.message);
      throw error;
    }
  }

  async scrapeResourcesFromQuery(query, domain = null, options = {}) {
    const { maxResults = 20 } = options;
    const resources = [];
    
    logger.info(`🔍 Starting simplified resource scraping for: ${query}`);

    try {
      // Generate mock resources for demonstration
      const mockResources = this.generateMockResources(query, domain, maxResults);
      
      // Process and save resources
      const processedResources = await this.processAndSaveResources(mockResources, domain);
      
      logger.info(`🎉 Scraping completed: ${processedResources.length} resources found`);
      return processedResources;
    } catch (error) {
      logger.error('Scraping error:', error.message);
      return [];
    }
  }

  generateMockResources(query, domain, maxResults) {
    const resources = [];
    const queryLower = query.toLowerCase();
    
    // Generate relevant mock resources based on query
    const templates = [
      {
        title: `${query} - Complete Guide`,
        description: `Comprehensive guide to ${query} with examples and best practices`,
        type: 'Tutorial',
        source: 'MockSource',
        url: `https://example.com/guide/${queryLower.replace(/\s+/g, '-')}`
      },
      {
        title: `Learn ${query} - Interactive Course`,
        description: `Interactive online course covering ${query} fundamentals`,
        type: 'Course',
        source: 'MockEdu',
        url: `https://mockedu.com/course/${queryLower.replace(/\s+/g, '-')}`
      },
      {
        title: `${query} Documentation`,
        description: `Official documentation for ${query}`,
        type: 'Documentation',
        source: 'MockDocs',
        url: `https://docs.example.com/${queryLower.replace(/\s+/g, '-')}`
      },
      {
        title: `${query} Tutorial Video`,
        description: `Video tutorial explaining ${query} concepts`,
        type: 'Video',
        source: 'MockTube',
        url: `https://mocktube.com/watch/${queryLower.replace(/\s+/g, '-')}`
      },
      {
        title: `${query} Project Examples`,
        description: `Real-world project examples using ${query}`,
        type: 'Project',
        source: 'MockHub',
        url: `https://mockhub.com/project/${queryLower.replace(/\s+/g, '-')}`
      }
    ];

    const numToGenerate = Math.min(maxResults, templates.length);
    
    for (let i = 0; i < numToGenerate; i++) {
      const template = templates[i];
      resources.push({
        ...template,
        difficulty: this.getRandomDifficulty(),
        duration: this.getRandomDuration(),
        domain: domain || this.inferDomain(query),
        skill: query,
        metadata: {
          scrapedAt: new Date(),
          mockResource: true
        }
      });
    }

    return resources;
  }

  async scrapeSpecificUrl(url, domain = null, skill = null) {
    try {
      logger.info(`🔗 Scraping specific URL: ${url}`);
      
      // For demo purposes, create a mock resource
      const resource = {
        title: `Resource from ${new URL(url).hostname}`,
        description: `Content scraped from ${url}`,
        url,
        type: 'Article',
        difficulty: 'Intermediate',
        duration: '10 min',
        source: new URL(url).hostname,
        domain: domain || 'General',
        skill: skill || 'General',
        metadata: {
          scrapedAt: new Date(),
          directScrape: true,
          mockResource: true
        }
      };
      
      return await this.processAndSaveResources([resource], domain);
    } catch (error) {
      logger.error(`Error scraping URL ${url}:`, error.message);
      throw error;
    }
  }

  async processAndSaveResources(resources, domain) {
    const processedResources = [];
    const seenUrls = new Set();
    
    for (const resource of resources) {
      // Skip duplicates
      if (seenUrls.has(resource.url)) continue;
      seenUrls.add(resource.url);
      
      // Generate unique ID
      const id = this.generateResourceId(resource.title, resource.source);
      
      // Validate and clean data
      const processedResource = {
        id,
        title: this.cleanTitle(resource.title),
        description: this.cleanDescription(resource.description),
        url: resource.url,
        type: resource.type || 'Tutorial',
        difficulty: resource.difficulty || 'Beginner',
        duration: resource.duration || '30 min',
        domain: resource.domain || domain || 'General',
        skill: resource.skill,
        source: resource.source,
        color: this.getColorForType(resource.type),
        tags: this.extractTags(resource.title, resource.description),
        rating: resource.rating || 0,
        isActive: true,
        lastScraped: new Date(),
        metadata: resource.metadata || {}
      };
      
      try {
        // Check if resource already exists
        const existingResource = await Resource.findOne({ url: resource.url });
        
        if (existingResource) {
          // Update existing resource
          await Resource.findByIdAndUpdate(existingResource._id, {
            ...processedResource,
            lastScraped: new Date()
          });
          logger.info(`Updated existing resource: ${resource.title}`);
        } else {
          // Create new resource
          const newResource = new Resource(processedResource);
          await newResource.save();
          processedResources.push(processedResource);
          logger.info(`Created new resource: ${resource.title}`);
        }
      } catch (error) {
        logger.error(`Error saving resource ${resource.title}:`, error.message);
      }
    }
    
    return processedResources;
  }

  // Helper methods
  generateResourceId(title, source) {
    const cleanTitle = title.toLowerCase().replace(/[^a-z0-9]/g, '-').substring(0, 50);
    const cleanSource = source.toLowerCase().replace(/[^a-z0-9]/g, '-');
    return `${cleanSource}-${cleanTitle}-${Date.now()}`;
  }

  cleanTitle(title) {
    return title.trim().substring(0, 200);
  }

  cleanDescription(description) {
    return description.trim().substring(0, 1000);
  }

  getRandomDifficulty() {
    const difficulties = ['Beginner', 'Intermediate', 'Advanced'];
    return difficulties[Math.floor(Math.random() * difficulties.length)];
  }

  getRandomDuration() {
    const durations = ['10 min', '30 min', '1 hour', '2 hours', '1 day', '1 week'];
    return durations[Math.floor(Math.random() * durations.length)];
  }

  inferDomain(query) {
    const queryLower = query.toLowerCase();
    
    if (queryLower.includes('react') || queryLower.includes('vue') || queryLower.includes('angular') || 
        queryLower.includes('frontend') || queryLower.includes('css') || queryLower.includes('html') || 
        queryLower.includes('javascript')) {
      return 'Frontend Development';
    }
    
    if (queryLower.includes('node') || queryLower.includes('express') || queryLower.includes('backend') || 
        queryLower.includes('api') || queryLower.includes('server')) {
      return 'Backend Development';
    }
    
    if (queryLower.includes('python') || queryLower.includes('machine learning') || 
        queryLower.includes('data science') || queryLower.includes('ai')) {
      return 'Data Science & AI';
    }
    
    if (queryLower.includes('mobile') || queryLower.includes('android') || queryLower.includes('ios') || 
        queryLower.includes('react native') || queryLower.includes('flutter')) {
      return 'Mobile Development';
    }
    
    if (queryLower.includes('devops') || queryLower.includes('docker') || queryLower.includes('kubernetes') || 
        queryLower.includes('aws') || queryLower.includes('cloud')) {
      return 'DevOps & Cloud';
    }
    
    return 'General';
  }

  getColorForType(type) {
    const colors = {
      'Tutorial': '#10B981',
      'Course': '#3B82F6',
      'Documentation': '#6366F1',
      'Interactive': '#F59E0B',
      'Book': '#8B5CF6',
      'Guide': '#06B6D4',
      'Project': '#EF4444',
      'Video': '#EC4899',
      'Article': '#84CC16'
    };
    
    return colors[type] || '#6B7280';
  }

  extractTags(title, description) {
    const text = (title + ' ' + description).toLowerCase();
    const tags = [];
    
    const commonTags = [
      'javascript', 'python', 'react', 'node.js', 'css', 'html', 'vue', 'angular',
      'machine learning', 'data science', 'api', 'database', 'mongodb', 'sql',
      'docker', 'kubernetes', 'aws', 'cloud', 'mobile', 'android', 'ios',
      'tutorial', 'beginner', 'advanced', 'guide', 'course'
    ];
    
    for (const tag of commonTags) {
      if (text.includes(tag)) {
        tags.push(tag);
      }
    }
    
    return tags.slice(0, 5); // Limit to 5 tags
  }

  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = SimplifiedWebScrapingService;


