import cv2
import torch
from torchvision import transforms
from network import TinyVGG
from pathlib import Path

# Function to preprocess frames
def preprocess_frame(frame):
    # Resize the frame
    frame = cv2.resize(frame, (512, 512))
    # Convert frame to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert frame to tensor
    frame = transforms.ToTensor()(frame)
    return frame

# Load model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
train_data = ['Active','Fatigue']
model_0 = TinyVGG(input_shape=3, hidden_units=40, output_shape=len(train_data)).to(device)
MODEL_PATH = Path("mood_tracker\model")
MODEL_NAME = "model.pth"
MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME
model_0.load_state_dict(torch.load(MODEL_SAVE_PATH,map_location=torch.device('cpu')))

# Initialize camera
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    
    # Preprocess frame
    preprocessed_frame = preprocess_frame(frame)
    
    # Perform prediction
    with torch.no_grad():
        preprocessed_frame = preprocessed_frame.unsqueeze(0).to(device)
        output = model_0(preprocessed_frame)
        _, predicted = torch.max(output, 1)
        prediction = train_data[predicted.item()]
        print(prediction)
    
    # Display prediction
    # cv2.putText(frame, prediction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Live Feed', frame)
    
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

# Release video capture and close window
video_capture.release()
cv2.destroyAllWindows()
