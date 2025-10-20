// Simple test for resources service
const http = require('http');

function testResourcesService() {
  console.log('🔍 Testing Resources Service...\n');

  // Test health endpoint
  const options = {
    hostname: 'localhost',
    port: 8001,
    path: '/health',
    method: 'GET',
    timeout: 5000
  };

  const req = http.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      try {
        const response = JSON.parse(data);
        console.log('✅ Health check response:', response);
        
        if (response.status === 'ok' || response.status === 'degraded') {
          console.log('🎉 Resources Service is running!');
          testScraping();
        } else {
          console.log('⚠️  Service is running but not healthy');
        }
      } catch (error) {
        console.log('❌ Invalid response:', data);
      }
    });
  });

  req.on('error', (error) => {
    console.log('❌ Service not reachable:', error.message);
    console.log('💡 Make sure to start the Resources Service first:');
    console.log('   cd resources_service && npm start');
  });

  req.on('timeout', () => {
    console.log('❌ Request timed out');
    req.destroy();
  });

  req.end();
}

function testScraping() {
  console.log('\n📡 Testing scraping endpoint...');
  
  const postData = JSON.stringify({
    query: 'React hooks tutorial',
    domain: 'Frontend Development',
    maxResults: 5
  });

  const options = {
    hostname: 'localhost',
    port: 8001,
    path: '/api/scraping/resources',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData)
    },
    timeout: 10000
  };

  const req = http.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      try {
        const response = JSON.parse(data);
        console.log('✅ Scraping response:', response);
        
        if (response.success) {
          console.log('🎉 Scraping functionality is working!');
          console.log(`📚 Found ${response.data.resourcesFound} resources`);
        } else {
          console.log('⚠️  Scraping failed:', response.error);
        }
      } catch (error) {
        console.log('❌ Invalid scraping response:', data);
      }
    });
  });

  req.on('error', (error) => {
    console.log('❌ Scraping test failed:', error.message);
  });

  req.on('timeout', () => {
    console.log('❌ Scraping request timed out');
    req.destroy();
  });

  req.write(postData);
  req.end();
}

// Run the test
testResourcesService();


