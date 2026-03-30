import os
import shutil

def create_structure():
    base_dir = "customer_support_agent"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    # Services
    services = ["knowledge_base", "ticket_retrieval", "chat_agent", "feedback"]
    for service in services:
        service_dir = os.path.join(base_dir, "services", service)
        os.makedirs(os.path.join(service_dir, "app"))
        os.makedirs(os.path.join(service_dir, "app", "routes"))
        os.makedirs(os.path.join(service_dir, "app", "models"))
        os.makedirs(os.path.join(service_dir, "app", "utils"))

        # Create __init__.py files
        for sub in ["routes", "models", "utils"]:
            with open(os.path.join(service_dir, "app", sub, "__init__.py"), "w") as f:
                f.write("")

        # Main files
        with open(os.path.join(service_dir, "app", "__init__.py"), "w") as f:
            f.write("")
        with open(os.path.join(service_dir, "app", "main.py"), "w") as f:
            f.write("")
        with open(os.path.join(service_dir, "requirements.txt"), "w") as f:
            f.write("")
        with open(os.path.join(service_dir, "Dockerfile"), "w") as f:
            f.write("")

    # UI
    ui_dir = os.path.join(base_dir, "ui")
    os.makedirs(ui_dir)
    with open(os.path.join(ui_dir, "app.py"), "w") as f:
        f.write("")
    with open(os.path.join(ui_dir, "requirements.txt"), "w") as f:
        f.write("")

    # Shared
    shared_dir = os.path.join(base_dir, "shared")
    os.makedirs(shared_dir)
    with open(os.path.join(shared_dir, "config.yml"), "w") as f:
        f.write("")
    with open(os.path.join(shared_dir, "database.py"), "w") as f:
        f.write("")
    with open(os.path.join(shared_dir, "models.py"), "w") as f:
        f.write("")

    # Root files
    with open(os.path.join(base_dir, "docker-compose.yml"), "w") as f:
        f.write("")
    with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
        f.write("")
    with open(os.path.join(base_dir, "setup_structure.py"), "w") as f:
        f.write("")

    print("Project structure created successfully!")

if __name__ == "__main__":
    create_structure()