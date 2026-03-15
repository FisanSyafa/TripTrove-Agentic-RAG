"""
Script untuk testing agent secara interaktif
"""
from agent_rag import TripTroveAgent
import sys

def main():
    print("="*60)
    print("🏝️  TripTrove AI Assistant - Interactive Test")
    print("="*60)
    print("\nMemuat agent...")
    
    try:
        agent = TripTroveAgent()
        print("✅ Agent berhasil dimuat!\n")
    except Exception as e:
        print(f"❌ Error loading agent: {e}")
        sys.exit(1)
    
    print("Ketik 'exit' atau 'quit' untuk keluar\n")
    
    while True:
        try:
            # Get user input
            query = input("\n🧑 Anda: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit', 'keluar']:
                print("\n👋 Terima kasih! Sampai jumpa!")
                break
            
            # Get response
            print("\n🤖 TripTrove AI: ", end="", flush=True)
            response = agent.query(query)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Terima kasih! Sampai jumpa!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
