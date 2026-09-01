import json
import os
import time
import random
from datetime import datetime

class SovereignTraffic:
    """
    Sovereign Traffic: The specialized module for automated traffic scaling.
    Responsible for adjusting budgets and audiences based on ROI data.
    """
    def __init__(self, repo_root=None):
        if repo_root is None:
            # Try to detect repo root
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # We assume this script is in src/sovereign-entity/
            self.repo_root = os.path.abspath(os.path.join(script_dir, "../.."))
        else:
            self.repo_root = repo_root
            
        self.roi_file_path = os.path.join(self.repo_root, "src/sovereign-entity/AETHER_FLOW/Intelligence_Report/niche_roi.json")
        self.ad_accounts_path = os.path.join(self.repo_root, "src/sovereign-entity/AETHER_FLOW/Intelligence_Report/ad_accounts.json")
        
        self.load_roi_data()
        self.load_ad_accounts()

    def load_roi_data(self):
        if os.path.exists(self.roi_file_path):
            try:
                with open(self.roi_file_path, 'r') as f:
                    self.roi_data = json.load(f)
            except Exception as e:
                print(f"Error loading ROI data: {e}")
                self.roi_data = {}
        else:
            print(f"ROI file not found at {self.roi_file_path}")
            self.roi_data = {}

    def load_ad_accounts(self):
        if os.path.exists(self.ad_accounts_path):
            try:
                with open(self.ad_accounts_path, 'r') as f:
                    self.ad_accounts = json.load(f)
            except Exception as e:
                print(f"Error loading Ad Accounts: {e}")
                self.ad_accounts = {}
        else:
            self.ad_accounts = {}
            # Initialize if empty
            for niche in self.roi_data:
                self.ad_accounts[niche] = {
                    "budget": 100.0,
                    "status": "ACTIVE",
                    "audience": "Broad",
                    "last_action": "INITIALIZED"
                }
            self.save_ad_accounts()

    def save_ad_accounts(self):
        try:
            os.makedirs(os.path.dirname(self.ad_accounts_path), exist_ok=True)
            with open(self.ad_accounts_path, 'w') as f:
                json.dump(self.ad_accounts, f, indent=4)
        except Exception as e:
            print(f"Error saving Ad Accounts: {e}")

    def scale_logic(self, niche, current_roi, target_roi):
        if niche not in self.ad_accounts:
            self.ad_accounts[niche] = {"budget": 100.0, "status": "ACTIVE", "audience": "Broad"}
            
        account = self.ad_accounts[niche]
        budget = account.get("budget", 100.0)
        action = ""
        
        # Avoid division by zero
        if target_roi <= 0: target_roi = 0.85
        
        roi_diff = (current_roi - target_roi) / target_roi
        
        if roi_diff >= 0.2:
            # ROI is 20%+ above target -> AGGRESSIVE SCALE
            new_budget = budget * 1.5
            action = f"AGGRESSIVE SCALE (+50%)"
            account["budget"] = round(new_budget, 2)
            account["status"] = "ACTIVE"
        elif roi_diff > 0:
            # ROI is above target -> MODERATE SCALE
            new_budget = budget * 1.2
            action = f"MODERATE SCALE (+20%)"
            account["budget"] = round(new_budget, 2)
            account["status"] = "ACTIVE"
        elif roi_diff > -0.3:
            # ROI is below target but not disastrous -> MODERATE CUT
            new_budget = budget * 0.8
            action = f"MODERATE CUT (-20%)"
            account["budget"] = round(new_budget, 2)
            account["status"] = "ACTIVE"
        else:
            # ROI is 30%+ below target -> STOP
            action = f"CRITICAL STOP"
            account["budget"] = 0
            account["status"] = "PAUSED"

        account["last_action"] = action
        account["last_roi"] = round(current_roi, 2)
        account["timestamp"] = str(datetime.now())
        return action

    def optimize(self):
        print(f"--- ⚜️ SOVEREIGN TRAFFIC OPTIMIZATION CYCLE: {datetime.now()} ---")
        self.load_roi_data() # Reload to get latest from AI Architect
        
        results = []
        for niche, data in self.roi_data.items():
            target_roi = data.get("target_roi", 0.85)
            
            # Simulate fetching current ROI from a real source
            # In a real setup, this would call Meta/Google Ads API
            current_roi = target_roi + random.uniform(-0.4, 0.4)
            
            action = self.scale_logic(niche, current_roi, target_roi)
            print(f"[{niche:30}] ROI: {current_roi:.2f} (Target: {target_roi}) -> {action}")
            results.append({"niche": niche, "roi": current_roi, "action": action})
        
        self.save_ad_accounts()
        return results

if __name__ == "__main__":
    st = SovereignTraffic()
    st.optimize()
