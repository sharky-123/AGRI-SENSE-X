# FARM-SENSE X (v2.5) - Mobile Web Application Deployment Guide

## 🚀 Overview
This repository contains the mobile-first, responsive web application for **FARM-SENSE X v2.5** configured for direct zero-configuration deployment on **Vercel** without any dependencies on Streamlit.

---

## 📁 Project Structure
```
agri-sense-x/
├── api/
│   └── index.py             # Vercel Serverless Python Backend (REST API)
├── public/                  # Mobile PWA Frontend
│   ├── index.html           # Native Mobile Application Layout
│   ├── styles.css           # Modern Dark-Mode Tailwind-like Mobile Styling
│   └── app.js               # Client-side Controller & Satellite Sync
├── vercel.json              # Vercel Serverless Routing & Deployment Config
├── run_mobile_web.py        # Local Dev Server (Runs locally at http://localhost:5000)
└── requirements.txt         # Dependencies
```

---

## 💻 Local Testing (Before Vercel)
To test the mobile web app on your laptop or mobile browser via local WiFi:

```bash
python run_mobile_web.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.
*(Tip: Press `F12` in Chrome/Edge and click the mobile device icon to view the native phone layout).*

---

## 🌐 How to Deploy on Vercel (100% Free)

### Method 1: Using GitHub (Recommended)
1. Push this `agri-sense-x` folder to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Deploy FARM-SENSE X Mobile Web on Vercel"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```
2. Go to **[vercel.com](https://vercel.com)** and sign in with GitHub.
3. Click **"Add New Project"** > Select your repository.
4. Leave all build settings default (`vercel.json` automatically configures routes).
5. Click **"Deploy"**.
6. Within 60 seconds, Vercel will give you a live production URL (e.g. `https://farm-sense-x.vercel.app`).

### Method 2: Using Vercel CLI (Direct from Terminal)
If you have Node.js and Vercel CLI installed:
```bash
npm i -g vercel
vercel
```
Follow the 3 prompts on terminal and your app will be live immediately!
