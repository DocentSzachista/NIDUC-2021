#Class that gathers communication statistics
class Statistics:
    def __init__(self) -> None:
        self.min_packages = 0
        self.ammount_of_packets = 0
        self.detected_errors = 0
        self.undetected_errors = 0

    def get_statistics(self) -> str:
        stats = f"Minimum amount of packages: {self.min_packages}\n"
        stats += f"Packets exchanged: {self.ammount_of_packets}\n"
        stats += f"Detected errors: {self.detected_errors}\n"
        stats += f"Undetected errors: {self.undetected_errors}\n"
        return stats

    def add_statistics(self, stats_to_add) -> None:
        self.min_packages += stats_to_add.min_packages
        self.ammount_of_packets += stats_to_add.ammount_of_packets
        self.detected_errors += stats_to_add.detected_errors
        self.undetected_errors += stats_to_add.undetected_errors
