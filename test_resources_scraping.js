const axios = require('axios');

const RESOURCES_API_URL = 'http://localhost:8001';

// Test the resources service scraping functionality
async function testResourcesScraping() {
  console.log('🔍 Testing Resources Service Scraping...\n');

  try {
    // Test 1: Health check
    console.log('1. Testing health endpoint...');
    const healthResponse = await axios.get(`${RESOURCES_API_URL}/health`);
    console.log('✅ Health check:', healthResponse.data);

    // Test 2: Get scraping sources
    console.log('\n2. Testing scraping sources...');
    const sourcesResponse = await axios.get(`${RESOURCES_API_URL}/api/scraping/sources`);
    console.log('✅ Scraping sources:', sourcesResponse.data.data.sources.length, 'sources available');

    // Test 3: Test query scraping
    console.log('\n3. Testing query scraping...');
    const scrapingResponse = await axios.post(`${RESOURCES_API_URL}/api/scraping/resources`, {
      query: 'React hooks tutorial',
      domain: 'Frontend Development',
      maxResults: 10,
      includeVideo: true,
      includeArticles: true
    });
    console.log('✅ Query scraping result:', scrapingResponse.data);

    // Test 4: Test URL scraping
    console.log('\n4. Testing URL scraping...');
    const urlScrapingResponse = await axios.post(`${RESOURCES_API_URL}/api/scraping/url`, {
      url: 'https://react.dev/learn/state-a-components-memory',
      domain: 'Frontend Development',
      skill: 'React hooks'
    });
    console.log('✅ URL scraping result:', urlScrapingResponse.data);

    // Test 5: Get scraped resources
    console.log('\n5. Testing scraped resources retrieval...');
    const resourcesResponse = await axios.get(`${RESOURCES_API_URL}/api/resources?limit=5`);
    console.log('✅ Scraped resources:', resourcesResponse.data);

    console.log('\n🎉 All tests passed! Resources scraping is working correctly.');

  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
    
    if (error.code === 'ECONNREFUSED') {
      console.log('\n💡 Make sure the Resources Service is running on port 8001');
      console.log('   Run: npm start in the resources_service directory');
    }
  }
}

// Run the test
testResourcesScraping();


