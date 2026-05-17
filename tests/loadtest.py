import random
import logging
from locust import HttpUser, task, between
from locust.env import Environment
from locust.stats import stats_printer, stats_history

class FraudApiUser(HttpUser):
    # Simulated delay between requests
    wait_time = between(0.5, 2)

    @task(4)
    def send_normal_transaction(self):
        """Generates mock normal data following your dataset's exact profile."""
        payload = {
            "data": {
                "V1": random.gauss(0.0, 1.95), "V2": random.gauss(0.0, 1.65),
                "V3": random.gauss(0.0, 1.51), "V4": random.gauss(0.0, 1.41),
                "V5": random.gauss(0.0, 1.38), "V6": random.gauss(0.0, 1.33),
                "V7": random.gauss(0.0, 1.23), "V8": random.gauss(0.0, 1.19),
                "V9": random.gauss(0.0, 1.09), "V10": random.gauss(0.0, 1.08),
                "V11": random.gauss(0.2, 1.1), "V12": random.gauss(0.3, 1.2),
                "V13": random.gauss(0.0, 1.0), "V14": random.gauss(0.0, 0.9),
                "V15": random.gauss(0.0, 1.1), "V16": random.gauss(0.0, 0.8),
                "V17": random.gauss(0.0, 0.7), "V18": random.gauss(0.1, 1.0),
                "V19": random.gauss(0.0, 1.2), "V20": random.gauss(0.0, 0.5),
                "V21": random.gauss(0.0, 0.73), "V22": random.gauss(0.0, 0.72),
                "V23": random.gauss(0.0, 0.62), "V24": random.gauss(0.0, 0.60),
                "V25": random.gauss(0.0, 0.52), "V26": random.gauss(0.0, 0.48),
                "V27": random.gauss(0.0, 0.40), "V28": random.gauss(0.0, 0.33),
                "Amount": random.gauss(-0.26, 1.0)
            }
        }
        self.client.post("/transaction", json=payload)

    @task(1)
    def send_fraudulent_anomaly(self):
        """Generates extreme outliers designed to trigger model alerts."""
        payload = {
            "data": {
                "V1": random.uniform(-20.0, -50.0), "V2": random.uniform(10.0, 20.0),
                "V3": random.uniform(-25.0, -45.0), "V4": random.uniform(5.0, 15.0),
                "V5": random.uniform(-10.0, -30.0), "V6": random.uniform(-5.0, -15.0),
                "V7": random.uniform(-20.0, -40.0), "V8": random.uniform(5.0, 18.0),
                "V9": random.uniform(-5.0, -12.0), "V10": random.uniform(-10.0, -24.0),
                "V11": random.uniform(5.0, 12.0), "V12": random.uniform(-10.0, -18.0),
                "V13": random.uniform(-3.0, -6.0), "V14": random.uniform(-8.0, -19.0),
                "V15": random.uniform(-4.0, -8.0), "V16": random.uniform(-6.0, -14.0),
                "V17": random.uniform(-10.0, -25.0), "V18": random.uniform(-4.0, -9.0),
                "V19": random.uniform(2.0, 6.0), "V20": random.uniform(5.0, 20.0),
                "V21": random.uniform(5.0, 25.0), "V22": random.uniform(-4.0, 10.0),
                "V23": random.uniform(-10.0, 20.0), "V24": random.uniform(-1.0, 4.0),
                "V25": random.uniform(-2.0, 7.0), "V26": random.uniform(-1.0, 3.0),
                "V27": random.uniform(1.0, 30.0), "V28": random.uniform(1.0, 30.0),
                "Amount": random.uniform(60.0, 102.0)
            }
        }
        self.client.post("/transaction", json=payload)


# ==========================================
# 2. PROGRAMMATIC RUNNER SETUP
# ==========================================
if __name__ == "__main__":
    # Setup standard terminal logging
    logging.basicConfig(level=logging.INFO)

    # 1. Setup the runtime environment and link your user behavior class
    env = Environment(user_classes=[FraudApiUser])
    
    # Set the target endpoint host (your FastAPI gateway)
    env.host = "http://127.0.0.1:8000"

    # 2. Initialize the runner infrastructure
    env.create_local_runner()

    # 3. Start the Web Dashboard with strict local loopback isolation
    # This prevents anyone on your local network/Wi-Fi from seeing it.
    web_ui = env.create_web_ui(
        host="127.0.0.1", 
        port=8089
    )

    env.runner.start(user_count=200, spawn_rate=5)

    print("\n" + "="*50)
    print(" SECURITY NOTICE: Dashboard locked strictly to localhost.")
    print(" Open your browser and go to: http://127.0.0.1:8089")
    print("="*50 + "\n")

    # 4. Keep the python process alive while the web UI runs
    try:
        env.runner.greenlet.join()
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C exit
        print("\nStopping load test environment...")
        web_ui.stop()
        env.runner.quit()