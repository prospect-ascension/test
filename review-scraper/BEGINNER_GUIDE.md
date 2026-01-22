# Complete Beginner's Guide

**Never used Python or terminal before? No problem!** Follow these exact steps.

---

## Part 1: Get Python (5 minutes)

### On Mac:

1. Press `Cmd + Space` (opens Spotlight)
2. Type `terminal` and press Enter
3. Copy this command and paste it in Terminal:
   ```bash
   python3 --version
   ```
4. Press Enter
5. **If you see**: `Python 3.11.x` or `Python 3.9.x` or similar → **Skip to Part 2**
6. **If you see**: `command not found` → Install Python:
   - Go to: https://www.python.org/downloads/
   - Click the yellow "Download Python" button
   - Open the downloaded file
   - Follow the installer (just keep clicking "Continue")

### On Windows:

1. Press the `Windows key`
2. Type `cmd` and press Enter
3. Type this command:
   ```bash
   python --version
   ```
4. Press Enter
5. **If you see**: `Python 3.x.x` → **Skip to Part 2**
6. **If you see**: an error → Install Python:
   - Go to: https://www.python.org/downloads/
   - Click the yellow "Download Python" button
   - Run the installer
   - **IMPORTANT**: Check the box that says "Add Python to PATH"
   - Click "Install Now"

---

## Part 2: Download the Code (2 minutes)

### Option A: Using Git (if you have it)

In Terminal/Command Prompt, type these commands **one at a time**:

```bash
git clone https://github.com/prospect-ascension/test.git
cd test
git checkout claude/project-planning-GkXUI
cd review-scraper
```

### Option B: Download ZIP (easier)

1. Go to: https://github.com/prospect-ascension/test
2. Click the green "Code" button (top right)
3. Click "Download ZIP"
4. **Unzip the file** (double-click it on Mac, right-click → "Extract All" on Windows)
5. Open Terminal/Command Prompt
6. Navigate to the review-scraper folder:

**On Mac:**
- In Finder, find the `review-scraper` folder inside the unzipped folder
- Drag the folder onto the Terminal window
- Your path will appear in Terminal
- Type `cd ` (with a space) before that path and press Enter

**On Windows:**
- Open File Explorer
- Navigate to the `review-scraper` folder
- Click in the address bar at the top
- Type `cmd` and press Enter
- A command prompt will open in that folder

---

## Part 3: Install Everything (5 minutes)

You should now be in the `review-scraper` folder. Verify by typing:

```bash
ls          # On Mac/Linux
dir         # On Windows
```

You should see files like: `scrape_reviews.py`, `companies.yaml`, `setup.sh`

**If you DON'T see these files**, you're in the wrong folder. Go back to Part 2.

**If you DO see these files**, continue:

### On Mac/Linux:

```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

### On Windows:

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

**This will take 3-5 minutes.** You'll see lots of text scrolling - that's normal!

---

## Part 4: Edit the Companies File (2 minutes)

You need to tell the scraper which companies to scrape.

1. Open the `companies.yaml` file in any text editor:
   - **Mac**: Right-click → Open With → TextEdit
   - **Windows**: Right-click → Open With → Notepad

2. The file already has 7 companies configured with your URLs!
   - Airwallex
   - Wise
   - Revolut
   - WorldFirst
   - Payoneer
   - OFX
   - Currencycloud

3. **You can use it as-is**, or edit if needed:
   - To remove a company: Delete the entire section for that company
   - To add a company: Copy-paste an existing company section and change the URLs
   - If a company doesn't have a page on a platform, set it to `null`

4. Save the file and close it

---

## Part 5: Run the Scraper! (30-60 minutes)

### On Mac/Linux:

```bash
python3 scrape_reviews.py
```

### On Windows:

```bash
python scrape_reviews.py
```

You'll see:

```
============================================================
🔍 REVIEW SCRAPER - Trustpilot, G2, Capterra
============================================================

✅ Loaded 7 companies from companies.yaml

📋 Companies to scrape:
   1. Airwallex (Trustpilot, G2, Capterra)
   2. Wise (Trustpilot, G2, Capterra)
   ...
```

**The scraper is now running!**

You'll see progress messages like:
```
🏢 Scraping Airwallex from Trustpilot...
  🔗 URL: https://uk.trustpilot.com/review/airwallex.com
  📄 Scraping page 1...
  📄 Scraping page 2...
```

**Wait for it to finish.** This takes 30-60 minutes depending on how many reviews exist.

**Don't close the terminal window!**

---

## Part 6: Get Your Results!

When done, you'll see:

```
📊 SCRAPING SUMMARY
============================================================
Total companies scraped: 7
Total reviews collected: 5234

Breakdown by platform:
  - Trustpilot: 2845 reviews
  - G2: 1523 reviews
  - Capterra: 866 reviews

✅ All files saved to ./output/ directory
```

### View Your Data:

1. Find the `output` folder inside `review-scraper`
2. Open any CSV file:
   - **Mac**: Double-click opens in Numbers
   - **Windows**: Double-click opens in Excel
   - **Or**: Upload to Google Sheets

Files you'll find:
- `trustpilot_reviews.csv` - All Trustpilot reviews
- `g2_reviews.csv` - All G2 reviews
- `capterra_reviews.csv` - All Capterra reviews
- `all_reviews.csv` - Everything combined

---

## Troubleshooting

### "python: command not found" or "python3: command not found"

→ Python isn't installed. Go back to Part 1.

### "pip: command not found"

→ Try `pip3` instead of `pip` (on Mac)

### "Cannot find companies.yaml"

→ You're in the wrong folder. Type:
```bash
cd review-scraper
```

### "Failed to load page"

→ Check your internet connection. The scraper needs to access the review websites.

### The scraper is taking forever

→ Normal! Large companies with thousands of reviews take time. Be patient.

### I got an error about YAML

→ There's a typo in your `companies.yaml` file. Common issues:
- Wrong indentation (must be 2 spaces)
- Missing colon after company name
- Forgot to use `null` for missing URLs

### "No reviews found"

→ The website HTML might have changed. Open an issue on GitHub with:
1. Which company failed
2. Which platform failed
3. Copy-paste the error message

---

## What's Next?

Once you have your CSVs:

1. **Open in Excel/Google Sheets** for analysis
2. **Search for keywords** like "slow", "expensive", "support issue"
3. **Compare ratings** across competitors
4. **Look for patterns** in negative reviews
5. **Identify pain points** your product could solve

---

## Need Help?

1. Check this guide again - did you miss a step?
2. Read the error message carefully - it usually tells you what's wrong
3. Try searching Google for the exact error message
4. Open an issue on GitHub with details about what went wrong

---

**You got this! 🚀**
