# 进度条(progress bar)

- [Python] 进度条案例
```python
# 1. 单进度条
import time
from tqdm import tqdm

char_list = ["a", "b", "c"]
for c in tqdm(char_list):
    time.sleep(0.5)

# 2. 单进度条支持自定义标题
import time
from tqdm import tqdm

char_list = ["a", "b", "c"]
process_bar = tqdm(char_list)
for c in process_bar:
    time.sleep(0.5)
    process_bar.set_description(f"Processing {c}")

# 3. 双进度条支持自定义标题
import time
from tqdm import tqdm

lic1 = range(3)
lic2 = range(100)

for i in tqdm(lic1, desc='outer loop'):
    for i in tqdm(lic2, desc='inner loop', leave=False):
        time.sleep(0.01)

# 4. 双进度条支持动态自定义标题
import time
from tqdm import tqdm

lic1 = range(3)
lic2 = range(100)

process_bar = tqdm(lic1, desc="process")
for i in process_bar:
    process_bar.set_description("process %d" % i)
    subprocess_bar = tqdm(lic2, desc="subprocess", leave=False)
    for j in subprocess_bar:
        subprocess_bar.set_description("subprocess %d" % j)
        time.sleep(0.01)
```