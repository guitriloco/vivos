class ValueDistiller:
    def process(self, signals):
        print(f"[Value_Hyper] Applying Recursive Distillation to {len(signals)} signals...")
        # Only extract the 'Technical Gold'
        distilled = [s for s in signals if s['roi'] > 0.90]
        for s in distilled:
            s['strategy'] = "ABSOLUTE_DOMINANCE"
        return distilled
distiller = ValueDistiller()
