require('dotenv').config();

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { Sequelize, DataTypes } = require('sequelize');

// Initialize Express app
const app = express();
app.use(cors());
app.use(bodyParser.json());

// Database connection
const sequelize = new Sequelize(`process.env.DATABASE_URL`);

// User model
const User = sequelize.define('User', {
    username: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false,
    },
});

// Sync the database
sequelize.sync()
    .then(() => console.log('Database synchronized'))
    .catch(err => console.error('Database synchronization error:', err));

// Define routes
app.get('/', (req, res) => {
    res.send('Welcome to the Stock Advisory App!');
});

// Signup route
app.post('/signup', async (req, res) => {
    const { username, password } = req.body;
    try {
        const newUser = await User.create({ username, password });
        res.status(201).json({ message: 'User registered successfully!', userId: newUser.id });
    } catch (error) {
        res.status(400).json({ error: 'User registration failed.' });
    }
});

// Login route
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    try {
        const user = await User.findOne({ where: { username, password } });
        if (user) {
            res.json({ message: 'Login successful!', userId: user.id });
        } else {
            res.status(401).json({ error: 'Invalid username or password.' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Login failed.' });
    }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
