import pytest
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
import time

def run_independent_tests() -> List[Tuple[str, bool]]:
    """运行独立测试"""
    results = []
    independent_tests = [
        "test_workflow_loader.py",
        "test_workflow_controller.py"
    ]
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(pytest.main, [f"tests/{test}"]) 
            for test in independent_tests
        ]
        results = [
            (test, future.result() == 0)
            for test, future in zip(independent_tests, futures)
        ]
    return results

def run_sequential_tests() -> List[Tuple[str, bool]]:
    """运行有依赖的测试"""
    sequential_tests = [
        "test_engineer.py",
        "test_qa_engineer.py"
    ]
    return [
        (test, pytest.main([f"tests/{test}"]) == 0)
        for test in sequential_tests
    ]

def main():
    start_time = time.time()
    print("Starting test suite...")
    
    # 并行运行独立测试
    independent_results = run_independent_tests()
    
    # 串行运行依赖测试
    sequential_results = run_sequential_tests()
    
    # 输出结果
    all_results = independent_results + sequential_results
    passed = sum(1 for _, success in all_results if success)
    total = len(all_results)
    
    print("\nTest Results:")
    for test, success in all_results:
        status = "✓" if success else "✗"
        print(f"{status} {test}")
    
    print(f"\nTotal: {passed}/{total} passed")
    print(f"Time taken: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    main()
