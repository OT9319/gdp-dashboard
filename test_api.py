#!/usr/bin/env python3
"""
Test script for Constitutional Architecture API
Validates all Zapier integration endpoints
"""
import requests
import json
import time
import sys

API_BASE = "http://localhost:8000"

def test_api():
    print("🧪 Testing Constitutional Architecture API")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['message']}")
            print(f"   System: {data['system']}")
            print(f"   AEGIS Status: {data['aegis_status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Authentication
    print("\n2. Testing authentication...")
    try:
        response = requests.post(f"{API_BASE}/api/auth/token")
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data["access_token"]
            print("✅ Authentication successful")
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False
    
    # Test 3: AEGIS Content Filter (compliant content)
    print("\n3. Testing AEGIS filter with compliant content...")
    try:
        filter_data = {"content": "This is a well-structured task that follows constitutional principles"}
        response = requests.post(f"{API_BASE}/api/security/filter", headers=headers, json=filter_data)
        if response.status_code == 200:
            result = response.json()
            if result["is_compliant"]:
                print(f"✅ AEGIS filter passed: compliant content (confidence: {result['confidence']})")
            else:
                print(f"❌ AEGIS filter failed: should be compliant but was rejected")
                return False
        else:
            print(f"❌ AEGIS filter failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AEGIS filter failed: {e}")
        return False
    
    # Test 4: AEGIS Content Filter (non-compliant content)
    print("\n4. Testing AEGIS filter with non-compliant content...")
    try:
        filter_data = {"content": "This is urgent and needs immediate attention ASAP!"}
        response = requests.post(f"{API_BASE}/api/security/filter", headers=headers, json=filter_data)
        if response.status_code == 200:
            result = response.json()
            if not result["is_compliant"]:
                print(f"✅ AEGIS filter passed: non-compliant content rejected")
                print(f"   Reason: {result['reason']}")
            else:
                print(f"❌ AEGIS filter failed: should reject non-compliant content")
                return False
        else:
            print(f"❌ AEGIS filter failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AEGIS filter failed: {e}")
        return False
    
    # Test 5: Task Creation
    print("\n5. Testing task creation...")
    try:
        tasks_created = []
        test_tasks = [
            {"name": "Review quarterly report", "priority": "💡 Normal", "content": "Q4 financial analysis"},
            {"name": "Update documentation", "priority": "⚡ High", "content": "API documentation update"},
            {"name": "Code review session", "priority": "📝 Low", "content": "Review pending PRs"},
        ]
        
        for task_data in test_tasks:
            response = requests.post(f"{API_BASE}/api/tasks", headers=headers, json=task_data)
            if response.status_code == 200:
                task = response.json()
                tasks_created.append(task)
                print(f"✅ Task created: {task['name']} (ID: {task['id']})")
            else:
                print(f"❌ Task creation failed: {response.status_code}")
                return False
        
        print(f"   Total tasks created: {len(tasks_created)}")
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return False
    
    # Test 6: Workload Summary
    print("\n6. Testing workload summary...")
    try:
        response = requests.get(f"{API_BASE}/api/tasks/workload", headers=headers)
        if response.status_code == 200:
            workload = response.json()
            print("✅ Workload summary retrieved:")
            print(f"   Total tasks: {workload['total_tasks']}")
            print(f"   Total minutes: {workload['total_minutes']}")
            print(f"   By priority: {workload['tasks_by_priority']}")
            print(f"   By status: {workload['status_breakdown']}")
        else:
            print(f"❌ Workload summary failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Workload summary failed: {e}")
        return False
    
    # Test 7: List all tasks
    print("\n7. Testing task listing...")
    try:
        response = requests.get(f"{API_BASE}/api/tasks", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Tasks listed: {len(tasks)} tasks found")
            for task in tasks[:3]:  # Show first 3
                print(f"   - {task['name']} ({task['priority']}) - {task['estimated_minutes']}min")
        else:
            print(f"❌ Task listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Task listing failed: {e}")
        return False
    
    print("\n🎉 All tests passed! API is ready for Zapier integration.")
    print("\nNext steps:")
    print("1. Deploy the API to a public URL")
    print("2. Configure your Zapier integrations using the endpoints")
    print("3. Set up Notion databases and Gmail labels")
    return True

def main():
    # Wait for API to be ready
    print("Waiting for API to be ready...")
    for i in range(10):
        try:
            response = requests.get(f"{API_BASE}/")
            if response.status_code == 200:
                break
        except:
            pass
        time.sleep(1)
        print(".", end="", flush=True)
    
    print("\n")
    
    # Run tests
    if test_api():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()