#!/bin/bash


set -e

echo "🚀 Setting up Container Loading Optimization App environment..."

echo "📦 Updating package list..."
sudo apt-get update

echo "🗄️ Installing SQLite development libraries..."
sudo apt-get install -y libsqlite3-dev

echo "🐍 Installing Python development headers..."
sudo apt-get install -y python3-dev

echo "🔧 Installing build essentials..."
sudo apt-get install -y build-essential

echo "🌐 Installing curl..."
sudo apt-get install -y curl

echo "🧹 Cleaning up..."
sudo apt-get autoremove -y
sudo apt-get autoclean

echo "✅ Environment setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Set up environment variables (PYTHONPATH=. DATABASE_URL=sqlite:///app.db)"
echo "2. Install Python dependencies: cd backend && pip install -r requirements.txt"
echo "3. Install Node.js dependencies: cd frontend && npm install"
echo "4. Run the application: See README.md for detailed instructions"
