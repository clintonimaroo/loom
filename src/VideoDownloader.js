import React, { useState } from 'react';
import axios from 'axios';

const VideoDownloader = () => {
    const [url, setUrl] = useState('');
    const [message, setMessage] = useState('');

    const handleDownload = async (e) => {
        e.preventDefault();
        setMessage('Downloading...');
        try {
            const response = await axios.post('http://localhost:5000/download', { url }, { responseType: 'blob' });
            const blob = new Blob([response.data], { type: response.data.type });
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', 'loom_video.mp4');
            document.body.appendChild(link);
            link.click();
            link.remove();
            setMessage('Download successful!');
        } catch (error) {
            setMessage('Failed to download video.');
        }
    };

    return (
        <div>
            <h1>Loom Video Downloader</h1>
            <form onSubmit={handleDownload}>
                <input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter Loom video URL"
                    required
                />
                <button type="submit">Download</button>
            </form>
            <p>{message}</p>
        </div>
    );
};

export default VideoDownloader;
