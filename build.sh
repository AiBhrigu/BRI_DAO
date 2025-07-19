#!/bin/bash
echo "🔧 Building Whitepaper PDFs..."

mkdir -p docs

# English
if [ -f docs/Whitepaper_EN.md ]; then
    pandoc docs/Whitepaper_EN.md -o docs/Whitepaper_EN.pdf --pdf-engine=xelatex -V mainfont="DejaVu Serif"
    echo "✅ EN PDF generated"
fi

# Russian
if [ -f docs/Whitepaper_RU.md ]; then
    pandoc docs/Whitepaper_RU.md -o docs/Whitepaper_RU.pdf --pdf-engine=xelatex -V mainfont="DejaVu Serif"
    echo "✅ RU PDF generated"
fi

echo "📄 Done!"
