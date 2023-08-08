USE crypto_analysis;

-- Create the free_signals table
CREATE TABLE free_signals (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    coin_name TEXT,
    buy_range TEXT,
    take_profit TEXT,
    stop_loss TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the users_db table
CREATE TABLE users_db (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50),
    password TEXT,
    cpassword TEXT
);
