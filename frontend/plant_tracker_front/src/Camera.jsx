import Webcam from "react-webcam";
import * as tf from '@tensorflow/tfjs';

const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
};
  
function WebcamCapture() {
    
  const preprocessImage = async (base64Image, targetHeight, targetWidth) => {
      const img = new Image();
      img.src = `data:image/jpeg;base64,${base64Image.replace(/^data:image\/\w+;base64,/, '')}`;
      
      return new Promise((resolve) => {
          img.onload = () => {
              const canvas = document.createElement('canvas');
              canvas.width = targetWidth;
              canvas.height = targetHeight;
      
              const ctx = canvas.getContext('2d');
              ctx.drawImage(img, 0, 0, targetWidth, targetHeight);
      
              const imageData = ctx.getImageData(0, 0, targetWidth, targetHeight);
              const tensor = tf.browser.fromPixels(imageData)
                  .expandDims(0) // Batch dimension: [1, 128, 128, 3]
                  .toFloat()
                  .div(255.0); // Normalize to [0, 1] range
              
              resolve(tensor.arraySync()); // Convert tensor to raw JS array
          };
      });
  };

    const sendImageToBackend = async (imageSrc) => {
        if (!imageSrc) return;
    
        try {
          // Preprocess the image; convert to correct format and size of 128x128
          const preprocessedData = await preprocessImage(imageSrc, 128, 128);

          // Send POST request to the backend
          const response = await fetch('/api/v1/models/plant_model:predict', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              instances: preprocessedData
            }),
          });
    
          const result = await response.json();
          console.log("Response from backend:", result);

          // Once we get the response, map it to 



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