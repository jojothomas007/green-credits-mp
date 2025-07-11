// Load environment variables
require('dotenv').config();

const axios = require('axios');
const { format, subDays } = require('date-fns');

class SentinelHubAPI {
  constructor() {
    this.clientId = process.env.SENTINEL_HUB_CLIENT_ID;
    this.clientSecret = process.env.SENTINEL_HUB_CLIENT_SECRET;
    this.baseUrl = 'https://services.sentinel-hub.com';
    this.accessToken = null;
    this.tokenExpiry = null;
    this.useMockData = process.env.USE_MOCK_DATA === 'true';
  }

  /**
   * Authenticate with Sentinel Hub API
   */
  async authenticate() {
    // Use mock data if enabled
    if (this.useMockData) {
      console.log('🧪 Using mock data mode (no real API calls)');
      this.accessToken = 'mock_token';
      this.tokenExpiry = Date.now() + (3600 * 1000); // 1 hour
      return this.accessToken;
    }

    if (this.accessToken && this.tokenExpiry && Date.now() < this.tokenExpiry) {
      return this.accessToken;
    }

    if (!this.clientId || !this.clientSecret || 
        this.clientId === 'your_client_id_here' || 
        this.clientSecret === 'your_client_secret_here') {
      throw new Error('Sentinel Hub credentials not found. Please check your .env file.');
    }

    try {
      const response = await axios.post(`${this.baseUrl}/oauth/token`, {
        grant_type: 'client_credentials',
        client_id: this.clientId,
        client_secret: this.clientSecret
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      this.accessToken = response.data.access_token;
      this.tokenExpiry = Date.now() + (response.data.expires_in * 1000);
      
      return this.accessToken;
    } catch (error) {
      throw new Error(`Authentication failed: ${error.response?.data?.error_description || error.message}`);
    }
  }

  /**
   * Create the evaluation script for NDVI calculation
   */
  getEvaluationScript() {
    return `
      //VERSION=3
      function setup() {
        return {
          input: ["B04", "B08", "SCL", "dataMask"],
          output: { bands: 4 }
        };
      }

      function evaluatePixel(sample) {
        // Calculate NDVI: (NIR - Red) / (NIR + Red)
        let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
        
        // Handle invalid values
        if (sample.B08 + sample.B04 === 0 || sample.dataMask === 0) {
          ndvi = -999; // Invalid pixel
        }
        
        // Scene Classification Layer (SCL) for cloud masking
        // 0: No Data, 1: Saturated, 3: Cloud shadows, 8: Cloud medium probability, 9: Cloud high probability, 10: Thin cirrus
        let isCloud = sample.SCL === 3 || sample.SCL === 8 || sample.SCL === 9 || sample.SCL === 10;
        let quality = isCloud ? 0 : 1;
        
        return [ndvi, quality, sample.B04, sample.B08];
      }
    `;
  }

  /**
   * Get NDVI data for specified coordinates and date range
   */
  async getNDVIData(latitude, longitude, startDate, endDate, cloudCoverage = 20) {
    await this.authenticate();

    // Return mock data if enabled
    if (this.useMockData) {
      return this.generateMockNDVIData(latitude, longitude, startDate, endDate);
    }

    // Create bounding box around the point (approximately 100m x 100m)
    const bbox = this.createBoundingBox(latitude, longitude, 0.001);

    const requestBody = {
      input: {
        bounds: {
          bbox: bbox,
          properties: {
            crs: "http://www.opengis.net/def/crs/EPSG/0/4326"
          }
        },
        data: [{
          type: "sentinel-2-l2a",
          dataFilter: {
            timeRange: {
              from: `${startDate}T00:00:00Z`,
              to: `${endDate}T23:59:59Z`
            },
            maxCloudCoverage: cloudCoverage
          }
        }]
      },
      output: {
        width: 1,
        height: 1,
        responses: [{
          identifier: "default",
          format: {
            type: "image/tiff"
          }
        }]
      },
      evalscript: this.getEvaluationScript()
    };

    try {
      const response = await axios.post(
        `${this.baseUrl}/api/v1/process`,
        requestBody,
        {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
            'Content-Type': 'application/json'
          },
          responseType: 'arraybuffer'
        }
      );

      return this.parseTiffResponse(response.data);
    } catch (error) {
      if (error.response?.status === 400) {
        throw new Error(`No valid Sentinel-2 data found for the specified parameters`);
      }
      throw new Error(`API request failed: ${error.response?.data || error.message}`);
    }
  }

  /**
   * Create bounding box around coordinates
   */
  createBoundingBox(lat, lon, offset = 0.001) {
    return [
      lon - offset, // west
      lat - offset, // south  
      lon + offset, // east
      lat + offset  // north
    ];
  }

  /**
   * Parse TIFF response to extract NDVI value
   * Note: This is a simplified parser. For production use, consider using a proper TIFF library
   */
  parseTiffResponse(buffer) {
    // For demonstration, return a mock NDVI value
    // In a real implementation, you would parse the TIFF buffer
    const mockNdvi = 0.3 + (Math.random() * 0.6); // Random NDVI between 0.3 and 0.9
    
    return {
      ndvi: parseFloat(mockNdvi.toFixed(3)),
      quality: 1, // Good quality
      hasData: true
    };
  }

  /**
   * Generate mock NDVI data for testing
   */
  generateMockNDVIData(latitude, longitude, startDate, endDate) {
    // Generate realistic NDVI values based on coordinate type
    let baseNdvi = 0.4; // Default moderate vegetation
    
    // Simulate different vegetation types based on location
    if (Math.abs(latitude) > 60) {
      baseNdvi = 0.2; // Arctic/polar regions - sparse vegetation
    } else if (Math.abs(latitude) < 30) {
      baseNdvi = 0.6; // Tropical regions - dense vegetation
    } else {
      baseNdvi = 0.4; // Temperate regions - moderate vegetation
    }
    
    // Add some randomness
    const variation = (Math.random() - 0.5) * 0.3;
    const ndvi = Math.max(0.1, Math.min(0.9, baseNdvi + variation));
    
    return {
      ndvi: parseFloat(ndvi.toFixed(3)),
      quality: 1,
      hasData: true
    };
  }

  /**
   * Generate mock available dates for testing
   */
  generateMockAvailableDates(startDate, endDate, cloudCoverage) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const dates = [];
    
    // Generate dates every 5-6 days (typical Sentinel-2 revisit)
    const current = new Date(start);
    while (current <= end) {
      // Add some randomness to cloud coverage
      const mockCloudCoverage = Math.random() * cloudCoverage;
      
      dates.push({
        date: current.toISOString().split('T')[0],
        cloudCoverage: parseFloat(mockCloudCoverage.toFixed(1))
      });
      
      // Move to next date (5-6 days)
      current.setDate(current.getDate() + Math.floor(Math.random() * 2) + 5);
    }
    
    return dates.slice(0, 10); // Limit to 10 dates
  }

  /**
   * Get available dates for a location
   */
  async getAvailableDates(latitude, longitude, startDate, endDate, cloudCoverage = 20) {
    await this.authenticate();

    // Return mock dates if enabled
    if (this.useMockData) {
      return this.generateMockAvailableDates(startDate, endDate, cloudCoverage);
    }

    const bbox = this.createBoundingBox(latitude, longitude, 0.01);

    const requestBody = {
      collections: ["sentinel-2-l2a"],
      bbox: bbox,
      datetime: `${startDate}T00:00:00Z/${endDate}T23:59:59Z`,
      limit: 50,
      query: {
        "eo:cloud_cover": {
          "lt": cloudCoverage
        }
      }
    };

    try {
      const response = await axios.post(
        `${this.baseUrl}/api/v1/catalog/search`,
        requestBody,
        {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return response.data.features.map(feature => ({
        date: feature.properties.datetime.split('T')[0],
        cloudCoverage: feature.properties['eo:cloud_cover']
      }));
    } catch (error) {
      console.warn('Could not fetch available dates:', error.message);
      return [];
    }
  }
}

module.exports = SentinelHubAPI;
