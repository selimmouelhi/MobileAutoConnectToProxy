"""
Unit Tests for REMA 1000 Staging API
Based on Proxyman traffic analysis
"""

import pytest
import requests
from typing import Optional


# Configuration
BASE_URL = "https://api.staging.digital.rema1000.dk"
API_VERSION = "/api/v1"


class TestConfig:
    """Test configuration - update with valid credentials"""
    AUTH_TOKEN: Optional[str] = None  # Set your Bearer token here
    HEADERS = {
        "Accept": "application/json",
        "Accept-Language": "da-DK;q=1.0, en-DK;q=0.9",
        "User-Agent": "REMA1000App/6.4.2 (iOS 18.6.0; iPhone13,3)",
        "Accept-Encoding": "gzip, deflate, br",
    }

    @classmethod
    def get_headers(cls):
        headers = cls.HEADERS.copy()
        if cls.AUTH_TOKEN:
            headers["Authorization"] = f"Bearer {cls.AUTH_TOKEN}"
        return headers


# ============================================================================
# JOBS-V2 ENDPOINT TESTS
# ============================================================================

class TestJobsV2Endpoint:
    """Tests for /api/v1/jobs-v2 endpoint"""

    ENDPOINT = f"{BASE_URL}{API_VERSION}/jobs-v2"

    def test_jobs_v2_returns_200(self):
        """Test that jobs-v2 endpoint returns 200 OK"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_jobs_v2_response_is_json(self):
        """Test that response is valid JSON"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        assert response.headers.get("Content-Type") == "application/json"
        # Should not raise JSONDecodeError
        data = response.json()
        assert isinstance(data, list), "Response should be a list of jobs"

    def test_jobs_v2_response_time_under_2_seconds(self):
        """Test that response time is acceptable (< 2s)"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        assert response.elapsed.total_seconds() < 2.0, \
            f"Response too slow: {response.elapsed.total_seconds()}s"

    def test_jobs_v2_response_time_under_1_second(self):
        """Test that response time is optimal (< 1s) - may fail on staging"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        assert response.elapsed.total_seconds() < 1.0, \
            f"Response slower than optimal: {response.elapsed.total_seconds()}s"

    def test_jobs_v2_job_structure(self):
        """Test that each job has required fields"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        if len(data) > 0:
            job = data[0]
            required_fields = [
                "id", "type", "status_v2", "user", "delivery_guy",
                "started", "delivered", "completed", "hidden",
                "total_price", "reserve_amount", "items", "extra_items"
            ]
            for field in required_fields:
                assert field in job, f"Missing required field: {field}"

    def test_jobs_v2_job_types_valid(self):
        """Test that job type is one of expected values"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        valid_types = ["collect", "delivery"]
        for job in data:
            assert job.get("type") in valid_types, \
                f"Invalid job type: {job.get('type')}"

    def test_jobs_v2_status_values(self):
        """Test that status_v2 is one of expected values"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        valid_statuses = [
            "pending", "accepted", "shopping", "ready",
            "delivering", "delivered", "completed", "cancelled"
        ]
        for job in data:
            assert job.get("status_v2") in valid_statuses, \
                f"Invalid status: {job.get('status_v2')}"

    def test_jobs_v2_user_structure(self):
        """Test that user object has required fields"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        if len(data) > 0:
            user = data[0].get("user", {})
            required_fields = ["id", "name", "phone", "rating"]
            for field in required_fields:
                assert field in user, f"Missing user field: {field}"

    def test_jobs_v2_delivery_guy_structure(self):
        """Test that delivery_guy object has required fields"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        if len(data) > 0:
            delivery_guy = data[0].get("delivery_guy", {})
            required_fields = ["id", "name", "phone", "rating"]
            for field in required_fields:
                assert field in delivery_guy, f"Missing delivery_guy field: {field}"

    def test_jobs_v2_items_structure(self):
        """Test that items array contains valid item objects"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        if len(data) > 0 and len(data[0].get("items", [])) > 0:
            item = data[0]["items"][0]
            required_fields = [
                "id", "item_id", "amount", "bought", "total_price",
                "name", "category_id", "category_name", "status"
            ]
            for field in required_fields:
                assert field in item, f"Missing item field: {field}"

    def test_jobs_v2_extra_items_structure(self):
        """Test that extra_items (fees) have required fields"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        if len(data) > 0:
            extra_items = data[0].get("extra_items", [])
            valid_codenames = ["packaging", "collect", "delivery"]
            for extra in extra_items:
                assert "name" in extra, "Extra item missing 'name'"
                assert "price" in extra, "Extra item missing 'price'"
                assert "codename" in extra, "Extra item missing 'codename'"
                assert extra["codename"] in valid_codenames, \
                    f"Invalid codename: {extra['codename']}"

    def test_jobs_v2_price_calculations(self):
        """Test that reserve_amount >= total_price (20% buffer)"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        for job in data:
            total = job.get("total_price", 0)
            reserve = job.get("reserve_amount", 0)
            assert reserve >= total, \
                f"Reserve ({reserve}) should be >= total ({total})"

    def test_jobs_v2_unauthorized_without_token(self):
        """Test that endpoint requires authentication"""
        response = requests.get(
            self.ENDPOINT,
            params={"as": "user", "limited": 1},
            headers={"Accept": "application/json"},
            timeout=10
        )
        assert response.status_code in [401, 403], \
            f"Expected 401/403 without auth, got {response.status_code}"


# ============================================================================
# SHOPPING LISTS POLLING ENDPOINT TESTS
# ============================================================================

