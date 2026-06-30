import cv2
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

# ── 1. Load Image ──────────────────────────────────────────
img = cv2.imread('data/cloudy.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print(f"Image loaded: {img_rgb.shape}")

# ── 2. Detect Clouds (bright white regions) ─────────────────
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Cloud pixels are bright (high value in all channels)
_, cloud_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Clean up mask
kernel = np.ones((5,5), np.uint8)
cloud_mask = cv2.morphologyEx(cloud_mask, cv2.MORPH_CLOSE, kernel)
cloud_mask = cv2.morphologyEx(cloud_mask, cv2.MORPH_DILATE, kernel)

print(f"Cloud pixels detected: {np.sum(cloud_mask > 0)}")

# ── 3. Remove Clouds Using Inpainting ──────────────────────
result = cv2.inpaint(img, cloud_mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)
result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

# ── 4. Calculate Metrics ────────────────────────────────────
psnr_score = psnr(img_rgb, result_rgb)
ssim_score = ssim(img_rgb, result_rgb, channel_axis=2)
print(f"\n=== RESULTS ===")
print(f"PSNR : {psnr_score:.2f} dB")
print(f"SSIM : {ssim_score:.4f}")

# ── 5. Save Visual Output ───────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Cloud Removal - LISS-IV Imagery', fontsize=16, fontweight='bold')

axes[0].imshow(img_rgb)
axes[0].set_title('Input: Cloudy Image', fontsize=13)
axes[0].axis('off')

axes[1].imshow(cloud_mask, cmap='gray')
axes[1].set_title('Cloud Mask Detected', fontsize=13)
axes[1].axis('off')

axes[2].imshow(result_rgb)
axes[2].set_title('Output: Cloud Removed', fontsize=13)
axes[2].axis('off')

plt.tight_layout()
plt.savefig('result.png', dpi=150, bbox_inches='tight')
print("\nResult saved to result.png")
