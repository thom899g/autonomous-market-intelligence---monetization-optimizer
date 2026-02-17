import pandas as pd
import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DataCollector:
    """Collects market data from various sources"""
    
    def __init__(self, config):
        self.config = config
        self.api_keys = self.config.get_api_keys()
        
    def collect_data(self) -> Dict:
        """Main method to collect market data"""
        try:
            # Historical data collection
            historical_data = self._get_historical_data()
            
            # Real-time data collection
            real_time_data = self._get_real_time_data()
            
            return {
                "historical": historical_data,
                "real_time": real_time_data
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Data collection failed: {str(e)}")
            raise
        
    def _get_historical_data(self) -> pd.DataFrame:
        """Collects historical market data"""
        params = {
            "api_key": self.api_keys["alphavantage"],
            "start_date": (datetime.now() - timedelta(days=365)).isoformat(),
            "end_date": datetime.now().isoformat()
        }
        
        response = requests.get(self.config.HISTORICAL_DATA_ENDPOINT, params=params)
        if not response.ok:
            raise Exception(f"Failed to fetch historical data: {response.text}")
            
        return pd.DataFrame(response.json()["data"])
    
    def _get_real_time_data(self) -> Dict:
        """Collects real-time market data"""
        response = requests.get(self.config.REAL_TIME_DATA_ENDPOINT, 
                              params={"api_key": self.api_keys["alphavantage"]})
        
        if not response.ok:
            raise Exception(f"Failed to fetch real-time data: {response.text}")
            
        return response.json()