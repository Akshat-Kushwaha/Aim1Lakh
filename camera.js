(async function () {
    try {
        const videoElement = document.getElementById('userCamera');
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = stream;
    } catch (error) {
        console.error("Camera access error: ", error);
        alert("Unable to access the camera. Please grant permissions.");
    }
})();
