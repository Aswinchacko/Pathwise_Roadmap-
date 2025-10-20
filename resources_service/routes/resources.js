const express = require('express');
const { query, validationResult } = require('express-validator');
const Resource = require('../models/Resource');
const logger = require('../utils/logger');

const router = express.Router();

// GET /api/resources - Get all resources with optional filters
router.get('/', [
  query('domain').optional().trim(),
  query('type').optional().trim(),
  query('difficulty').optional().trim(),
  query('search').optional().trim(),
  query('limit').optional().isInt({ min: 1, max: 1000 }),
  query('offset').optional().isInt({ min: 0 })
], async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    const {
      domain,
      type,
      difficulty,
      search,
      limit = 50,
      offset = 0
    } = req.query;

    // Build query
    const query = { isActive: true };
    
    if (domain) {
      query.domain = new RegExp(domain, 'i');
    }
    
    if (type) {
      query.type = type;
    }
    
    if (difficulty) {
      query.difficulty = difficulty;
    }

    let resources;
    
    if (search) {
      // Text search
      resources = await Resource.find({
        ...query,
        $text: { $search: search }
      }, { score: { $meta: 'textScore' } })
        .sort({ score: { $meta: 'textScore' } })
        .limit(parseInt(limit))
        .skip(parseInt(offset));
    } else {
      // Regular query
      resources = await Resource.find(query)
        .sort({ lastScraped: -1, createdAt: -1 })
        .limit(parseInt(limit))
        .skip(parseInt(offset));
    }

    const total = await Resource.countDocuments(query);

    res.json({
      success: true,
      resources,
      pagination: {
        total,
        limit: parseInt(limit),
        offset: parseInt(offset),
        hasMore: total > parseInt(offset) + parseInt(limit)
      }
    });

  } catch (error) {
    logger.error('Resources fetch error:', error);
    next(error);
  }
});

// GET /api/resources/search - Search resources
router.get('/search', [
  query('q').notEmpty().trim().withMessage('Search query is required'),
  query('domain').optional().trim(),
  query('type').optional().trim(),
  query('difficulty').optional().trim(),
  query('limit').optional().isInt({ min: 1, max: 100 })
], async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    const { q, domain, type, difficulty, limit = 50 } = req.query;

    // Build search query
    const searchQuery = {
      isActive: true,
      $text: { $search: q }
    };
    
    if (domain) {
      searchQuery.domain = new RegExp(domain, 'i');
    }
    
    if (type) {
      searchQuery.type = type;
    }
    
    if (difficulty) {
      searchQuery.difficulty = difficulty;
    }

    const resources = await Resource.find(searchQuery, { score: { $meta: 'textScore' } })
      .sort({ score: { $meta: 'textScore' } })
      .limit(parseInt(limit));

    res.json({
      success: true,
      resources,
      query: q,
      resultsCount: resources.length
    });

  } catch (error) {
    logger.error('Resources search error:', error);
    next(error);
  }
});

// GET /api/resources/domain/:domain - Get resources by domain
router.get('/domain/:domain', async (req, res, next) => {
  try {
    const { domain } = req.params;
    const { limit = 50, offset = 0 } = req.query;

    const resources = await Resource.find({
      domain: new RegExp(domain, 'i'),
      isActive: true
    })
      .sort({ lastScraped: -1, createdAt: -1 })
      .limit(parseInt(limit))
      .skip(parseInt(offset));

    const total = await Resource.countDocuments({
      domain: new RegExp(domain, 'i'),
      isActive: true
    });

    res.json({
      success: true,
      resources,
      domain,
      pagination: {
        total,
        limit: parseInt(limit),
        offset: parseInt(offset),
        hasMore: total > parseInt(offset) + parseInt(limit)
      }
    });

  } catch (error) {
    logger.error('Domain resources fetch error:', error);
    next(error);
  }
});

// GET /api/resources/stats - Get resource statistics
router.get('/stats', async (req, res, next) => {
  try {
    const totalResources = await Resource.countDocuments({ isActive: true });
    
    const typeStats = await Resource.aggregate([
      { $match: { isActive: true } },
      { $group: { _id: '$type', count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]);

    const difficultyStats = await Resource.aggregate([
      { $match: { isActive: true } },
      { $group: { _id: '$difficulty', count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]);

    const domainStats = await Resource.aggregate([
      { $match: { isActive: true } },
      { $group: { _id: '$domain', count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]);

    const recentlyScraped = await Resource.countDocuments({
      isActive: true,
      lastScraped: { $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
    });

    const byType = {};
    typeStats.forEach(stat => {
      byType[stat._id] = stat.count;
    });

    const byDifficulty = {};
    difficultyStats.forEach(stat => {
      byDifficulty[stat._id] = stat.count;
    });

    const byDomain = {};
    domainStats.forEach(stat => {
      byDomain[stat._id] = stat.count;
    });

    res.json({
      success: true,
      data: {
        totalResources,
        recentlyScraped,
        byType,
        byDifficulty,
        byDomain
      }
    });

  } catch (error) {
    logger.error('Stats error:', error);
    next(error);
  }
});

// GET /api/resources/:id - Get specific resource
router.get('/:id', async (req, res, next) => {
  try {
    const { id } = req.params;
    
    const resource = await Resource.findOne({
      $or: [
        { _id: id },
        { id: id }
      ],
      isActive: true
    });

    if (!resource) {
      return res.status(404).json({
        success: false,
        message: 'Resource not found'
      });
    }

    // Increment views
    await resource.incrementViews();

    res.json({
      success: true,
      resource
    });

  } catch (error) {
    logger.error('Resource fetch error:', error);
    next(error);
  }
});

module.exports = router;