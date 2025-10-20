const express = require('express');
const mongoose = require('mongoose');
const { getRedisClient } = require('../config/redis');
const logger = require('../utils/logger');

const router = express.Router();

// GET /health - Health check endpoint
router.get('/', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    version: process.env.npm_package_version || '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    services: {}
  };

  let statusCode = 200;

  try {
    // Check MongoDB connection
    if (mongoose.connection.readyState === 1) {
      health.services.mongodb = {
        status: 'connected',
        host: mongoose.connection.host,
        name: mongoose.connection.name
      };
    } else {
      health.services.mongodb = {
        status: 'disconnected',
        error: 'MongoDB not connected'
      };
      health.status = 'degraded';
      statusCode = 503;
    }

    // Check Redis connection (optional)
    const redisClient = getRedisClient();
    if (redisClient && redisClient.isOpen) {
      health.services.redis = {
        status: 'connected'
      };
    } else {
      health.services.redis = {
        status: 'unavailable',
        note: 'Redis is optional for this service'
      };
    }

    // Memory usage
    const memUsage = process.memoryUsage();
    health.memory = {
      rss: `${Math.round(memUsage.rss / 1024 / 1024)} MB`,
      heapTotal: `${Math.round(memUsage.heapTotal / 1024 / 1024)} MB`,
      heapUsed: `${Math.round(memUsage.heapUsed / 1024 / 1024)} MB`
    };

  } catch (error) {
    logger.error('Health check error:', error);
    health.status = 'error';
    health.error = error.message;
    statusCode = 503;
  }

  res.status(statusCode).json(health);
});

// GET /health/ready - Readiness probe
router.get('/ready', async (req, res) => {
  try {
    // Check if MongoDB is ready
    if (mongoose.connection.readyState !== 1) {
      return res.status(503).json({
        status: 'not ready',
        reason: 'MongoDB not connected'
      });
    }

    res.json({
      status: 'ready',
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    logger.error('Readiness check error:', error);
    res.status(503).json({
      status: 'not ready',
      error: error.message
    });
  }
});

// GET /health/live - Liveness probe
router.get('/live', (req, res) => {
  res.json({
    status: 'alive',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

module.exports = router;


