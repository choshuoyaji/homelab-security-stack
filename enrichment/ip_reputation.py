import requests
import json

class ThreatEnrichment:
    """Threat intelligence enrichment for IP addresses."""
    
    def __init__(self, config):
        self.vt_api_key = config.get("virustotal_api_key")
        self.abuseipdb_key = config.get("abuseipdb_api_key")
    
    def check_ip_reputation(self, ip_address):
        """Check IP against multiple threat intel sources."""
        results = {
            "ip": ip_address,
            "threat_score": 0,
            "sources": [],
            "mitre_techniques": []
        }
        
        abuse_score = self._check_abuseipdb(ip_address)
        if abuse_score is not None:
            results["sources"].append({"name": "AbuseIPDB", "score": abuse_score})
        
        vt_score = self._check_virustotal(ip_address)
        if vt_score is not None:
            results["sources"].append({"name": "VirusTotal", "score": vt_score})
        
        scores = [s["score"] for s in results["sources"]]
        if scores:
            results["threat_score"] = sum(scores) / len(scores)
        
        return results
    
    def _check_abuseipdb(self, ip):
        """Query AbuseIPDB API."""
        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {"Key": self.abuseipdb_key, "Accept": "application/json"}
        params = {"ipAddress": ip, "maxAgeInDays": 90}
        
        try:
            resp = requests.get(url, headers=headers, params=params)
            data = resp.json()
            return data["data"]["abuseConfidenceScore"]
        except Exception as e:
            print(f"AbuseIPDB error: {e}")
            return None
    
    def _check_virustotal(self, ip):
        """Query VirusTotal API."""
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"x-apikey": self.vt_api_key}
        
        try:
            resp = requests.get(url, headers=headers)
            data = resp.json()
            stats = data["data"]["attributes"]["last_analysis_stats"]
            malicious = stats.get("malicious", 0)
            total = sum(stats.values())
            return int((malicious / total) * 100) if total > 0 else 0
        except Exception as e:
            print(f"VirusTotal error: {e}")
            return None
