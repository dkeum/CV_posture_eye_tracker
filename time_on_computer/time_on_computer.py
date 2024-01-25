import time

class TimeTrack:
    def __init__(self):
        self.break_time = 5  # 5 minutes
        self.reminder_interval = 120 # 2 hours 
        self.break_time_2 = 20  # 20 seconds
        self.reminder_interval_2 = 20 # 20 mins

        # reference for numbers: https://www.webmd.com/eye-health/eye-fatigue-causes-symptoms-treatment

        self.start_time_20min = time.time()  # Record the initial time
        self.start_time_3hr = time.time()  # Record the initial time

    def has_three_hours_passed(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time_3hr

        # Check if 3 hours (180 minutes) have passed
        return elapsed_time >= self.reminder_interval * 60
    
    def has_20_min_passed(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time_20min

        # Check if 20 minutes have passed
        return elapsed_time >= self.reminder_interval_2 * 60  # 20 minutes in seconds

    def main(self, shared_resource=None):


        while not shared_resource.app_exit:
            if shared_resource is not None:
                if self.has_20_min_passed():
                    
                    if self.has_three_hours_passed():
                        shared_resource.message_to_display2 = "5 min break"
                        time.sleep(1)
                        
                        # Calculate the end time for the break
                        end_break_time = time.time() + self.break_time * 60

                        while time.time() < end_break_time:
                            remaining_time = int(end_break_time - time.time())
                            minutes = remaining_time // 60
                            seconds = remaining_time % 60

                            shared_resource.message_to_display2 = f"Countdown: {minutes} min {seconds} sec"
                            time.sleep(1)
                        
                        self.start_time_3hr = time.time()
                            
                        # shared_resource.message_to_display2 = ""
                    else:
                        print("20 sec eye break")
                        # Calculate the end time for the break
                        end_break_time = time.time() + self.break_time_2

                        while time.time() < end_break_time:
                            remaining_time = int(end_break_time - time.time())
                            seconds = remaining_time % 60
                            shared_resource.message_to_display2 = f"Countdown: {seconds} sec"
                            time.sleep(1)
                        
                        self.start_time_20min = time.time()

                shared_resource.message_to_display2 = "Focus Mode"
            
            # check in every 20 mins
            time.sleep(1)
        


if __name__ == "__main__":
    # Example usage
    time_tracker = TimeTrack()
    time_tracker.main()
