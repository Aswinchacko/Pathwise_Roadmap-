const { createClient } = require('redis');
const logger = require('../utils/logger');

let redisClient = null;

const connectRedis = async () => {
  try {
    const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';
    
    redisClient = createClient({
      url: redisUrl,
      socket: {
        connectTimeout: 5000,
        reconnectStrategy: (retries) => {
          if (retries > 5) {
            logger.error('Redis max retry attempts reached');
            return false;
          }
          return Math.min(retries * 100, 3000);
        }
      }
    });

    redisClient.on('error', (err) => {
      logger.error('Redis Client Error:', err);
    });

    redisClient.on('connect', () => {
      logger.info('🔗 Redis Client Connected');
    });

    redisClient.on('ready', () => {
      logger.info('✅ Redis Client Ready');
    });

    redisClient.on('end', () => {
      logger.warn('Redis Client Disconnected');
    });

    await redisClient.connect();
    
  } catch (error) {
    logger.error('Redis connection failed:', error);
    // Don't exit process if Redis fails, just log the error
    logger.warn('Continuing without Redis cache...');
  }
};

const getRedisClient = () => {
  if (!redisClient || !redisClient.isOpen) {
    logger.warn('Redis client not available');
    return null;
  }
  return redisClient;
};

module.exports = { connectRedis, getRedisClient };

