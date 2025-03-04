import serial
import time
import numpy as np
import cv2
import tensorflow as tf

# Define the serial port for Arduino (Make sure to change it to your actual Arduino port)
arduino = serial.Serial('COM4', 9600, timeout=1)  # Arduino Port
time.sleep(0.5)  # Wait for Arduino to initialize

# Load the TensorFlow model directly using `tf.keras.models.load_model`
model_path = "C:/Users/chris/Downloads/keras_model.h5/keras_model.h5"  # Make sure the model is in .h5 format
model = tf.keras.models.load_model(model_path, compile=True)  # Load the Keras model

# Define class labels directly in the code (instead of loading from a text file)
class_names = ["Glasses ON", "Glasses OFF"]  # Define your classes here

# Open webcam
cap = cv2.VideoCapture(0)  # Open the first camera (webcam)

def preprocess_frame(frame):
    """Prepares an image frame for model prediction."""
    image = cv2.resize(frame, (224, 224))  # Resize for model input
    image = image.astype(np.float32) / 255.0  # Normalize to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

prev_class = None  # Store previous class
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    processed_frame = preprocess_frame(frame)
    predictions = model.predict(processed_frame)

    class_index = np.argmax(predictions)  # Get the index of the highest prediction
    confidence = np.max(predictions)  # Get the confidence value

    # Check if confidence is above a threshold
    if confidence > 0.5:
        class_name = class_names[class_index]  # Get the class name using the index
        print(f"Prediction: {class_name} with confidence {confidence:.2f}")
        
        # Send signals to Arduino based on classification
        if class_name == "Glasses ON":
            if arduino and arduino.is_open:
                arduino.write(b'2')  # Blink LED twice
        elif class_name == "Glasses OFF":
            if arduino and arduino.is_open:
                arduino.write(b'3')  # Blink LED three times

    # Display video feed
    cv2.imshow("Face Recognition", frame)

    # Exit loop if 'e' is pressed
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

# Cleanup
cap.release()  # Release the webcam
arduino.close()  # Close the serial connection
cv2.destroyAllWindows()  # Close all OpenCV windows

