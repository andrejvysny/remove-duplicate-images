import tkinter as tk
from PIL import Image, ImageTk
import os
from PIL import Image, ImageChops


mainDirectory = "Camera"
secondaryDirectory = "Camera1"
autoRemove=True


def on_button_click_rename(image_path):
    oldPath = mainDirectory + "/" + image_path
    newPath = mainDirectory + "/RENAMED_" + image_path
    try:
        os.rename(oldPath, newPath)
        print(f"[RENAME] File '{oldPath}' has been renamed to '{newPath}'.")
    except FileNotFoundError:
        print(f"Error: The file '{oldPath}' does not exist.")
    except OSError as e:
        print(f"Error: {e}")
    root.destroy() 


def on_button_click_remove(direcoryToRemove,image_path):
    file_path = direcoryToRemove + "/" + image_path
    try:
        os.remove(file_path)
        print(f"[KEEP] File '{file_path}' has been removed.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except OSError as e:
        print(f"Error: {e}")
    root.destroy()


def on_button_click_skip(image_path):
    print(f"[SKIP] - " + image_path)
    root.destroy() 

def determine_images_difference(image_path):
    img1 = Image.open(mainDirectory+"/"+image_path)
    img2 = Image.open(secondaryDirectory+"/"+image_path)
    try:
        if img1.size != img2.size or img1.mode != img2.mode or img1.format != img2.format:
            print("[DIFF] Size|mode|format")
            return "DIFFERENT"
        else:
            diff = ImageChops.difference(img1, img2)
            if diff.getbbox() is None:
                if autoRemove:
                    return "AUTO_REMOVE"
                return "SAME"
            else:
                print("[DIFF] PixelDiff")
                return "DIFFERENT"
    except Exception as e:
        print(f"Error - {image_path} - Error: {e}")
        return "N/A"
    


def create_image_frame(image_path, side, currentDirectory, otherDirectory):
    # Load the image using Pillow
    image = Image.open(currentDirectory + "/" + image_path)
    thumbnail = Image.open(currentDirectory + "/" + image_path)
    thumbnail.thumbnail((800, 800))  # Resize the image to fit the frame

    # Create a frame for the image and button
    frame = tk.Frame(root)
    frame.pack(side=side, padx=10, pady=10)

   # Add the text over the image
    text_label = tk.Label(frame, text=image_path)
    text_label.pack(pady=10)


# Add the text over the image
    text_label = tk.Label(frame, text="ImageSize: {size};\n ImageMode: {mode};\n ImageFormat: {format};".format(size=image.size,mode=image.mode,format=image.format,))
    text_label.pack(pady=10)

   # Convert the image to PhotoImage format for displaying in Tkinter
    photo = ImageTk.PhotoImage(thumbnail)
    # Add the image to the frame
    label = tk.Label(frame, image=photo)
    label.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected
    label.pack()

    button = tk.Button(frame,bg="#54e8ff", text="KEEP THIS ONE", command=lambda: on_button_click_remove(direcoryToRemove=otherDirectory,image_path=image_path), pady=10, padx=10)
    button.pack(pady=10)

 

def display_image(index):
    if index >= len(images):  # Stop the loop if all images have been displayed
        return

    # Create the main window
    global root
    root = tk.Tk()
    root.title("Image Viewer")

   # Create a frame for the image and button
    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, padx=10, pady=10)

     # Get image and text from the list
    image_path = images[index]

    diff = determine_images_difference(image_path)
 
   # Add the text over the image
    text_label = tk.Label(frame, text=diff)
    text_label.pack(pady=10)

    
    button = tk.Button(frame,bg="#ff6f00", text="RENAME ONE", command=lambda: on_button_click_rename(image_path), pady=10, padx=10)
    button.pack(pady=10)

    button = tk.Button(frame,bg="#ff6f00", text="SKIP", command=lambda: on_button_click_skip(image_path=image_path), pady=10, padx=10)
    button.pack(pady=10)

    create_image_frame(image_path,tk.LEFT, currentDirectory=mainDirectory,otherDirectory=secondaryDirectory)
    create_image_frame(image_path,tk.RIGHT, currentDirectory=secondaryDirectory,otherDirectory=mainDirectory)

  # Set default window position to be close to the top-left corner
    window_width = 2100  # Adjust the width of the window if needed
    window_height = 1300  # Adjust the height of the window if needed
    x = 10
    y = 10
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")


    if diff == "AUTO_REMOVE":
        on_button_click_remove(secondaryDirectory,image_path)
    # Start the main event loop
    root.mainloop()


    # Continue the loop after the window is closed
    display_image(index + 1)

# List of images, button texts, and image texts


imagess = set(os.listdir(mainDirectory)).intersection(os.listdir(secondaryDirectory))

images = list(imagess)
display_image(0)

# Start the loop by displaying the first image

