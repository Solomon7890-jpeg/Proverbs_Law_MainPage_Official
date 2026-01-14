# 🎨 Logo Integration Guide - Rotating Logos

## ✅ What's Been Done

### Logos Copied
I've copied your images to the project:

```
ProVerbS_LaW_mAiN_PAgE/assets/
├── logo_main.jpg  (128.21 KB) - Main/fallback logo
├── logo_1.jpg     (90.95 KB)  - Rotating logo 1
├── logo_2.jpg     (60.84 KB)  - Rotating logo 2
└── logo_3.jpg     (70.82 KB)  - Rotating logo 3
```

### Features Added
✅ **Rotating Logo System** - Logos change every 60 seconds
✅ **Professional Styling** - Circular design with border and shadow
✅ **Smooth Transitions** - Fade in/out animation
✅ **Responsive Design** - Works on all devices

---

## 🎯 How It Works

### Rotation Cycle (60 seconds each)
```
0-60 sec:   Logo 1 displays
60-120 sec: Logo 2 displays
120-180 sec: Logo 3 displays
Then repeats...
```

### Animation Details
- **Fade Duration**: Smooth 2-second fade between logos
- **Logo Size**: 150x150 pixels (circular)
- **Border**: 4px white border with shadow
- **Position**: Centered in header above title

---

## 🚀 Deployment Options

### Option 1: Deploy with Rotating Logos (Recommended) ⭐

```bash
cd ProVerbS_LaW_mAiN_PAgE

# Use the version with logos
cp integrated_chatbot_with_logos.py app.py

# Deploy
python deploy_to_hf.py
```

**Important**: The `assets` folder with logos will be deployed automatically!

### Option 2: Test Locally First

```bash
cd ProVerbS_LaW_mAiN_PAgE

# Run locally to see the rotating logos
python integrated_chatbot_with_logos.py

# Visit: http://localhost:7860
# Watch the logos rotate every 60 seconds!
```

### Option 3: Windows One-Click

Create a new batch file or use existing one:
```bash
cd ProVerbS_LaW_mAiN_PAgE
cp integrated_chatbot_with_logos.py app.py
DEPLOY_NOW.bat
```

---

## 📁 File Structure for Deployment

When you deploy, make sure these files are included:

```
ProVerbS_LaW_mAiN_PAgE/
├── app.py (or integrated_chatbot_with_logos.py renamed)
├── README.md
├── requirements.txt (if you have one)
└── assets/
    ├── logo_1.jpg
    ├── logo_2.jpg
    ├── logo_3.jpg
    └── logo_main.jpg
```

---

## 🎨 Customization Options

### Change Rotation Speed

Edit `integrated_chatbot_with_logos.py` line 298:

```javascript
// Change from 60000 (60 sec) to your desired time in milliseconds
setInterval(showNextLogo, 60000);  // 60 seconds
setInterval(showNextLogo, 30000);  // 30 seconds
setInterval(showNextLogo, 120000); // 2 minutes
```

### Change Logo Size

Edit CSS at line 228:

```css
.rotating-logo {
    width: 150px;   /* Change size */
    height: 150px;  /* Keep same as width for circle */
    border-radius: 50%;
    /* ... */
}
```

### Change Logo Border/Shadow

Edit CSS at line 233:

```css
border: 4px solid rgba(255, 255, 255, 0.8);  /* Border thickness and color */
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);   /* Shadow */
```

### Add More Logos

1. Copy additional logo images to `assets/` folder:
   ```bash
   copy "your_logo_4.jpg" "assets/logo_4.jpg"
   ```

2. Edit the HTML section (line 288) to add logo_4:
   ```html
   <img src="file/assets/logo_4.jpg" class="rotating-logo logo-4" alt="ProVerBs Logo 4" style="display: none;">
   ```

3. Update JavaScript to include 4 logos in rotation

---

## 🔧 Troubleshooting

