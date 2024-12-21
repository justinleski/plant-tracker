import { useState } from 'react';
import Webcam from "react-webcam";

const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
};
  
function WebcamCapture() {
    
    const sendImageToBackend = async (imageSrc) => {
        if (!imageSrc) return;
    
        try {
          // Send POST request to the backend
          const response = await fetch('/api/v1/models/plant_model:predict', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              instances: [{
                image_bytes: { b64: imageSrc.split(',')[1] } // Send the base64 string without the prefix
              }]
            }),
          });
    
          const result = await response.json();
          console.log("Response from backend:", result);
        } catch (error) {
          console.error("Error sending image to backend:", error);
        }
      };
    
    return (<Webcam
        audio={false}
        height={720}
        screenshotFormat="image/jpeg"
        width={1280}
        videoConstraints={videoConstraints}
    >
        {({ getScreenshot }) => (
        <button
            onClick={() => {
                const imageSrc = getScreenshot();
                if (imageSrc) {
                    console.log("Success");
                    sendImageToBackend(imageSrc);
                }
            }}
        >
            Capture Photo
        </button>
        )}
    </Webcam>)

}

export default WebcamCapture