class TestShoppingListsPolling:
    """Tests for /api/v1/shoppinglists/polling endpoint"""

    ENDPOINT = f"{BASE_URL}{API_VERSION}/shoppinglists/polling"

    def test_polling_returns_200(self):
        """Test that polling endpoint returns 200 OK"""
        import time
        response = requests.get(
            self.ENDPOINT,
            params={"unixtime": int(time.time())},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_polling_response_time_under_500ms(self):
        """Test that polling response is fast (< 500ms)"""
        import time
        response = requests.get(
            self.ENDPOINT,
            params={"unixtime": int(time.time())},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        assert response.elapsed.total_seconds() < 0.5, \
            f"Polling too slow: {response.elapsed.total_seconds()}s"

    def test_polling_response_is_json(self):
        """Test that polling response is valid JSON"""
        import time
        response = requests.get(
            self.ENDPOINT,
            params={"unixtime": int(time.time())},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        assert "application/json" in response.headers.get("Content-Type", "")
        response.json()  # Should not raise

    def test_polling_with_old_timestamp(self):
        """Test polling with old timestamp returns updates"""
        response = requests.get(
            self.ENDPOINT,
            params={"unixtime": 0},  # Very old timestamp
            headers=TestConfig.get_headers(),
            timeout=10
        )
        assert response.status_code == 200

    def test_polling_unauthorized_without_token(self):
        """Test that polling requires authentication"""
        import time
        response = requests.get(
            self.ENDPOINT,
            params={"unixtime": int(time.time())},
            headers={"Accept": "application/json"},
            timeout=10
        )
        assert response.status_code in [401, 403], \
            f"Expected 401/403 without auth, got {response.status_code}"


# ============================================================================
# KILLSWITCH ENDPOINT TESTS
# ============================================================================

class TestKillswitch:
    """Tests for the killswitch status endpoint"""

    ENDPOINT = "https://rema1000-killswitch.plus.shape.dk/status"

    def test_killswitch_status(self):
        """Test killswitch endpoint availability"""
        response = requests.get(
            self.ENDPOINT,
            params={
                "platform": "ios",
                "bundleIdentifier": "dk.rema1000.vigotestflight",
                "versionNumber": "6.4.2"
            },
            timeout=10
        )
        # Currently returning 404 - this test documents the issue
        assert response.status_code == 200, \
            f"Killswitch returning {response.status_code} - needs investigation"


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestAPIPerformance:
    """Performance and load tests"""

    def test_jobs_v2_multiple_requests_consistency(self):
        """Test that multiple requests return consistent response times"""
        times = []
        for _ in range(5):
            response = requests.get(
                f"{BASE_URL}{API_VERSION}/jobs-v2",
                params={"as": "user", "limited": 1},
                headers=TestConfig.get_headers(),
                timeout=10
            )
            times.append(response.elapsed.total_seconds())

        avg_time = sum(times) / len(times)
        max_time = max(times)

        assert avg_time < 2.0, f"Average response time too high: {avg_time}s"
        assert max_time < 3.0, f"Max response time too high: {max_time}s"

    def test_polling_multiple_requests_consistency(self):
        """Test polling endpoint consistency"""
        import time
        times = []
        for _ in range(5):
            response = requests.get(
                f"{BASE_URL}{API_VERSION}/shoppinglists/polling",
                params={"unixtime": int(time.time())},
                headers=TestConfig.get_headers(),
                timeout=10
            )
            times.append(response.elapsed.total_seconds())

        avg_time = sum(times) / len(times)
        assert avg_time < 0.5, f"Average polling time too high: {avg_time}s"


# ============================================================================
# DATA VALIDATION TESTS
# ============================================================================

class TestDataValidation:
    """Data integrity and validation tests"""

    def test_job_id_is_positive_integer(self):
        """Test that job IDs are positive integers"""
        response = requests.get(
            f"{BASE_URL}{API_VERSION}/jobs-v2",
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        for job in data:
            assert isinstance(job["id"], int), "Job ID should be integer"
            assert job["id"] > 0, "Job ID should be positive"

    def test_prices_are_non_negative(self):
        """Test that prices are non-negative numbers"""
        response = requests.get(
            f"{BASE_URL}{API_VERSION}/jobs-v2",
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        for job in data:
            assert job.get("total_price", 0) >= 0, "Total price should be >= 0"
            assert job.get("reserve_amount", 0) >= 0, "Reserve amount should be >= 0"

            for item in job.get("items", []):
                assert item.get("total_price", 0) >= 0, \
                    f"Item price should be >= 0: {item.get('name')}"

    def test_phone_numbers_format(self):
        """Test that phone numbers follow expected format"""
        import re
        response = requests.get(
            f"{BASE_URL}{API_VERSION}/jobs-v2",
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        phone_pattern = re.compile(r'^\+\d{10,15}$')
        for job in data:
            user_phone = job.get("user", {}).get("phone")
            if user_phone:
                assert phone_pattern.match(user_phone), \
                    f"Invalid phone format: {user_phone}"

    def test_ratings_in_valid_range(self):
        """Test that ratings are between 0 and 5"""
        response = requests.get(
            f"{BASE_URL}{API_VERSION}/jobs-v2",
            params={"as": "user", "limited": 1},
            headers=TestConfig.get_headers(),
            timeout=10
        )
        data = response.json()

        for job in data:
            user_rating = job.get("user", {}).get("rating", 0)
            dg_rating = job.get("delivery_guy", {}).get("rating", 0)

            assert 0 <= user_rating <= 5, f"Invalid user rating: {user_rating}"
            assert 0 <= dg_rating <= 5, f"Invalid delivery_guy rating: {dg_rating}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