### Issue: Logos don't appear after deployment

**Solution 1**: Check that assets folder is uploaded
- Go to your Space on HF
- Click "Files" tab
- Verify `assets/` folder exists with all logos

**Solution 2**: Re-upload assets manually
- In HF Space, click "Files" → "Add file" → "Upload files"
- Upload the entire `assets` folder

### Issue: Logos don't rotate

**Solution**: Clear browser cache and refresh
- Press Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- JavaScript may be cached

### Issue: Logos appear stretched/distorted

**Solution**: Check image aspect ratio
- Logos should be square (1:1 aspect ratio)
- Or adjust CSS to `object-fit: contain` instead of `cover`

### Issue: First logo doesn't show

**Solution**: Check that logo_1.jpg has `display: block` in HTML:
```html
<img src="file/assets/logo_1.jpg" class="rotating-logo logo-1" alt="ProVerBs Logo 1" style="display: block;">
```

---

## 📋 Deployment Checklist

Before deploying:
- [ ] Assets folder exists in ProVerbS_LaW_mAiN_PAgE/
- [ ] All 4 logo files are in assets/ folder
- [ ] Logo files are named correctly (logo_1.jpg, logo_2.jpg, logo_3.jpg)
- [ ] `integrated_chatbot_with_logos.py` is ready
- [ ] (Optional) Tested locally first

Deploy:
- [ ] Copy integrated_chatbot_with_logos.py to app.py
- [ ] Run deployment script
- [ ] Include assets folder in deployment

After deployment:
- [ ] Check that logos display
- [ ] Verify rotation works (wait 60+ seconds)
- [ ] Test on mobile device
- [ ] Check different browsers

---

## 🎭 Logo Display Details

### Header Layout
```
┌─────────────────────────────────┐
│                                 │
│        [Rotating Logo]          │ ← 150x150px circle
│                                 │
│   ⚖️ ProVerBs Legal AI Platform │
│                                 │
│ Lawful vs. Legal: Dual Analysis│
│                                 │
└─────────────────────────────────┘
```

### CSS Classes Applied
- `.rotating-logo` - Base styling for all logos
- `.logo-1`, `.logo-2`, `.logo-3` - Individual logo selectors
- Animation delays: 0s, 20s, 40s for smooth rotation

---

## 🌐 HF Space File Paths

In your deployed Space, logos are accessed via:
```
file/assets/logo_1.jpg
file/assets/logo_2.jpg
file/assets/logo_3.jpg
```

This is Gradio's special file serving path for static assets.

---

## 💡 Pro Tips

1. **Image Format**: JPG is good for photos, PNG for graphics with transparency
2. **Image Size**: Keep under 200KB for fast loading
3. **Aspect Ratio**: Square images (1:1) work best for circular display
4. **Quality**: Use good quality but compress for web
5. **Testing**: Always test locally before deploying

---

## 📸 Your Logo Files

**Source Location**: 
```
C:\Users\freet\OneDrive\Documents\SOLO'CODES\MODULES\New folder\
```

**Copied To**:
```
ProVerbS_LaW_mAiN_PAgE\assets\
```

**Main Logo**: 20250515_061525560_iOS.jpg → logo_main.jpg (128.21 KB)

**Rotating Logos**:
- 20250515_061454922_iOS.jpg → logo_1.jpg (90.95 KB)
- 20250515_061533625_iOS.jpg → logo_2.jpg (60.84 KB)
- 20250515_061538456_iOS.jpg → logo_3.jpg (70.82 KB)

---

## ✅ Ready to Deploy!

Your logos are integrated and ready to go!

**Quick Deploy**:
```bash
cd ProVerbS_LaW_mAiN_PAgE
cp integrated_chatbot_with_logos.py app.py
python deploy_to_hf.py
```

**Your rotating logos will be live at:**
https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE

---

**Questions? Need to adjust the rotation speed or styling? Just ask!**
