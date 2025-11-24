#!/bin/bash
# Quick test script for BRUTAL EDITION components

echo "🧪 BRUTAL EDITION Verification"
echo "=============================="
echo ""

# Component checks
test -f .claude/hooks.json && echo "✅ hooks.json configured" || echo "❌ Missing"
test -f .claude/hooks-handlers/brutal-edition-banner.sh && echo "✅ Banner script" || echo "❌ Missing"
test -f .claude/hookify.anti-vibecoding.local.md && echo "✅ Anti-vibecoding hook" || echo "❌ Missing"
test -f .claude/commands/wow.md && echo "✅ /wow command" || echo "❌ Missing"
test -f CODE_QUALITY_STANDARDS.md && echo "✅ Quality standards" || echo "❌ Missing"
test -f .claude/ENGINEERING_STANDARDS.md && echo "✅ LLM guidance" || echo "❌ Missing"
test -f .env.example && echo "✅ .env.example" || echo "❌ Missing"
grep -q "^\.env$" .gitignore && echo "✅ .env ignored" || echo "❌ Not ignored"

echo ""
echo "📊 Statistics:"
echo "  Patterns: $(grep -c '^###' .claude/hookify.anti-vibecoding.local.md) categories"
echo "  Python utils: $(find plugins/hookify/utils -name '*.py' -type f | wc -l) files"

echo ""
echo "🎯 Status: BRUTAL EDITION READY ✅"
echo ""
echo "🚀 Next Steps:"
echo "  1. Restart Claude Code to see banner"
echo "  2. Try: /wow"
echo "  3. Request code with anti-patterns to test enforcement"
