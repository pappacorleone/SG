import os
import matplotlib.pyplot as plt
from PIL import Image

def generate_weekly_summary(tasks, habits):
    # Get the data for the tasks and habits
    task_names = [task[0] for task in tasks]
    task_statuses = [task[3] for task in tasks]
    habit_names = [habit[0] for habit in habits]
    habit_statuses = [habit[3] for habit in habits]
    
    # Create the pie chart for the tasks
    plt.pie(task_statuses, labels=task_names, shadow=True)
    plt.title("Weekly Task Summary")
    plt.savefig("task_summary.png")
    
    # Create the pie chart for the habits
    plt.pie(habit_statuses, labels=habit_names, shadow=True)
    plt.title("Weekly Habit Summary")
    plt.savefig("habit_summary.png")
    
    # Combine the two images into one
    images = [Image.open(x) for x in ["task_summary.png", "habit_summary.png"]]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_image = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for image in images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.size[0]
    new_image.save("weekly_summary.png")
    
    # Delete the individual images
    os.remove("task_summary.png")
    os.remove("habit_summary.png")
