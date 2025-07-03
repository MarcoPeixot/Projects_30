import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const mongoUri = process.env.MONGO_URI;
const PORT = process.env.PORT || 3000;

mongoose.connect(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch((err) => {
        console.error('MongoDB connection error:', err);
        process.exit(1);
    });

const urlSchema = new mongoose.Schema({
    originalUrl: {
        type: String,
        required: true,
    },
    shortUrl: {
        type: String,
        required: true,
        unique: true,
    },
});

const Url = mongoose.model('Url', urlSchema);

function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

async function generateUniqueShortUrl() {
    let shortUrl;
    let exists = true;
    while (exists) {
        shortUrl = Math.random().toString(36).substring(2, 8);
        exists = await Url.exists({ shortUrl });
    }
    return shortUrl;
}

app.post("/api/shorten", async (req, res) => {
    try {
        const { originalUrl } = req.body;
        if (!originalUrl || !isValidUrl(originalUrl)) {
            return res.status(400).json({ error: "Invalid or missing originalUrl" });
        }
        const shortUrl = await generateUniqueShortUrl();
        const newUrl = new Url({ originalUrl, shortUrl });
        await newUrl.save();
        res.status(201).json({
            originalUrl,
            shortUrl: `${req.protocol}://${req.get('host')}/${shortUrl}`,
        });
    } catch (err) {
        res.status(500).json({ error: "Internal server error" });
    }
});

app.get("/:shortUrl", async (req, res) => {
    try {
        const { shortUrl } = req.params;
        const url = await Url.findOne({ shortUrl });
        if (!url) {
            return res.status(404).json({ error: "URL not found" });
        }
        res.redirect(url.originalUrl);
    } catch (err) {
        res.status(500).json({ error: "Internal server error" });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});