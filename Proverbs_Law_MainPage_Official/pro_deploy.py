import subprocess
import os

class ProDeployer:
    """
    Automated Deployment Engine for the ProVerBs 'Pro Set Up'.
    Targets: GCP Cloud Run + Artifact Registry.
    """
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", "proverbs-legal-ai")
        self.region = "us-central1" # High-availability legal research region
        self.service_name = "proverbs-ultimate-brain"

    def execute_deployment(self):
        """
        Executes the 'Gigantically Robust' deployment sequence.
        """
        print(f"--- Initiating Pro Set Up Deployment for: {self.service_name} ---")
        
        # 1. Build and Tag the Production Image
        image_tag = f"gcr.io/{self.project_id}/{self.service_name}:latest"
        print(f"[Build] Global Production Image: {image_tag}")
        subprocess.run(["docker", "build", "-t", image_tag, "."], check=True)
        
        # 2. Push to Google Artifact Registry
        print(f"[Registry] Pushing to Artifact Registry...")
        subprocess.run(["docker", "push", image_tag], check=True)
        
        # 3. Deploy to Cloud Run with Pro-Scaling
        print(f"[Cloud Run] Scaling Live (Status-Aware Mode)...")
        deploy_cmd = [
            "gcloud", "run", "deploy", self.service_name,
            "--image", image_tag,
            "--platform", "managed",
            "--region", self.region,
            "--allow-unauthenticated",
            "--memory", "4Gi",
            "--cpu", "2",
            "--min-instances", "1",
            "--max-instances", "10",
            "--set-env-vars", f"GCP_PROJECT_ID={self.project_id},PYTHONUNBUFFERED=1"
        ]
        subprocess.run(deploy_cmd, check=True)
        
        print(f"DONE: Deployment Complete: {self.service_name} is LIVE.")

if __name__ == "__main__":
    deployer = ProDeployer()
    deployer.execute_deployment()
