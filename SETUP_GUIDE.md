# Quick Start Guide: Mercer RSS Feed Setup

## Step-by-Step Instructions

### ✅ Step 1: Create GitHub Account (if needed)
- Go to https://github.com
- Sign up for a free account
- Verify your email

### ✅ Step 2: Create New Repository

1. Click the **+** icon in top-right corner
2. Select **New repository**
3. Fill in details:
   - **Repository name**: `mercer-rss-feed`
   - **Description**: "Automated RSS feed for Mercer HR content"
   - **Visibility**: ☑️ **Public** (required for GitHub Pages)
   - **Initialize**: Leave all checkboxes UNCHECKED
4. Click **Create repository**

### ✅ Step 3: Upload Files to Repository

You have all the files you need. Here's how to upload them:

**Method 1: Drag & Drop (Easiest)**

1. On the empty repository page, click **uploading an existing file**
2. Drag and drop ALL these files into the upload area:
   - `scrape_feed.py`
   - `README.md`
   - `.gitignore`
   - `requirements.txt`
3. For the workflow file, you'll need to create the folder structure:
   - Click **Add file** → **Create new file**
   - In the filename box, type: `.github/workflows/update-feed.yml`
   - Paste the contents of `update-feed.yml`
   - Click **Commit new file**

**Method 2: Using Git Command Line**

```bash
# Clone your empty repository
git clone https://github.com/YOUR-USERNAME/mercer-rss-feed.git
cd mercer-rss-feed

# Copy all the files I created into this folder
# Then commit and push:
git add .
git commit -m "Initial commit: RSS feed scraper"
git push origin main
```

### ✅ Step 4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **⚙️ Settings** (top tab)
3. Scroll down left sidebar and click **Pages**
4. Under **Build and deployment**:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/ (root)`
5. Click **Save**
6. You'll see a message: "Your site is being built from the main branch"

### ✅ Step 5: Run the Feed Generator

1. Go to **Actions** tab (top of repository)
2. You may see a message about workflows - click **I understand my workflows, go ahead and enable them**
3. Click **Update Mercer RSS Feed** (left sidebar)
4. Click **Run workflow** (blue button on right)
5. Select branch: `main`
6. Click **Run workflow** (green button)
7. Wait 1-2 minutes - you'll see a yellow dot → green checkmark when done
8. Go back to your repository **Code** tab - you should see `mercer_feed.xml`

### ✅ Step 6: Get Your RSS Feed URL

Your RSS feed URL will be:

```
https://YOUR-USERNAME.github.io/mercer-rss-feed/mercer_feed.xml
```

Replace `YOUR-USERNAME` with your actual GitHub username (all lowercase).

**Test it**: Visit this URL in your browser - you should see XML content!

### ✅ Step 7: Add to Coda

1. Open your Coda document
2. Type `/` to open the slash menu
3. Search for and add **RSS Pack**
4. In the RSS Pack configuration:
   - **Feed URL**: Paste your feed URL from Step 6
   - Configure display options as needed
5. Done! Your feed will auto-update daily

## 🔧 Customization Options

### Change Update Schedule

Edit `.github/workflows/update-feed.yml` in your repository:

```yaml
schedule:
  - cron: '0 8 * * *'  # Current: Daily at 8 AM UTC
```

**Examples:**
- Every 6 hours: `'0 */6 * * *'`
- Twice daily: `'0 8,20 * * *'` (8 AM and 8 PM UTC)
- Weekdays only: `'0 8 * * 1-5'`
- Weekly: `'0 8 * * 1'` (Mondays)

### Change Number of Articles

Edit `scrape_feed.py`:

```python
MAX_PAGES = 3  # Change to 1, 2, 5, etc.
# 1 page = ~10 articles
# 3 pages = ~30 articles
# 5 pages = ~50 articles
```

## 🎯 What Happens Next?

1. **Automatic Updates**: GitHub Actions runs daily at 8 AM UTC
2. **Feed Updates**: New articles are scraped and added to `mercer_feed.xml`
3. **Coda Syncs**: Your Coda RSS Pack will detect the changes
4. **You Read**: Latest HR content appears in your Coda page!

## 🆘 Troubleshooting

**"Workflow failed" in Actions tab?**
- Click on the failed run to see error details
- Common fix: Make sure repository is Public
- Check that all files are uploaded correctly

**Feed URL shows 404?**
- Wait 2-3 minutes after enabling GitHub Pages
- Verify Pages is enabled in Settings → Pages
- Check that `mercer_feed.xml` exists in repository

**No new articles appearing?**
- Check Actions tab for latest run status
- Manually trigger: Actions → Run workflow
- Verify the Mercer website structure hasn't changed

**Coda can't read the feed?**
- Test feed URL in browser first
- Ensure repository is Public
- Check RSS Pack documentation for URL format

## 📞 Need Help?

- Check repository Issues tab
- Review GitHub Actions logs
- Test scraper locally: `python scrape_feed.py`

---

**You're all set!** 🎉

Your automated RSS feed will keep you updated with the latest Mercer HR content without any manual work.
