// backend/models/User.js
const { Model, DataTypes, Sequelize } = require('sequelize');
console.log("DATABASE_URL:", process.env.DATABASE_URL);
const sequelize = new Sequelize(process.env.DATABASE_URL, {
    dialect: 'postgres', // Add this line to specify PostgreSQL
});

class User extends Model {}

User.init({
    name: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    email: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false,
    },
}, {
    sequelize,
    modelName: 'User',
});

module.exports = User;
