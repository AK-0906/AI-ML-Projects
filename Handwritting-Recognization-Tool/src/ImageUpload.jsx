// src/ImageUpload.js
import React, { useState } from 'react';

const ImageUpload = () => {
    const [file, setFile] = useState(null);
    const [text, setText] = useState('');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('http://3.111.217.121/upload', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            setText(data.text);
        } catch (error) {
            console.error('Error uploading the file:', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
            {text && <p>Generated Text: {text}</p>}
        </div>
    );
};

export default ImageUpload;
