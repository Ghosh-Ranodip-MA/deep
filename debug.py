import os
import sys
import traceback

print("="*50)
print("🔍 DEBUGGING RENDER DEPLOYMENT")
print("="*50)
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print("\n📂 Files in current directory:")
for f in os.listdir('.'):
    print(f"  - {f}")

print("\n📂 Files in app/ directory:")
if os.path.exists('app'):
    for f in os.listdir('app'):
        print(f"  - {f}")
else:
    print("  ❌ app/ directory not found!")

print("\n🔧 Trying to import app.main...")
try:
    from app.main import app
    print("✅ SUCCESS: app.main imported!")
    print(f"✅ App routes: {[route.path for route in app.routes]}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\n📝 Full traceback:")
    traceback.print_exc()

print("\n✅ Debug complete")