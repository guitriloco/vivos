import os, json, time
def main():
    while True:
        print(json.dumps({"pulse": "ACTIVE", "aggregate": "MUTANT-NECTAR", "ts": time.time()}))
        time.sleep(60)
if __name__ == "__main__": main()
