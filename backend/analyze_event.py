from ingestion.models import TelemetryEvent
from datetime import datetime, timedelta
import json

def analyze_network_events():
    """Analyze network events"""
    print("\n" + "="*80)
    print("NETWORK EVENTS ANALYSIS")
    print("="*80)
    
    network_events = TelemetryEvent.objects.filter(event_type='network')
    total = network_events.count()
    
    if total == 0:
        print("\n⚠️  No network events found!")
        print("\nTo generate network events:")
        print("  1. Open Chrome and visit a website")
        print("  2. Run: Invoke-WebRequest https://google.com")
        print("  3. Run: curl https://example.com")
        return
    
    print(f"\nTotal network events: {total}")
    
    # Group by process
    processes = {}
    for event in network_events:
        if event.raw_data and 'network' in event.raw_data:
            proc = event.raw_data['network'].get('image', 'Unknown')
            processes[proc] = processes.get(proc, 0) + 1
    
    print("\nTop processes making network connections:")
    for proc, count in sorted(processes.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {proc[:50]:50} : {count} connections")
    
    # Show recent connections
    print(f"\n{'-'*80}")
    print("LATEST 5 NETWORK CONNECTIONS:")
    print('-'*80)
    
    for i, event in enumerate(network_events.order_by('-created_at')[:5], 1):
        if event.raw_data and 'network' in event.raw_data:
            net = event.raw_data['network']
            time = event.created_at.strftime('%H:%M:%S')
            proc = net.get('image', 'Unknown').split('\\')[-1]  # Get filename only
            
            print(f"\n{i}. [{time}] {proc}")
            print(f"   → Destination: {net.get('dest_ip')}:{net.get('dest_port')}")
            print(f"   → Protocol: {net.get('protocol', 'Unknown')}")

def analyze_file_events():
    """Analyze file events"""
    print("\n" + "="*80)
    print("FILE EVENTS ANALYSIS")
    print("="*80)
    
    file_events = TelemetryEvent.objects.filter(event_type='file')
    total = file_events.count()
    
    if total == 0:
        print("\n⚠️  No file events found!")
        print("\nTo generate file events:")
        print("  1. Create file: echo 'test' > C:\\temp\\test.txt")
        print("  2. Copy file: copy C:\\temp\\test.txt C:\\temp\\test2.txt")
        print("  3. Open notepad and save a file")
        return
    
    print(f"\nTotal file events: {total}")
    
    # Group by operation
    operations = {}
    for event in file_events:
        if event.raw_data and 'file' in event.raw_data:
            op = event.raw_data['file'].get('operation', 'Unknown')
            operations[op] = operations.get(op, 0) + 1
    
    print("\nFile operations:")
    for op, count in operations.items():
        print(f"  • {op:10} : {count} files")
    
    # Show recent file operations
    print(f"\n{'-'*80}")
    print("LATEST 5 FILE OPERATIONS:")
    print('-'*80)
    
    for i, event in enumerate(file_events.order_by('-created_at')[:5], 1):
        if event.raw_data and 'file' in event.raw_data:
            file = event.raw_data['file']
            time = event.created_at.strftime('%H:%M:%S')
            
            print(f"\n{i}. [{time}] {file.get('operation', 'Unknown').upper()}")
            print(f"   → File: {file.get('path', 'Unknown')}")
            print(f"   → Process: {file.get('process_image', 'Unknown')}")

def show_statistics():
    """Show overall statistics"""
    print("\n" + "="*80)
    print("OVERALL STATISTICS")
    print("="*80)
    
    total = TelemetryEvent.objects.count()
    process_count = TelemetryEvent.objects.filter(event_type='process').count()
    file_count = TelemetryEvent.objects.filter(event_type='file').count()
    network_count = TelemetryEvent.objects.filter(event_type='network').count()
    
    print(f"\nTotal events: {total}")
    print(f"  • Process events: {process_count} ({process_count/total*100:.1f}%)")
    print(f"  • File events: {file_count} ({file_count/total*100:.1f}%)")
    print(f"  • Network events: {network_count} ({network_count/total*100:.1f}%)")
    
    # Recent activity (last hour)
    one_hour_ago = datetime.now() - timedelta(hours=1)
    recent = TelemetryEvent.objects.filter(created_at__gte=one_hour_ago).count()
    print(f"\nEvents in last hour: {recent}")

if __name__ == '__main__':
    print("="*80)
    print(" "*25 + "EDR EVENT ANALYSIS")
    print("="*80)
    
    show_statistics()
    analyze_network_events()
    analyze_file_events()
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)
