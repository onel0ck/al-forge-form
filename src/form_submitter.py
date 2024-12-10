import requests
import random
import time
import json
from typing import Dict, Any
from loguru import logger
import uuid
from urllib.parse import urlencode
from config import FORM_ID, FORM_BASE_URL, TIMEOUT_BETWEEN_REQUESTS

class TypeformSubmitter:
    def __init__(self):
        self.base_url = FORM_BASE_URL
        self.form_id = FORM_ID
        self.user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
        self.response_id = None
        self.signature = None
        self.landed_at = None
        
    def create_session(self, proxy: str = None) -> None:
        self.session = requests.Session()
        
        if proxy:
            self.session.proxies = {
                "http": proxy,
                "https": proxy
            }
            logger.info(f"Using proxy: {proxy}")
            
            try:
                test_response = self.session.get(
                    f"{self.base_url}/to/{self.form_id}",
                    timeout=10
                )
                test_response.raise_for_status()
                logger.info("Proxy connection successful")
            except Exception as e:
                logger.error(f"Proxy test failed: {str(e)}")
                raise Exception(f"Failed to connect using proxy {proxy}")

        self.session.headers.update({
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': self.base_url,
            'priority': 'u=1, i',
            'referer': f'{self.base_url}/to/{self.form_id}?utm_source=landing-page&typeform-source=forge.allora.network',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'Cookie': 'tf_respondent_cc={"groups":["2","3","4"],"timestamp":"2024-12-06T04:22:14.626Z","implicitConsent":true}'
        })

    def _add_delay(self) -> None:
        time.sleep(random.uniform(TIMEOUT_BETWEEN_REQUESTS, TIMEOUT_BETWEEN_REQUESTS * 1.5))

    def record_form_open(self) -> None:
        url = f"{self.base_url}/forms/{self.form_id}/insights/performance/view-form-open"
        
        self.session_response_id = f"5j5CKjms{str(uuid.uuid4())[:4]}"
        
        payload = {
            'form_id': self.form_id,
            'field_id': 'WelcomeScreenID',
            'response_id': self.session_response_id,
            'user_agent': self.user_agent,
            'running_experiments': '[{"test_id":"AB_PulseSurvey_Respond_RESP-1091","variant_label":"out_of_experiment"},{"test_id":"AB_Rosetta_Cache_Respond_RESP-2532","variant_label":"variant"}]',
            'utm': '[{"name":"source","value":"landing-page"}]',
            'version': '1'
        }

        try:
            self.session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            })

            logger.debug("Sending request with payload:")
            logger.debug(json.dumps(payload, indent=2))

            encoded_payload = urlencode(payload)
            logger.debug(f"Encoded payload: {encoded_payload}")
            
            response = self.session.post(url, data=encoded_payload)
            
            logger.debug(f"Request URL: {response.request.url}")
            logger.debug(f"Request headers: {response.request.headers}")
            logger.debug(f"Request body: {response.request.body}")
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            response.raise_for_status()
            self._add_delay()
        except Exception as e:
            logger.error(f"Error in record_form_open: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Response content: {e.response.text}")
                logger.error(f"Request headers: {e.response.request.headers}")
                logger.error(f"Request body: {e.response.request.body}")
            raise

    def start_submission(self) -> None:
        url = f"{self.base_url}/forms/{self.form_id}/start-submission"
        
        self.session.headers.update({
            'content-type': 'application/json; charset=UTF-8',
            'accept': 'application/json'
        })
        
        payload = {
            "visit_response_id": self.session_response_id
        }
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            self.signature = data["signature"]
            self.response_id = data["submission"]["response_id"]
            self.landed_at = data["submission"]["landed_at"]
            
            self._add_delay()
        except Exception as e:
            logger.error(f"Error in start_submission: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Response content: {e.response.text}")
            raise

    def record_field_view(self, field_id: str, previous_field_id: str) -> None:
        url = f"{self.base_url}/forms/{self.form_id}/insights/performance/see"
        
        self.session.headers['content-type'] = 'application/x-www-form-urlencoded'
        
        payload = {
            'form_id': self.form_id,
            'field_id': field_id,
            'previous_seen_field_id': previous_field_id,
            'response_id': self.session_response_id,
            'user_agent': self.user_agent,
            'version': '1'
        }
        
        try:
            response = self.session.post(url, data=payload)
            response.raise_for_status()
            self._add_delay()
        except Exception as e:
            logger.error(f"Error in record_field_view: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Response content: {e.response.text}")
            raise

    def submit_form(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        url = f"{self.base_url}/forms/{self.form_id}/complete-submission"
        
        self.session.headers.update({
            'content-type': 'application/json; charset=UTF-8',
            'accept': 'application/json'
        })
        
        field_mapping = {
            "nickname": "IABEnTmQY6XJ",
            "firstname": "VInp2vt8Y6er",
            "wallet": "Wa4FcochMjId",
            "email": "UtZXZuDeWDER",
            "discord": "D3Nx1NCQk3GJ",
            "telegram": "g1FpcqMGptS8",
            "linkedin": "jiQxI27EPUhM",
            "twitter": "vGL12L9rRVJo",
            "huggingface": "Rp8dzVXdOx3W",
            "kaggle": "SRY6nUrw9qOE",
            "github": "Xk1xui1hPOJB"
        }

        answers = []
        for field, value in form_data.items():
            if field in field_mapping:
                answer = {
                    "field": {
                        "id": field_mapping[field],
                        "type": "email" if field == "email" else "short_text"
                    },
                    "type": "email" if field == "email" else "text"
                }
                if field == "email":
                    answer["email"] = value
                else:
                    answer["text"] = value
                answers.append(answer)

        payload = {
            "signature": self.signature,
            "form_id": self.form_id,
            "landed_at": self.landed_at,
            "answers": answers,
            "hidden": [{"key": "utm_source", "value": "landing-page"}],
            "thankyou_screen_ref": "16c4ad63-fac7-4150-aee8-7ad821f8951b"
        }

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error in submit_form: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Response content: {e.response.text}")
            raise

    def submit_full_form(self, form_data: Dict[str, str], proxy: str = None) -> Dict[str, Any]:
        try:
            self.create_session(proxy)
            self.record_form_open()
            self.start_submission()
            
            fields = [
                ("WelcomeScreenID", "EtmUJQ6fWwpi"),
                ("EtmUJQ6fWwpi", "xdOdVWGwJESm"),
                ("xdOdVWGwJESm", "EndingID")
            ]
            
            for prev_field, current_field in fields:
                self.record_field_view(current_field, prev_field)
                self._add_delay()
            
            result = self.submit_form(form_data)
            return result
            
        except Exception as e:
            logger.error(f"Error submitting form: {str(e)}")
            return {"error": str(e)}