# ⚜️ Sovereign Traffic Strategy

## Overview
Sovereign Traffic is the automated scaling engine of the Nectar Suprema ecosystem. It monitors the ROI of each colonized niche and adjusts advertising budgets in real-time to maximize profit and minimize waste.

## How it Works
The system follows a recursive optimization loop:
1. **Data Acquisition**: Reads target ROI for each niche from `niche_roi.json` (managed by Nexus Core).
2. **Performance Analysis**: Fetches current ROI from Ads APIs (currently simulated).
3. **Scaling Decisions**:
    *   **ROI >= Target + 20%**: Aggressive Scale (+50% budget).
    *   **ROI > Target**: Moderate Scale (+20% budget).
    *   **ROI < Target**: Moderate Cut (-20% budget).
    *   **ROI <= Target - 30%**: Critical Stop (Pause campaign).
4. **Execution**: Applies changes to Ad Accounts and logs actions in `ad_accounts.json`.

## Usage
To run a manual optimization cycle:
```bash
python3 src/sovereign-entity/sovereign_traffic.py
```

## Future Integrations
- [ ] Direct integration with Meta Ads API (Graph API).
- [ ] Direct integration with Google Ads API.
- [ ] Audience auto-refinement based on conversion demographic data.
- [ ] Creative rotation (A/B testing) triggered by CTR drops.

---
*Developed by the Growth Hacker ⚜️*
