from dataclasses import dataclass
import statistics
import time
import utils
import sys

from veloxsearch.config import SearchAlgorithm
from veloxsearch.velox import Velox


@dataclass
class TestResult:
    # Load time, list of search time
    tries: list[tuple[float, list[float]]]
    load_time_average: float
    load_time_median: float
    search_time_average: float
    search_time_median: float


def main():
    benchmark(
        "starwars_8k_2018.txt",
        limit=10,
        queries=["cor", "o", "tat", "da", "l"],
        steps=100,
    )
    benchmark(
        "french.txt",
        limit=5,
        queries=[
            "c",
            "ba",
            "tot",
            "vinc",
            "pourt",
            "absolu",
            "gentille",
            "anti-",
        ],
        steps=1,
        exclude=[],
    )
    # Requires data/rockyou.txt
    # benchmark(
    #     "rockyou.txt",
    #     limit=5,
    #     queries=["c", "ba", "toto", "vince", "poutac"],
    #     steps=1,
    #     exclude=[],
    # )


def format_results(results: dict[SearchAlgorithm, TestResult]):
    print(f"algo,load_time_avg,load_time_median,search_time_avg,search_time_median")
    for algo, result in results.items():
        print(
            f"{algo},{result.load_time_average*1000}ms,{result.load_time_median*1000}ms,{result.search_time_average*1000}ms,{result.search_time_median*1000}ms"
        )


def benchmark(wordlist: str, limit: int, queries: list[str], steps: int, exclude=[]):
    print(f"# wordlist:{wordlist};limit:{limit};queries:{queries};test steps:{steps}")
    results = {}
    for algorithm in SearchAlgorithm:
        if algorithm in exclude:
            continue

        print(f"+ Benchmarking {algorithm}", file=sys.stderr)

        not_implemented = False
        tries = []

        for i in range(steps):
            start = time.time()
            try:
                velox = Velox(utils.get_config(wordlist, algorithm, limit))
            except NotImplementedError:
                not_implemented = True
                continue

            if not_implemented:
                break

            end = time.time()
            load_time = end - start

            search_times = []
            for query in queries:
                start = time.time()
                velox.complete_prefix(query)
                end = time.time()
                search_times.append(end - start)

            tries.append((load_time, search_times))

        if not_implemented:
            continue

        result = TestResult(
            tries=tries,
            load_time_average=statistics.mean(load for (load, _search) in tries),
            load_time_median=statistics.median(load for (load, _search) in tries),
            search_time_average=statistics.mean(
                search for (_load, search_times) in tries for search in search_times
            ),
            search_time_median=statistics.median(
                search for (_load, search_times) in tries for search in search_times
            ),
        )
        results[algorithm] = result

    format_results(results)


if __name__ == "__main__":
    main()
