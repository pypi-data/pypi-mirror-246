# chrome_manager.py
from azucar_web_driver.chrome_factory import ChromeFactory

class ChromeManager:
    def __init__(self):
        self.instances = []

    def create_new_instance(self, use_profile=False):
        new_instance = ChromeFactory.create_instance(use_profile)
        self.instances.append(new_instance)
        return new_instance

    def close_all_instances(self):
        for instance in self.instances:
            instance.quit()
        self.instances = []