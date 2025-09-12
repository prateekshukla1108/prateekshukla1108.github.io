#!/bin/bash

echo "🚀 Optimizing images for web performance..."

# Function to optimize images and create WebP versions
optimize_image() {
    local input="$1"
    local base="${input%.*}"
    local ext="${input##*.}"
    local output="${base}-opt.${ext}"
    local webp_output="${base}-opt.webp"

    if [[ "$input" == *.jpg ]] || [[ "$input" == *.jpeg ]]; then
        # JPEG optimization
        magick "$input" -resize '1200x1200>' -quality 85 -strip -interlace Plane "$output"
        # Create WebP version
        magick "$input" -resize '1200x1200>' -quality 85 -strip "$webp_output"
    elif [[ "$input" == *.png ]]; then
        # PNG optimization
        magick "$input" -resize '1200x1200>' -quality 85 -strip "$output"
        # Create WebP version
        magick "$input" -resize '1200x1200>' -quality 85 -strip "$webp_output"
    fi

    if [[ -f "$output" ]]; then
        local old_size=$(stat -f%z "$input" 2>/dev/null || stat -c%s "$input")
        local new_size=$(stat -f%z "$output" 2>/dev/null || stat -c%s "$output")
        local savings=$(( (old_size - new_size) * 100 / old_size ))
        echo "✅ $input: $(numfmt --to=iec-i --suffix=B $old_size) → $(numfmt --to=iec-i --suffix=B $new_size) (${savings}% saved)"
    fi
}

# Create optimized versions
echo "📸 Creating optimized image versions..."
find assets/images -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | while read -r img; do
    if [[ "$img" != *-opt.* ]]; then
        optimize_image "$img"
    fi
done

# Generate responsive images
echo "📱 Generating responsive image sizes..."
find assets/images -type f -name "*-opt.*" | while read -r img; do
    if [[ "$img" != *-small.* ]] && [[ "$img" != *-medium.* ]]; then
        base="${img%.*}"
        ext="${img##*.}"

        # Create smaller versions for different screen sizes
        magick "$img" -resize '800x800>' "${base}-medium.${ext}"
        magick "$img" -resize '400x400>' "${base}-small.${ext}"

        echo "📏 Generated responsive sizes for ${img}"
    fi
done

echo "🎉 Image optimization complete!"
echo "💡 Tip: Use <picture> elements with WebP fallbacks for best performance"
